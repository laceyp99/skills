"""Regression checks for locale-independent skill authoring and expected I/O failures."""

import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import generate_openai_yaml as generator
import init_skill as initializer
import quick_validate as validator


@contextlib.contextmanager
def non_utf8_default():
    """Make omitted file encodings use cp1252 on every test host."""
    original_open = io.open

    def locale_open(file, mode="r", buffering=-1, encoding=None, *args, **kwargs):
        if "b" not in mode and encoding is None:
            encoding = "cp1252"
        return original_open(file, mode, buffering, encoding, *args, **kwargs)

    with mock.patch("io.open", side_effect=locale_open):
        yield


class AuthoringScriptsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "sample-skill"
        self.skill.mkdir()
        self.skill_md = self.skill / "SKILL.md"
        self.output = io.StringIO()
        capture = contextlib.redirect_stdout(self.output)
        capture.__enter__()
        self.addCleanup(capture.__exit__, None, None, None)

    def write_skill(self, description="Example skill", body="Instructions."):
        self.skill_md.write_text(
            f"---\nname: sample-skill\ndescription: {description}\n---\n{body}\n",
            encoding="utf-8",
        )

    def run_cli(self, script, *args):
        env = os.environ.copy()
        env["PYTHONUTF8"] = "0"
        # Console capture is independent of the file-encoding behavior under test.
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8=0", str(SCRIPTS / script), *map(str, args)],
            capture_output=True, encoding="utf-8", env=env,
        )

    def assert_cli_error(self, script, message, *args):
        result = self.run_cli(script, *args)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_validation_with_ascii_and_unicode_under_non_utf8_default(self):
        for text in ("ASCII control", "Café — 你好 丁"):
            with self.subTest(text=text):
                self.write_skill(text, text)
                with non_utf8_default():
                    if not text.isascii():
                        with self.assertRaises(UnicodeDecodeError):
                            self.skill_md.read_text()
                    self.assertEqual(validator.validate_skill(self.skill), (True, "Skill is valid!"))
                    self.assertEqual(generator.read_frontmatter_name(self.skill), "sample-skill")
                result = self.run_cli("quick_validate.py", self.skill)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generated_unicode_metadata_round_trips(self):
        self.write_skill("Café 你好")
        values = {
            "display_name": "Café 你好",
            "short_description": "Helpful guidance for café workflows",
            "default_prompt": "Explain 你好 and café",
        }
        with non_utf8_default():
            path = generator.write_openai_yaml(
                self.skill, generator.read_frontmatter_name(self.skill),
                [f"{key}={value}" for key, value in values.items()],
            )
        self.assertIsNotNone(path)
        self.assertEqual(yaml.safe_load(path.read_bytes().decode("utf-8"))["interface"], values)
        result = self.run_cli(
            "generate_openai_yaml.py", self.skill,
            "--interface", f"display_name={values['display_name']}",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        metadata = yaml.safe_load(path.read_bytes().decode("utf-8"))
        self.assertEqual(metadata["interface"]["display_name"], values["display_name"])

    def test_scaffold_and_all_examples_use_utf8(self):
        text = "\nCafé 你好\n"
        with non_utf8_default(), mock.patch.object(
            initializer, "SKILL_TEMPLATE", initializer.SKILL_TEMPLATE + text
        ), mock.patch.object(
            initializer, "EXAMPLE_SCRIPT", initializer.EXAMPLE_SCRIPT + text
        ), mock.patch.object(
            initializer, "EXAMPLE_REFERENCE", initializer.EXAMPLE_REFERENCE + text
        ), mock.patch.object(
            initializer, "EXAMPLE_ASSET", initializer.EXAMPLE_ASSET + text
        ):
            skill = initializer.init_skill(
                "new-skill", self.root, ["scripts", "references", "assets"], True,
                ["display_name=Café 你好"],
            )
        self.assertIsNotNone(skill)
        for relative in ("SKILL.md", "scripts/example.py", "references/api_reference.md", "assets/example_asset.txt"):
            self.assertIn(text.strip(), (skill / relative).read_bytes().decode("utf-8"))
        metadata = yaml.safe_load((skill / "agents/openai.yaml").read_bytes().decode("utf-8"))
        self.assertEqual(metadata["interface"]["display_name"], "Café 你好")
        result = self.run_cli(
            "init_skill.py", "cli-skill", "--path", self.root,
            "--resources", "scripts,references,assets", "--examples",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("\u2014", (self.root / "cli-skill/SKILL.md").read_bytes().decode("utf-8"))

    def test_invalid_utf8_has_decode_specific_errors(self):
        self.skill_md.write_bytes(b"\xff")
        valid, message = validator.validate_skill(self.skill)
        self.assertFalse(valid)
        self.assertIn("not valid UTF-8", message)
        self.assertIsNone(generator.read_frontmatter_name(self.skill))
        self.assertIn("not valid UTF-8", self.output.getvalue())
        for script in ("quick_validate.py", "generate_openai_yaml.py"):
            self.assert_cli_error(script, "not valid UTF-8", self.skill)

    def test_unreadable_input_has_io_specific_errors(self):
        self.write_skill()
        with mock.patch.object(Path, "read_text", side_effect=PermissionError("access denied")):
            valid, message = validator.validate_skill(self.skill)
            self.assertFalse(valid)
            self.assertIn("Could not read SKILL.md", message)
            self.assertIsNone(generator.read_frontmatter_name(self.skill))
        self.assertIn("Could not read SKILL.md", self.output.getvalue())

    def test_cli_input_io_errors_do_not_traceback(self):
        self.skill_md.mkdir()
        for script in ("quick_validate.py", "generate_openai_yaml.py"):
            self.assert_cli_error(script, "Could not read SKILL.md", self.skill)

    def test_content_validation_errors_remain_distinct(self):
        cases = (
            ("No frontmatter", "No YAML frontmatter", "Invalid SKILL.md frontmatter"),
            ("---\nname: [\n---\n", "Invalid YAML", "Invalid YAML"),
            ("---\nname: 123\ndescription: Example\n---\n", "Name must be a string", "'name' is missing or invalid"),
        )
        for content, validator_message, generator_message in cases:
            with self.subTest(content=content):
                self.skill_md.write_text(content, encoding="utf-8")
                valid, message = validator.validate_skill(self.skill)
                self.assertFalse(valid)
                self.assertIn(validator_message, message)
                self.assert_cli_error("quick_validate.py", validator_message, self.skill)
                self.assert_cli_error("generate_openai_yaml.py", generator_message, self.skill)

    def test_missing_input_retains_missing_file_message(self):
        self.assertEqual(validator.validate_skill(self.skill), (False, "SKILL.md not found"))
        for script in ("quick_validate.py", "generate_openai_yaml.py"):
            self.assert_cli_error(script, "SKILL.md not found", self.skill)

    def test_generator_handles_directory_and_output_write_errors(self):
        self.write_skill()
        agents = self.skill / "agents"
        agents.write_text("blocks directory creation", encoding="utf-8")
        self.assert_cli_error("generate_openai_yaml.py", "Could not create agents/openai.yaml", self.skill)
        agents.unlink()
        agents.mkdir()
        (agents / "openai.yaml").mkdir()
        self.assert_cli_error("generate_openai_yaml.py", "Could not create agents/openai.yaml", self.skill)
        with mock.patch.object(Path, "write_text", side_effect=PermissionError("access denied")):
            self.assertIsNone(generator.write_openai_yaml(self.skill, "sample-skill", []))

    def test_initializer_handles_io_errors(self):
        blocked = self.root / "blocked"
        blocked.write_text("blocks directory creation", encoding="utf-8")
        self.assert_cli_error("init_skill.py", "Error creating directory", "new-skill", "--path", blocked)
        with mock.patch.object(Path, "write_text", side_effect=PermissionError("access denied")):
            self.assertIsNone(initializer.init_skill("new-skill", self.root, [], False, []))
        self.assertIn("Error creating SKILL.md", self.output.getvalue())
        with mock.patch.object(initializer, "create_resource_dirs", side_effect=PermissionError("access denied")):
            self.assertIsNone(initializer.init_skill("resource-skill", self.root, ["scripts"], True, []))
        self.assertIn("Error creating resource directories", self.output.getvalue())

    def test_programming_errors_are_not_hidden(self):
        self.write_skill()
        with mock.patch.object(Path, "read_text", side_effect=RuntimeError("bug")):
            for function in (validator.validate_skill, generator.read_frontmatter_name):
                with self.assertRaises(RuntimeError):
                    function(self.skill)
        with mock.patch.object(initializer, "write_openai_yaml", side_effect=RuntimeError("bug")):
            with self.assertRaises(RuntimeError):
                initializer.init_skill("new-skill", self.root, [], False, [])


if __name__ == "__main__":
    unittest.main()
