"""Pure declared lifetime ledger, not actual deletion or reclaim authorization."""
import json
import re

MAX_INPUT_BYTES = 32768
MAX_OUTPUT_BYTES = 262144
MAX_DEPTH = 6
MAX_NUMERIC_CHARS = 10
IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,23}", re.ASCII)
CONTEXT = {
    "platform": ("posix_regular", "windows", "unknown"),
    "reference_coverage": ("complete_declared", "partial", "unknown"),
    "event_outcomes": ("assumed_success", "failed", "unknown"),
}
FEATURES = frozenset(("dup", "fork", "mmap", "async_io", "tmpfile", "remote_fs", "snapshot",
                      "crash", "permissions", "symlink", "race", "external_refs", "secure_erase", "descriptor_reuse"))
EVENT_FIELDS = {
    "link": ("source_name", "new_name"), "unlink": ("name",),
    "open": ("name", "reference_id"), "close": ("reference_id",),
    "rename": ("source_name", "new_name"), "replace": ("source_name", "new_name"),
    "link_from_reference": ("reference_id", "new_name"),
}
ASSUMPTIONS = ("invented_ids", "declared_complete_references", "events_assumed_successful", "ordinary_regular_subset")
NOT_VERIFIED = ("input_truth", "reference_coverage", "actual_deletion", "storage_reclaimed",
                "secure_erasure", "durability", "permission_authorization")


class _Invalid(ValueError):
    def __init__(self, reason, status="rejected"):
        self.reason, self.status = reason, status


class _Transition(ValueError):
    def __init__(self, violation):
        self.violation = violation


def _outcome(status, reason):
    return {"status": status, "complete": status == "model_complete", "reason": reason,
            "actual_deletion": "unverified", "storage_reclaimed": "unverified",
            "secure_erasure": "unverified", "durability": "unverified", "permission_authorization": "unverified",
            "assumptions": list(ASSUMPTIONS), "not_verified": list(NOT_VERIFIED)}


def _keys(value, expected):
    if type(value) is not dict or len(value) != len(expected):
        raise _Invalid("object_shape")
    if any(type(key) is not str or len(key) > 32 for key in value) or set(value) != expected:
        raise _Invalid("object_shape")
    return value


def _list(value, maximum, minimum=0):
    if type(value) is not list or len(value) < minimum:
        raise _Invalid("list_shape")
    if len(value) > maximum:
        raise _Invalid("list_limit", "over_limit")
    return value


def _identifier(value):
    if type(value) is not str or len(value) > 24 or IDENTIFIER.fullmatch(value) is None:
        raise _Invalid("identifier")
    return value


def _enum(value, choices):
    if type(value) is not str or len(value) > 32 or value not in choices:
        raise _Invalid("enum")
    return value


def _integer_value(value):
    if type(value) is not int or not 0 <= value <= 999999999:
        raise _Invalid("integer_range")
    return value


def _mapping_rows(value):
    rows = []
    for row in _list(value, 8):
        _keys(row, {"id", "file_id"})
        rows.append((_identifier(row["id"]), _identifier(row["file_id"])))
    return rows


def _validated(value):
    root = _keys(value, {"id", "version", "profile", "files", "names", "references", "events", "context"})
    label, version, profile = _identifier(root["id"]), _integer_value(root["version"]), _identifier(root["profile"])
    files = []
    for row in _list(root["files"], 4, 1):
        _keys(row, {"id", "kind"})
        files.append((_identifier(row["id"]), _enum(row["kind"], ("regular", "directory", "symlink", "other", "unknown"))))
    names, references = _mapping_rows(root["names"]), _mapping_rows(root["references"])
    events = []
    for row in _list(root["events"], 24):
        # Check exact keys/types before key lookup or operation-driven dispatch.
        if type(row) is not dict or not 2 <= len(row) <= 4:
            raise _Invalid("object_shape")
        if any(type(key) is not str or len(key) > 32 for key in row) or "op" not in row:
            raise _Invalid("object_shape")
        operation = _enum(row["op"], EVENT_FIELDS)
        fields = EVENT_FIELDS[operation]
        _keys(row, {"id", "op", *fields})
        event = {"id": _identifier(row["id"]), "op": operation}
        for field in fields:
            event[field] = _identifier(row[field])
        events.append(event)
    context = _keys(root["context"], {*CONTEXT, "excluded_features"})
    declarations = [(field, _enum(context[field], choices)) for field, choices in CONTEXT.items()]
    features = [_enum(feature, FEATURES) for feature in _list(context["excluded_features"], 16)]
    if len(set(features)) != len(features):
        raise _Invalid("duplicate_feature")
    # All occurrences validate before comparisons/dedup; never skip shared aliases.
    for rows in (files, names, references, [(event["id"], None) for event in events]):
        if len({row[0] for row in rows}) != len(rows):
            raise _Invalid("duplicate_identity")
    catalog = {file_id for file_id, _ in files}
    if any(file_id not in catalog for _, file_id in names + references):
        raise _Invalid("unknown_file")
    represented = {file_id for _, file_id in names + references}
    if catalog != represented:
        raise _Invalid("initial_unreferenced_file")
    name_ids, reference_ids = {name for name, _ in names}, {ref for ref, _ in references}
    for event in events:
        for field in EVENT_FIELDS[event["op"]]:
            (reference_ids if field == "reference_id" else name_ids).add(event[field])
    if len(name_ids) > 8 or len(reference_ids) > 8:
        raise _Invalid("identifier_count_limit", "over_limit")
    unsupported = [f"context_{field}_{declaration}" for field, declaration in declarations if declaration != CONTEXT[field][0]]
    unsupported.extend(f"feature_{feature}" for feature in features)
    unsupported.extend(f"kind_{file_id}" for file_id, kind in files if kind != "regular")
    unsupported.extend(f"op_{event['id']}_{event['op']}" for event in events if event["op"] not in ("link", "unlink", "open", "close"))
    if version != 1:
        unsupported.append("version")
    if profile != "link_lifetime_v1":
        unsupported.append("profile")
    return (label, sorted(catalog), dict(names), dict(references), events), sorted(unsupported)


