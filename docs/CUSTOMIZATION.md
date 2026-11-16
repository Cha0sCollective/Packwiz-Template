# Customize the example

| File | Purpose |
| --- | --- |
| `pack/pack.toml` | Pack name, author, version, Minecraft and loader |
| `pack/index.toml` | Generated managed-file index; refresh with Packwiz |
| `pack/mods/` | Mod download metadata; starts empty |
| `pack/config/`, `pack/defaultconfigs/` | Maintained defaults |
| `pack/resourcepacks/` | Client resource-pack metadata |
| `distribution/repository.json` | Your GitHub owner/repository and template opt-out |
| `distribution/profile.json` | Permanent Prism/asset ID, display name and version |
| `distribution/runtime.json` | Matching Minecraft/NeoForge versions, Java and client memory in MiB |
| `distribution/prism-tools.json` | Pinned Packwiz tool downloads and SHA-256 hashes |
| `distribution/smoke.py` | Disposable server lifecycle and persistence checks |
| `.github/workflows/promote.yml` | Server image, test memory, approval and publication |
| `branding/icon.png` | Optional 512 × 512 PNG used as a per-channel Prism icon |

The initializer handles the name, author, ID and repository. After that, edit these files normally. Keep the repository identity and permanent ID consistent across public and beta. Packwiz, profile and optional `config/bcc-common.toml` version labels are aligned automatically during preparation; BCC is not required or bundled.

The default 6 GiB client maximum is an example, not a measurement of your eventual modpack's needs. Choose suitable client and server memory based on testing. The server workflow starts with a 4 GiB heap and 6 GiB container limit. Pin the server image by digest when you need a repeatable base; each test report records the image actually used.

The smoke test saves a chest, stone block, diamond items and a random scoreboard nonce, restarts the server, then checks persistence. You can add mod-specific assertions in `write_fixture` and `verify_fixture`. Keep verification separate from fixture creation so a broken reload cannot silently recreate the expected state.

Update Packwiz and GitHub action pins deliberately and test changes. The Packwiz CLI commit is recorded in `release.py` and pinned in `check.yml` and `promote.yml`; update all three together. Tool JARs are fetched from their pinned upstream release URLs and checked against `prism-tools.json`.

CH4OS branding, mod selections, mirrors, maps, server addresses, old release migrations and maintainer-specific agent profiles are intentionally absent. Attribution remains in [NOTICE.md](../NOTICE.md).
