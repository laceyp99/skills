#!/usr/bin/env python3
"""Check that root skills, the README table, and plugin registration agree."""

import json
import re
import sys
from collections import Counter
from pathlib import Path


def check_catalog(root):
    expected = {path.parent.name for path in root.glob("*/SKILL.md")}
    errors = []
    try:
        manifest = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        paths = manifest["skills"]
        if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
            raise ValueError("skills must be an array of strings")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f"Plugin manifest: {error}")
        paths = []

    readme = (root / "README.md").read_text(encoding="utf-8")
    section = re.search(r"^## Included Skills\s*\n(.*?)(?=^## |\Z)", readme, re.M | re.S)
    if section is None:
        errors.append("README: Included Skills section is missing")
    names = re.findall(r"^\|\s*`([^`]+)`\s*\|", section.group(1) if section else "", re.M)

    for label, actual, wanted in (
        ("README Included Skills", names, expected),
        ("Plugin skills", paths, {f"./{name}" for name in expected}),
    ):
        counts = Counter(actual)
        for entry in sorted(wanted - counts.keys()):
            errors.append(f"{label}: missing {entry}")
        for entry in sorted(counts.keys() - wanted):
            errors.append(f"{label}: stale or invalid {entry}")
        for entry, count in sorted(counts.items()):
            if count > 1:
                errors.append(f"{label}: duplicate {entry}")
    return errors


def main():
    root = Path(__file__).resolve().parents[1]
    try:
        errors = check_catalog(root)
    except OSError as error:
        errors = [str(error)]
    if errors:
        print("Skill catalog check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Skill catalog check passed: README and plugin match all root skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
