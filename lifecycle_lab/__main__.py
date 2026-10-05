"""Checked bounded stdin/report/demo/help delivery, without filesystem actions."""
import argparse
import json
import sys

from .core import MAX_INPUT_BYTES, analyze_json, evaluate, serialize_report
from .fixtures import oracles

HELP = "usage: lifecycle_lab {analyze,demo}\n\nSupplied lifetime trace; actual deletion/reclaim unverified.\n\nanalyze: bounded UTF8 JSON stdin\ndemo: twenty-two frozen reports\n--help: fixed usage\n"


def _text(destination, message):
    if destination is None:
        raise OSError("absent output stream")
    count = destination.write(message)
    if type(count) is not int or count != len(message):
        raise OSError("invalid text write count")
    destination.flush()


class _CheckedParser(argparse.ArgumentParser):
    def print_help(self, file=None):
        _text(sys.stdout if file is None else file, HELP)

    def error(self, message):
        _text(sys.stderr, '{"error":"invalid_arguments"}\n')
        raise SystemExit(2)


def _io_failure():
    diagnostic = sys.stderr
    # Stop dirty public sinks from overriding exit3 during CPython shutdown.
    sys.stdout = sys.stderr = None
    try:
        _text(diagnostic, '{"error":"input_or_output_failure"}\n')
    except (OSError, ValueError):
        pass
    return 3


def main():
    parser = _CheckedParser(prog="lifecycle_lab")
    parser.add_argument("command", choices=("analyze", "demo"))
    try:
        args = parser.parse_args()
        if args.command == "analyze":
            if sys.stdin is None:
                raise OSError("absent input stream")
            report = analyze_json(sys.stdin.buffer.read(MAX_INPUT_BYTES + 1))
        else:
            cases = []
            for fixture in oracles():
                result = evaluate(fixture["request"])
                cases.append({"report": result, "expected": fixture["expected"], "passed": result == fixture["expected"]})
            report = {"mode": "invented_lifetime_trace", "actual_deletion": "unverified",
                      "storage_reclaimed": "unverified", "cases": cases, "passed": all(case["passed"] for case in cases)}
        payload = serialize_report(report)
        emitted = json.loads(payload)
        if sys.stdout is None:
            raise OSError("absent report sink")
        count = sys.stdout.buffer.write(payload)
        if type(count) is not int or count != len(payload):
            raise OSError("invalid report write count")
        sys.stdout.buffer.flush()
    except (OSError, ValueError):
        return _io_failure()
    if emitted.get("status") == "over_limit":
        return 2
    if args.command == "demo":
        return 0 if report["passed"] else 1
    return 0 if report["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