def _eligible(name_count, reference_count):
    return name_count == 0 and reference_count == 0


def _snapshot(catalog, names, references):
    files = []
    for file_id in catalog:
        nc = sum(binding == file_id for binding in names.values())
        rc = sum(binding == file_id for binding in references.values())
        basis = "names_and_references" if nc and rc else "names_only" if nc else "references_only" if rc else "none"
        files.append({"id": file_id, "link_count": nc, "open_reference_count": rc,
                      "retention_basis": basis, "reclamation_eligible": _eligible(nc, rc)})
    return {"names": [{"id": name, "file_id": names[name]} for name in sorted(names)],
            "references": [{"id": ref, "file_id": references[ref]} for ref in sorted(references)], "files": files}


def _link(names, event):
    if event["source_name"] not in names:
        raise _Transition("missing_name")
    if event["new_name"] in names:
        raise _Transition("name_exists")
    names[event["new_name"]] = names[event["source_name"]]


def _unlink(names, event):
    if event["name"] not in names:
        raise _Transition("missing_name")
    del names[event["name"]]


def _close(references, event):
    if event["reference_id"] not in references:
        raise _Transition("missing_reference")
    del references[event["reference_id"]]


def _apply(names, references, used_references, event):
    op = event["op"]
    if op == "link":
        _link(names, event)
    elif op == "unlink":
        _unlink(names, event)
    elif op == "close":
        _close(references, event)
    else:
        if event["name"] not in names:
            raise _Transition("missing_name")
        if event["reference_id"] in used_references:
            raise _Transition("reference_reuse")
        references[event["reference_id"]] = names[event["name"]]
        used_references.add(event["reference_id"])


def _run(data):
    label, catalog, names, references, events = data
    used = set(references)
    initial = _snapshot(catalog, names, references)
    steps = []
    for index, event in enumerate(events):
        try:
            _apply(names, references, used, event)
        except _Transition as failure:
            # Return no partially replayed state; local prefix never escapes.
            return {**_outcome("rejected", "invalid_transition"), "violation": failure.violation, "event_index": index}
        steps.append({"index": index, "id": event["id"], "op": event["op"], "state": _snapshot(catalog, names, references)})
    return {**_outcome("model_complete", "declared_lifetime_trace_only"), "id": label, "profile": "link_lifetime_v1",
            "initial": initial, "steps": steps, "final": _snapshot(catalog, names, references)}


def evaluate(request):
    """Validate exact builtin declarations, then replay with detached pure states.

    All common fields precede exclusions/replay. Invalid traces expose no prefix;
    supplied truth and actual deletion/erase/durability/permissions are unverified.
    """
    try:
        data, unsupported = _validated(request)
        if unsupported:
            return {**_outcome("unsupported", "outside_subset"), "unsupported_reasons": unsupported}
        return _run(data)
    except _Invalid as failure:
        return _outcome(failure.status, failure.reason)

def _depth(text: str) -> None:
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                raise _Invalid("depth_limit", "over_limit")
        elif char in "]}":
            depth -= 1


def _unique(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise _Invalid("duplicate_key")
        result[key] = value
    return result


def _integer(token: str) -> int:
    if len(token) > MAX_NUMERIC_CHARS:
        raise _Invalid("numeric_token_limit", "over_limit")
    return int(token)


def _reject_number(token: str) -> None:
    if len(token) > MAX_NUMERIC_CHARS:
        raise _Invalid("numeric_token_limit", "over_limit")
    raise _Invalid("non_integer_number")


def analyze_json(raw: object) -> dict:
    """Strict UTF8 exact bytes, capped before JSON decoding, to bounded model report."""
    if type(raw) is not bytes:
        return _outcome("rejected", "input_type")
    if len(raw) > MAX_INPUT_BYTES:
        return _outcome("over_limit", "input_limit")
    try:
        text = raw.decode("utf-8", errors="strict")
        _depth(text)
        return evaluate(json.loads(text, object_pairs_hook=_unique, parse_int=_integer,
                                   parse_float=_reject_number, parse_constant=_reject_number))
    except _Invalid as error:
        return _outcome(error.status, error.reason)
    except (UnicodeError, ValueError, RecursionError):
        return _outcome("rejected", "invalid_json_or_utf8")


def serialize_report(report: dict) -> bytes:
    """Serialize trusted internally constructed reports; oversized fallback is incomplete.

    This is not an arbitrary-object public ingestion API. Accepted bounded reports
    cannot reach the cap; tests use labeled trusted oversized formatter seams.
    """
    def encode(value):
        return json.dumps(value, ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode("utf-8") + b"\n"
    encoded = encode(report)
    if len(encoded) > MAX_OUTPUT_BYTES:
        encoded = encode(_outcome("over_limit", "output_limit"))
        if len(encoded) > MAX_OUTPUT_BYTES:
            raise ValueError("trusted output budget smaller than fallback")
    return encoded
