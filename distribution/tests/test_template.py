"""Fork isolation and first-release behavior, without external services."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import release as r

spec = importlib.util.spec_from_file_location("pack_init", r.ROOT / "distribution/init.py")
initializer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initializer)


class ForkTests(unittest.TestCase):
    def copy_pack(self, root):
        for folder in ("pack", "distribution"):
            shutil.copytree(r.ROOT / folder, root / folder,
                            ignore=shutil.ignore_patterns("__pycache__", "tests"))

    def test_template_cannot_publish(self):
        with patch.object(r, "SETTINGS", {"template": True}), patch.object(r, "git") as git:
            with self.assertRaisesRegex(ValueError, "init.py"):
                r.require_configured()
            git.assert_not_called()

    def test_fork_cannot_publish_to_inherited_repository(self):
        with patch.object(r, "SETTINGS", {"template": False}), patch.dict(os.environ, {"GITHUB_REPOSITORY": "another/pack"}):
            with self.assertRaisesRegex(ValueError, "another repository"):
                r.require_configured()

    def test_origin_must_match_target(self):
        with patch.object(r, "SETTINGS", {"template": False}), patch.dict(os.environ, {"GITHUB_REPOSITORY": r.REPO}):
            for origin in ("https://github.com/other/pack.git", "https://example.com/" + r.REPO):
                with patch.object(r, "git", return_value=origin), self.assertRaisesRegex(ValueError, "origin"):
                    r.require_configured()
            for origin in (f"https://github.com/{r.REPO}.git", f"git@github.com:{r.REPO}.git"):
                with patch.object(r, "git", return_value=origin):
                    r.require_configured()

    def test_initializer_personalizes_without_upstream_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_pack(root)
            with patch.object(initializer.shutil, "which", return_value="packwiz"), patch.object(initializer.subprocess, "run") as run:
                initializer.initialize(root, "new-owner/new-pack", 'My "quoted" Pack', "My-Pack", "A Builder")
                run.assert_called_once_with(["packwiz", "refresh"], cwd=root / "pack", check=True)
            settings = json.loads((root / "distribution/repository.json").read_text())
            self.assertEqual(settings, {"repository": "new-owner/new-pack", "template": False})
            self.assertEqual(r.validate(root, aligned=True)["name"], 'My "quoted" Pack')
            self.assertEqual(json.loads((root / "distribution/profile.json").read_text())["id"], "My-Pack")

    def test_initializer_rolls_back_if_refresh_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.copy_pack(root)
            names = ("distribution/repository.json", "distribution/profile.json", "pack/pack.toml", "pack/index.toml")
            before = {n: (root / n).read_bytes() for n in names}
            with patch.object(initializer.shutil, "which", return_value="packwiz"), patch.object(initializer.subprocess, "run", side_effect=RuntimeError("refresh failed")):
                with self.assertRaises(RuntimeError):
                    initializer.initialize(root, "new-owner/new-pack", "My Pack", "My-Pack", "Builder")
            self.assertEqual(before, {n: (root / n).read_bytes() for n in names})

    def test_initializer_rejects_upstream_and_unsafe_names(self):
        for repo, pack_id, name in ((initializer.TEMPLATE, "Pack", "Pack"), ("../pack", "Pack", "Pack"),
                                     ("owner/pack", "../pack", "Pack"), ("owner/pack", "Pack", "name\ncommand")):
            with self.assertRaises(ValueError):
                initializer.initialize(Path("unused"), repo, name, pack_id, "Builder")

    def test_first_release_needs_no_old_tags(self):
        with patch.object(r, "git", return_value=""):
            self.assertEqual(r.previous_release("public-sha"), (None, None))

    def test_existing_tags_require_matching_public_snapshot(self):
        def git(*args):
            if args[:1] == ("tag",):
                return "v0.1.0"
            return "pack/config/changed.toml"
        with patch.object(r, "git", side_effect=git), self.assertRaisesRegex(ValueError, "match a published fixed version"):
            r.previous_release("public-sha")

    def test_fixed_build_creates_no_local_tag(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(r, "git") as git, patch.object(r, "run") as run, patch.object(r, "inspect_zip"):
            r.build(Path(tmp), "v0.1.0", "a" * 40)
            git.assert_not_called()
            args = run.call_args.args
            self.assertIn("-SnapshotVersion", args)
            self.assertIn("a" * 40, args)

    def test_manifest_rejects_wrong_repository_and_missing_files(self):
        manifest = {"repository": "wrong/pack", "smoke_sha256": "wrong"}
        with self.assertRaisesRegex(ValueError, "repository or smoke"):
            r.check_manifest(Path("unused"), manifest)
        manifest.update(repository=r.REPO, smoke_sha256=r.digest(r.ROOT / "distribution/smoke.py"),
                        packaging="sha", version="0.1.0", files={})
        with patch.object(r, "git", return_value="sha"), self.assertRaisesRegex(ValueError, "artifacts"):
            r.check_manifest(Path("unused"), manifest)

    def test_pack_paths_cannot_escape(self):
        for name in ("../outside", "/absolute", "C:/outside", "..\\outside"):
            with self.assertRaises(ValueError):
                r.safe_file(r.ROOT, name)


@unittest.skipUnless(shutil.which("packwiz"), "Packwiz is required for the real first-release integration check")
class FirstReleaseIntegration(unittest.TestCase):
    def test_preparation_updates_only_beta_in_fresh_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            work = base / "pack"
            bare = base / "remote.git"
            shutil.copytree(r.ROOT, work, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            def git(*args, cwd=work):
                return r.run("git", *args, cwd=cwd)
            git("init", "--bare", str(bare))
            git("init", "-b", "public")
            git("config", "user.name", "Template Test")
            git("config", "user.email", "test@example.invalid")
            git("add", ".")
            git("commit", "-m", "fresh template")
            start = git("rev-parse", "HEAD")
            git("remote", "add", "origin", str(bare))
            git("push", "origin", "HEAD:public", "HEAD:main", "HEAD:beta")
            def remote(branch):
                return git("rev-parse", "refs/heads/" + branch, cwd=bare)
            env = {"protection_rules": [{"type": "required_reviewers", "prevent_self_review": False,
                                          "reviewers": [{"type": "User"}]}]}
            out = base / "prepared"
            with patch.object(r, "git", side_effect=git), patch.object(r, "remote", side_effect=remote), \
                    patch.object(r, "api", return_value=env), patch.object(r, "tag_sha", return_value=None), \
                    patch.object(r, "release", return_value=None), patch.dict(os.environ, {"GITHUB_OUTPUT": str(base / "outputs")}):
                r.prepare("0.1.1", out)
            manifest = json.loads((out / "release.json").read_text())
            self.assertIsNone(manifest["previous_tag"])
            self.assertEqual(remote("public"), start)
            self.assertEqual(remote("main"), start)
            self.assertEqual(remote("beta"), manifest["candidate"])
            self.assertNotEqual(manifest["candidate"], start)
            self.assertEqual(git("tag"), "")
            self.assertIn('version = "0.1.1"', git("show", manifest["candidate"] + ":pack/pack.toml"))
            self.assertEqual(json.loads(git("show", manifest["candidate"] + ":distribution/profile.json"))["version"], "0.1.1")


if __name__ == "__main__":
    unittest.main()
