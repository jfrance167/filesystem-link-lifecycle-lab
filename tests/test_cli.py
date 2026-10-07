"""Bounded in-memory CLI control-flow and delivery seams."""
from io import BytesIO, StringIO
import json
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from lifecycle_lab.__main__ import main
from lifecycle_lab.core import MAX_INPUT_BYTES
from lifecycle_lab.fixtures import oracles


class CliTests(unittest.TestCase):
    def invoke(self, raw=b"{}", command="analyze", output=None, reader=None, errors=None):
        output = BytesIO() if output is None else output
        errors = StringIO() if errors is None else errors
        with patch("sys.argv", ["lifecycle_lab", command]), \
             patch("sys.stdin", SimpleNamespace(buffer=BytesIO(raw) if reader is None else reader)), \
             patch("sys.stdout", SimpleNamespace(buffer=output)), patch("sys.stderr", errors):
            code = main()
        return code, output, errors

    def test_outcomes_and_full_demo(self):
        for index, expected in ((0, 0), (12, 2)):
            fixture = oracles()[index]
            code, out, err = self.invoke(json.dumps(fixture["request"]).encode())
            self.assertEqual(code, expected)
            self.assertEqual(json.loads(out.getvalue()), fixture["expected"])
            self.assertEqual(err.getvalue(), "")
        value = oracles()[0]["request"]
        value["context"]["reference_coverage"] = "unknown"
        self.assertEqual(self.invoke(json.dumps(value).encode())[0], 2)
        for raw in (b"invalid", b"x"*(MAX_INPUT_BYTES+1)):
            self.assertEqual(self.invoke(raw)[0], 2)
        code, out, _ = self.invoke(command="demo")
        demo = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertTrue(demo["passed"])
        self.assertEqual(len(demo["cases"]), 22)
        self.assertEqual([case["report"] for case in demo["cases"]], [case["expected"] for case in oracles()])
        with patch("lifecycle_lab.__main__.evaluate", return_value={"trusted_seam":"wrong"}):
            self.assertEqual(self.invoke(command="demo")[0], 1)

    def test_bounded_read_and_output_limit_exit(self):
        class Reader:
            def read(self, size):
                self.size = size
                return b"x"*size
        reader = Reader()
        self.assertEqual(self.invoke(reader=reader)[0], 2)
        self.assertEqual(reader.size, MAX_INPUT_BYTES+1)
        with patch("lifecycle_lab.__main__.serialize_report", return_value=b'{"status":"over_limit","complete":false}\n'):
            self.assertEqual(self.invoke()[0], 2)
            self.assertEqual(self.invoke(command="demo")[0], 2)

    def test_read_write_flush_short_and_closed_failures(self):
        class Reader:
            def read(self, size):
                raise OSError("synthetic")
        class Write(BytesIO):
            def write(self, data):
                raise BrokenPipeError("synthetic")
        class Flush(BytesIO):
            def flush(self):
                raise OSError("synthetic")
        class Short(BytesIO):
            def write(self, data):
                return 0
        closed = BytesIO()
        closed.close()
        self.assertEqual(self.invoke(reader=Reader())[0], 3)
        for output in (Write(), Flush(), Short(), closed):
            code, _, errors = self.invoke(output=output)
            self.assertEqual(code, 3)
            self.assertEqual(json.loads(errors.getvalue()), {"error":"input_or_output_failure"})

    def test_parser_fixed_error_no_reflection(self):
        errors = StringIO()
        with patch("sys.argv", ["lifecycle_lab", "\x1bsecret\n"]), patch("sys.stderr", errors):
            with self.assertRaises(SystemExit) as raised:
                main()
        self.assertEqual(raised.exception.code, 2)
        self.assertEqual(errors.getvalue(), '{"error":"invalid_arguments"}\n')

    def test_exact_integer_binary_and_text_write_counts(self):
        calls=[]
        class Count(int):
            def __eq__(self, other):
                calls.append("equal"); raise AssertionError("untrusted equality")
        values=(lambda size: float(size), lambda size: True, lambda size: None, lambda size: Count(size))
        for value in values:
            class Binary(BytesIO):
                def write(self, data):
                    return value(len(data))
            self.assertEqual(self.invoke(output=Binary())[0],3)
            class Text(StringIO):
                def write(self, message):
                    return value(len(message))
            for argv,field in ((["--help"],"stdout"),(["invalid"],"stderr")):
                original_stdout,original_stderr=sys.stdout,sys.stderr
                with patch("sys.argv",["lifecycle_lab",*argv]), \
                     patch("sys.stdout",Text() if field=="stdout" else StringIO()), \
                     patch("sys.stderr",Text() if field=="stderr" else StringIO()):
                    self.assertEqual(main(),3)
                self.assertIs(sys.stdout,original_stdout)
                self.assertIs(sys.stderr,original_stderr)
        self.assertEqual(calls,[])

    def test_absent_and_dirty_public_sinks(self):
        class Short(StringIO):
            def write(self, text):
                return 0
        class Flush(StringIO):
            def flush(self):
                raise OSError("synthetic dirty diagnostic")
        for sink in (None, Short(), Flush()):
            with patch("sys.argv", ["lifecycle_lab", "invalid"]), patch("sys.stderr", sink), patch("sys.stdout", None):
                self.assertEqual(main(), 3)
                self.assertIsNone(sys.stdout)
                self.assertIsNone(sys.stderr)
        with patch("sys.argv", ["lifecycle_lab", "analyze"]), patch("sys.stdin", None), patch("sys.stderr", None):
            with patch("sys.stdout", None):
                self.assertEqual(main(), 3)


if __name__ == "__main__":
    unittest.main()
