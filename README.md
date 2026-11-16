# Packwiz Template

A forkable example of the [Create: Ch4oS Packwiz](https://github.com/Cha0sCollective/Create-Ch4os-Packwiz) release workflow. Start with an empty pack, add your own mods and configuration, and manage releases the same way.

**Start here: [set up your own repository](docs/SETUP.md).** Fork this repository, or use **Use this template** with **Include all branches turned off**. The setup guide creates `main` and `beta` from your personalized `public` branch so they share history.

This starter uses **Minecraft 1.21.1, NeoForge 21.1.248 and Java 21**. It contains no gameplay mods or CH4OS configuration. Other Minecraft versions and loaders need corresponding changes to the builder and server test.

## The workflow

| Branch | Purpose | Player behavior |
| --- | --- | --- |
| `beta` | Everyday edits and testing | Beta Prism instances update at launch |
| `public` | The release selected by the maintainer | Public Prism instances update at launch |
| `main` | Tracks the accepted release | Moves with `public` during promotion |

1. Edit the ordinary Packwiz pack under `pack/`, refresh its index, and push to `beta`.
2. Actions builds a rolling Beta Prism import ZIP.
3. Run **Promote beta to public** with a version. It captures beta, aligns version labels, builds the imports, and tests a disposable server through startup, ticking, saving and restart.
4. Review the exact candidate, ZIPs and logs, then approve the `public-release` environment.
5. Actions publishes an immutable numbered release, advances `public` and `main` together, and updates the rolling Public ZIP.

Numbered Prism downloads follow a commit SHA. Rolling downloads follow a branch. Mods download from their providers; import ZIPs contain only Prism metadata, notices and the two hash-verified Packwiz installer tools.

## Included

- A valid empty Packwiz pack with examples of where to add files.
- A local personalization command for repository, name, author and permanent pack ID.
- Windows/Linux checks, Prism packaging, release checksums and retry safeguards.
- A first-release path that works without inherited tags or releases.
- A disposable dedicated-server test with generic block/item persistence checks.
- Maintainer, Prism and server setup guides.

Release publication starts **disabled**. Fork settings, reviewers and Actions variables must be configured in your own repository. No custom token or separate hosting service is required for the public-repository workflow.

[Setup](docs/SETUP.md) · [Contributing](docs/CONTRIBUTING.md) · [Releases](distribution/README.md) · [Prism](docs/PRISM.md) · [Servers](docs/SERVER.md) · [Customization](docs/CUSTOMIZATION.md)

Project-authored files are [MIT licensed](LICENSE.txt). See [attribution](NOTICE.md) for the source revisions. Upstream downloads retain their own licenses.

