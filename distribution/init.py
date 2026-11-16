"""Personalize a fresh fork locally. Does not create, push or publish anything."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = "Cha0sCollective/Packwiz-Template"


def initialize(root, repository, name, pack_id, author):
    if not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", repository):
        raise ValueError("Use a GitHub owner/repository.")
    if repository.lower() == TEMPLATE.lower():
        raise ValueError("Choose your own repository, not the upstream template.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", pack_id):
        raise ValueError("Use letters, digits, underscores and hyphens for --id.")
    if any(not s.strip() or any(ord(c) < 32 for c in s) for s in (name, author)):
        raise ValueError("Name and author must be nonempty single-line text.")
    packwiz = shutil.which("packwiz")
    if not packwiz:
        raise ValueError("Install packwiz and put it on PATH before initialization.")
    settings_path = root / "distribution/repository.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    # An already-configured fork may be forked again before its first release.
    if not settings.get("template") and settings["repository"].lower() == repository.lower():
        raise ValueError("This repository is already initialized. Edit its metadata normally.")
    pack_path = root / "pack/pack.toml"
    text = pack_path.read_text(encoding="utf-8")
    for key, value in (("name", name), ("author", author)):
        text, count = re.subn(rf'(?m)^{key} = "[^\r\n]*"$', lambda _: f'{key} = {json.dumps(value, ensure_ascii=False)}', text)
        if count != 1:
            raise ValueError(f"Expected one {key} in pack/pack.toml.")
    parsed = tomllib.loads(text)
    profile_path = root / "distribution/profile.json"
    paths = (settings_path, profile_path, pack_path, root / "pack/index.toml")
    previous = {p: p.read_bytes() for p in paths}
    try:
        settings.update(repository=repository, template=False)
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8", newline="\n")
        profile_path.write_text(json.dumps({"id": pack_id, "name": name, "version": parsed["version"]}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        pack_path.write_text(text, encoding="utf-8", newline="\n")
        subprocess.run([packwiz, "refresh"], cwd=root / "pack", check=True)
    except Exception:
        for path, content in previous.items():
            path.write_bytes(content)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True, help="Your GitHub owner/repository")
    parser.add_argument("--name", required=True, help="Display name")
    parser.add_argument("--id", required=True, help="Permanent filename and Prism identity, e.g. My-Pack")
    parser.add_argument("--author", required=True)
    args = parser.parse_args()
    initialize(ROOT, args.repository, args.name, args.id, args.author)
    print("Personalized locally. Review and commit the changes, then follow docs/SETUP.md.")


if __name__ == "__main__":
    main()
