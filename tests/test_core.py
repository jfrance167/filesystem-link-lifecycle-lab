"""Frozen reports, independent remaining-label oracle, admission and pure effects."""
from copy import deepcopy
from contextlib import ExitStack
import builtins
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import unittest
from unittest.mock import patch

from lifecycle_lab import core
from lifecycle_lab.fixtures import oracles

ROOT = Path(__file__).resolve().parents[1]


def request():
    return oracles()[0]["request"]


def event(op, **fields):
    return {"id":"Event", "op":op, **fields}


class CoreTests(unittest.TestCase):
    def incomplete(self, value, status="rejected", reason=None):
        result = core.evaluate(value)
        self.assertEqual(result["status"], status)
        self.assertFalse(result["complete"])
        if reason:
            self.assertEqual(result["reason"], reason)
        for field in ("initial", "steps", "final"):
            self.assertNotIn(field, result)
        return result

    def test_frozen_full_reports(self):
        freeze = json.loads((ROOT/"research/oracle-freeze.json").read_bytes())
        self.assertEqual(freeze["application_files"], [])
        for path, digest in freeze["files_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest)
        fixed = json.loads((ROOT/"fixtures/oracles.json").read_bytes())
        self.assertEqual(fixed, oracles())
        self.assertEqual(len(fixed), 22)
        for fixture in fixed:
            with self.subTest(id=fixture["request"]["id"]):
                self.assertEqual(core.evaluate(fixture["request"]), fixture["expected"])
                self.assertEqual(core.analyze_json(json.dumps(fixture["request"]).encode()), fixture["expected"])

    def test_independent_32_traces_150_snapshots(self):
        domain = json.loads((ROOT/"fixtures/domain.json").read_bytes())
        self.assertEqual(len(domain), 32)
        total = 0
        for fixture in domain:
            self.assertEqual(core.evaluate(fixture["request"]), fixture["expected"])
            total += 1+len(fixture["expected"]["steps"])
        self.assertEqual(total, 150)

    def test_open_retention_regression(self):
        self.assertEqual(core.evaluate(oracles()[4]["request"]), oracles()[4]["expected"])

    def test_one_name_regression(self):
        self.assertEqual(core.evaluate(oracles()[2]["request"]), oracles()[2]["expected"])

    def test_one_reference_regression(self):
        self.assertEqual(core.evaluate(oracles()[7]["request"]), oracles()[7]["expected"])

    def test_rebind_regression(self):
        self.assertEqual(core.evaluate(oracles()[9]["request"]), oracles()[9]["expected"])

    def test_detached_snapshots_input_and_order(self):
        value = oracles()[9]["request"]
        before = deepcopy(value)
        result = core.evaluate(value)
        self.assertEqual(value, before)
        result["final"]["files"][0]["id"] = "Changed"
        result["steps"][0]["state"]["names"].clear()
        self.assertEqual(result["initial"], oracles()[9]["expected"]["initial"])
        self.assertEqual(result["steps"][1], oracles()[9]["expected"]["steps"][1])
        self.assertEqual(core.evaluate(value), oracles()[9]["expected"])
        reordered = deepcopy(value)
        for field in ("files", "names", "references"):
            reordered[field].reverse()
        self.assertEqual(core.evaluate(reordered), core.evaluate(value))

    def test_owned_reference_history_and_preconditions(self):
        for i in range(12, 17):
            self.assertEqual(core.evaluate(oracles()[i]["request"]), oracles()[i]["expected"])
        value = request()
        value["events"] = [event("link", source_name="Missing", new_name="A")]
        self.assertEqual(self.incomplete(value)["violation"], "missing_name")
        value["references"] = [{"id":"R", "file_id":"F"}]
        value["events"] = [event("open", name="Missing", reference_id="R")]
        self.assertEqual(self.incomplete(value)["violation"], "missing_name")

    def test_common_validation_before_exclusions_and_replay(self):
        for gate in ("version", "profile", "context", "kind", "operation", "transition"):
            value = request()
            if gate == "version": value["version"] = 2
            if gate == "profile": value["profile"] = "Future"
            if gate == "context": value["context"]["reference_coverage"] = "partial"
            if gate == "kind": value["files"][0]["kind"] = "directory"
            value["events"] = [event("rename" if gate == "operation" else "unlink", **({"source_name":"A", "new_name":"B"} if gate == "operation" else {"name":"Missing"})),
                               {"id":"Late", "op":"close", "reference_id":True}]
            self.incomplete(value, reason="identifier")
        value = request()
        value["version"] = 2
        value["names"][0]["file_id"] = "Absent"
        self.incomplete(value, reason="unknown_file")

    def test_known_unsupported_and_unknown_enums(self):
        value = request()
        for field, choices in core.CONTEXT.items():
            for declaration in choices[1:]:
                value = request(); value["context"][field] = declaration
                self.incomplete(value, "unsupported")
            value["context"][field] = "invalid"
            self.incomplete(value, reason="enum")
        for feature in core.FEATURES:
            value = request(); value["context"]["excluded_features"] = [feature]
            self.incomplete(value, "unsupported")
        for kind in ("directory", "symlink", "other", "unknown"):
            value = request(); value["files"][0]["kind"] = kind
            self.incomplete(value, "unsupported")
        for op, fields in (("rename", {"source_name":"A", "new_name":"B"}),
                           ("replace", {"source_name":"A", "new_name":"B"}),
                           ("link_from_reference", {"reference_id":"R", "new_name":"B"})):
            value=request(); value["events"]=[event(op, **fields)]
            self.incomplete(value, "unsupported")
        value=request(); value["events"]=[event("unknown")]
        self.incomplete(value, reason="enum")

    def test_identity_metaclass_keys_and_subclass_rejection_without_hooks(self):
        calls=[]
        class Meta(type):
            def __eq__(cls, other):
                calls.append("meta_equal"); raise AssertionError("hook")
            def __hash__(cls):
                calls.append("meta_hash"); raise AssertionError("hook")
        class Mapping(dict, metaclass=Meta):
            def __len__(self):
                calls.append("len"); raise AssertionError("hook")
            def __iter__(self):
                calls.append("iter"); raise AssertionError("hook")
        class Number(int, metaclass=Meta):
            def __le__(self, other):
                calls.append("number"); raise AssertionError("hook")
        class Text(str, metaclass=Meta):
            def __eq__(self, other):
                calls.append("text"); raise AssertionError("hook")
        class Sequence(list, metaclass=Meta):
            def __iter__(self):
                calls.append("iter"); raise AssertionError("hook")
        self.incomplete(Mapping(request()))
        value=request(); value["version"]=Number(1); self.incomplete(value)
        value=request(); value["id"]=Text("Case"); self.incomplete(value)
        value=request(); value["files"]=Sequence([]); self.incomplete(value)
        value=request(); value["events"]=[Mapping(event("unlink", name="A"))]; self.incomplete(value)
        value=request(); value["events"]=[event(Text("unlink"), name="A")]; self.incomplete(value)
        active=False
        class Key(str):
            def __hash__(self):
                if active: raise AssertionError("key_hash")
                return str.__hash__(self)
            def __eq__(self, other):
                if active: raise AssertionError("key_equal")
                return str.__eq__(self, other)
        value=request(); value[Key("other")]=value.pop("id"); active=True
        self.incomplete(value, reason="object_shape")
        self.assertEqual(calls, [])

    def test_alias_occurrences_cycles_and_identity_relationships(self):
        value=request(); value["references"]=value["names"]
        result=core.evaluate(value)
        self.assertEqual(result["initial"]["files"][0]["retention_basis"], "names_and_references")
        value=request(); value["names"].append(value["names"][0])
        self.incomplete(value, reason="duplicate_identity")
        value=request(); value["references"]=value["names"]
        value["names"][0]["file_id"]=True
        self.incomplete(value, reason="identifier")
        value=request(); value["names"][0]["file_id"]=value
        self.incomplete(value)
        value=request(); value["events"].append(value["events"])
        self.incomplete(value)
        value=request(); value["context"]["excluded_features"].append(value["context"]["excluded_features"])
        self.incomplete(value)

    def test_cardinality_identifiers_and_numeric_boundaries(self):
        for field, maximum in (("files",4),("names",8),("references",8),("events",24)):
            value=request(); value[field]=[None]*(maximum+1)
            self.incomplete(value,"over_limit","list_limit")
        value=request(); value["context"]["excluded_features"]=["dup"]*17
        self.incomplete(value,"over_limit","list_limit")
        value=request(); value["context"]["excluded_features"]=["dup","dup"]
        self.incomplete(value,reason="duplicate_feature")
        for bad in (True,-1,1000000000,1.5,"1",None):
            value=request(); value["version"]=bad; self.incomplete(value,reason="integer_range")
        for bad in ("", "x"*25, "Bad\n", "é", "\ud800"):
            value=request(); value["id"]=bad; self.incomplete(value,reason="identifier")
        value=request(); value["events"]=[{"id":f"E{i}","op":"link","source_name":"A","new_name":f"N{i}"} for i in range(8)]
        self.incomplete(value,"over_limit","identifier_count_limit")
        value=request(); value["events"]=[{"id":f"E{i}","op":"open","name":"A","reference_id":f"R{i}"} for i in range(9)]
        self.incomplete(value,"over_limit","identifier_count_limit")
        value=request(); value["x"*10000]=value.pop("id"); self.incomplete(value,reason="object_shape")

    def test_strict_json_and_lexical_depth(self):
        raw=json.dumps(request()).encode()
        exact=raw+b" "*(core.MAX_INPUT_BYTES-len(raw))
        self.assertTrue(core.analyze_json(exact)["complete"])
        self.assertEqual(core.analyze_json(exact+b" ")["reason"],"input_limit")
        for raw,reason in ((b"["*7+b"0"+b"]"*7,"depth_limit"),
                           (b"["*6+b"0"+b"]"*6,"object_shape"),
                           (b'{"x":"[[[[[[["}',"object_shape"),
                           (b'{"x":10000000000}',"numeric_token_limit"),
                           (b'{"x":1.5}',"non_integer_number"),
                           (b'{"x":Infinity}',"non_integer_number"),
                           (b'{"x":1,"x":2}',"duplicate_key"),
                           (b'\xff',"invalid_json_or_utf8")):
            self.assertEqual(core.analyze_json(raw)["reason"],reason)
        for bad in ("{}",bytearray(b"{}"),memoryview(b"{}")):
            self.assertEqual(core.analyze_json(bad)["reason"],"input_type")

    def test_formatter_trusted_seams(self):
        base=len(core.serialize_report({"x":""}))
        self.assertEqual(len(core.serialize_report({"x":"a"*(core.MAX_OUTPUT_BYTES-base)})),core.MAX_OUTPUT_BYTES)
        report=json.loads(core.serialize_report({"x":"a"*(core.MAX_OUTPUT_BYTES-base+1)}))
        self.assertEqual(report["reason"],"output_limit")
        self.assertNotIn("final",report)
        self.assertIn(b"\\u001b",core.serialize_report({"trusted":"\x1b"}))
        with patch.object(core,"MAX_OUTPUT_BYTES",1):
            with self.assertRaises(ValueError): core.serialize_report({"x":"y"})

    def test_core_no_host_effects(self):
        value=oracles()[9]["request"]
        with ExitStack() as guards:
            for module,name in ((builtins,"open"),(builtins,"eval"),(builtins,"exec"),(os,"remove"),(os,"unlink"),
                                (os,"link"),(os,"rename"),(os,"stat"),(os,"open"),(os,"chmod"),(os,"system"),
                                (subprocess,"Popen"),(socket,"socket")):
                guards.enter_context(patch.object(module,name,side_effect=AssertionError("forbidden host capability")))
            self.assertTrue(core.evaluate(value)["complete"])
            self.assertTrue(core.analyze_json(json.dumps(value).encode())["complete"])
            self.assertTrue(core.serialize_report(core.evaluate(value)).endswith(b"\n"))

    def test_admitted_max_shape_and_bound(self):
        import sys
        with patch.object(sys,"path",[str(ROOT/"tools"),*sys.path]):
            from measure_report import stress_request
        value=stress_request()
        before=deepcopy(value)
        result=core.evaluate(value)
        self.assertTrue(result["complete"])
        self.assertEqual(value,before)
        self.assertEqual((len(value["files"]),len(value["names"]),len(value["references"]),len(value["events"])),(4,8,8,24))
        self.assertEqual(len(result["steps"]),24)
        self.assertEqual(result["initial"]["references"],result["final"]["references"])
        self.assertLess(len(core.serialize_report(result)),163840)
        self.assertLess(163840,core.MAX_OUTPUT_BYTES)


if __name__ == "__main__":
    unittest.main()
