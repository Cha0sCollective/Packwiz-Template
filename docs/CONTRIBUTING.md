# Contributing to your pack

Use `beta` or a focused branch based on beta. `pack/` is the source of truth for mod metadata, configuration, scripts, recipes and resource packs. Keep changes small enough to review.

Run from `pack/`:

```text
packwiz modrinth install <exact-version-URL>
packwiz curseforge install <exact-file-URL>
packwiz remove <mod-name>
packwiz refresh
```

Inspect dependencies and choose the correct client/server side. Use official downloads and retain required notices. Keep gameplay JARs, personal configurations, credentials, worlds, logs and launcher state out of Git. Empty directory README files are excluded from the distributed pack by `.packwizignore`.

Configuration defaults belong in `config/` or `defaultconfigs/`. Ordinary managed files can be replaced at launch; use Packwiz's `preserve = true` setting when existing player edits should survive. Do not assume updating `defaultconfigs/` rewrites existing world server configs.

Run `packwiz refresh` after any maintained file change. The committed files use LF bytes on both Windows and Linux because Packwiz hashes those bytes. From the repository root, validate with:

```text
python distribution/release.py validate
python -m unittest discover -s distribution/tests -v
```

Changing Minecraft, the loader, Java or memory requirements also affects `distribution/runtime.json`. This starter deliberately supports Minecraft 1.21.1 / NeoForge 21.1.x / Java 21. Extending that range requires adapting and testing `Build-Prism.ps1`, `release.py` and `smoke.py`.

Test affected gameplay in disposable instances. Hash validation and ZIP checks do not prove that Minecraft launched, that a client connected, or that an old world upgrades safely. Record the exact revision, checks performed and remaining limitations in the PR.

Push beta normally. Run the promotion workflow from public when ready; it captures and tests a single beta commit. Pull beta after preparation, since the workflow may align version labels in a new commit. Direct public pushes immediately affect players and bypass the release process. See [release operations](../distribution/README.md).
