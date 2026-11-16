# Run a dedicated server

Use Java 21, Minecraft 1.21.1 and the NeoForge version in `pack/pack.toml`. AMP or another server manager handles Java, NeoForge, memory, process control and backups. Packwiz installs managed pack files; this repository does not contain a server manager.

Install the official [Packwiz installer bootstrap](https://packwiz.infra.link/tutorials/installing/packwiz-installer/) into your server's game directory. Read and accept the Minecraft EULA yourself if you agree to it. Stop the server and back up its world before changing the pack.

From that game directory, replace the repository path and run:

```text
java -jar packwiz-installer-bootstrap.jar -g -s server "https://raw.githubusercontent.com/YOUR-OWNER/YOUR-PACK/public/pack/pack.toml"
```

Use `beta` for an isolated testing server or a full commit SHA for a fixed snapshot. `-s server` excludes client-only files. Do not copy a client instance onto a server or run updates against a running server. Configure your manager's loader/runtime separately when those requirements change.

## Disposable release check

The release workflow uses Docker with a new private volume and no published ports. It explicitly requires EULA acceptance, installs the captured commit, starts and ticks the server, writes a vanilla fixture, saves and stops, restarts, then checks that the fixture persisted. It removes only its own container and volume.

To run the same test locally with Docker and Python 3.11+:

```text
python distribution/smoke.py --repository YOUR-OWNER/YOUR-PACK --pack-sha FULL_40_CHARACTER_COMMIT --accept-eula --output dist/local-smoke
```

Choose a new output directory each run. No server starts without `--accept-eula`. Review both phase logs and `report.json`; `lifecycle_passed_logs_unreviewed` means only the recorded lifecycle checks passed. This check does not exercise real clients, mod-specific behavior or an existing world's upgrade.

