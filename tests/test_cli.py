import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cli


class CliTests(unittest.TestCase):
    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_greet_default(self):
        code, out, _ = self.run_cli(["greet"])
        self.assertEqual(code, 0)
        self.assertIn("Hello, world", out)

    def test_greet_shout(self):
        code, out, _ = self.run_cli(["greet", "--name", "Victor", "--shout"])
        self.assertEqual(code, 0)
        self.assertIn("HELLO, VICTOR!", out)

    def test_env_greeting(self):
        with mock.patch.dict(os.environ, {"APP_GREETING": "Hola"}):
            code, out, _ = self.run_cli(["greet"])
        self.assertEqual(code, 0)
        self.assertIn("Hola, world", out)

    def test_config_file_overrides_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"greeting": "Bonjour", "repeat": 2}))
            code, out, _ = self.run_cli(["--config", str(path), "greet"])
        self.assertEqual(code, 0)
        self.assertEqual(out.count("Bonjour"), 2)

    def test_config_show(self):
        code, out, _ = self.run_cli(["config", "--show"])
        payload = json.loads(out)
        self.assertEqual(code, 0)
        self.assertIn("greeting", payload)

    def test_version(self):
        code, out, _ = self.run_cli(["version"])
        self.assertEqual(code, 0)
        self.assertIn(cli.VERSION, out)

    def test_invalid_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("{not json")
            code, _, err = self.run_cli(["--config", str(path), "greet"])
        self.assertEqual(code, 1)
        self.assertIn("config error", err)

    def test_missing_command_exits_2(self):
        with self.assertRaises(SystemExit) as ctx:
            self.run_cli([])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
