# Releases and Prism imports

Complete [repository setup](../docs/SETUP.md) before publishing. Daily edits remain ordinary Git and Packwiz operations on beta.

## Promote a release

1. Push the changes you want to beta.
2. Run **Promote beta to public** from public with a new stable version and your explicit Minecraft EULA acceptance.
3. Review the captured commit, notes, ZIP checksums and both lifecycle phase logs in the downloadable artifact.
4. Approve the waiting `public-release` deployment. A sole maintainer can approve their own run after review.

The first release may be `0.1.0`; there are no required historical tags. Later releases must use a greater version and preserve the previous fixed release. Preparation aligns Packwiz, profile and optional BCC version labels, refreshes the pack, and may commit that change to beta. Pull beta before your next edit.

Approval publishes a fixed snapshot, advances public and main atomically to the captured commit, and refreshes Public's ZIP. Later beta pushes are not included. Public is GitHub's Latest release; Beta is a prerelease. Numbered tags and ZIPs are never overwritten. Documentation/tooling-only commits may follow a version tag if the pack, identity, runtime and tool pins still match it.

Beta's rolling ZIP refreshes automatically on beta pushes after setup. Beta instances follow the branch even before a server check passes. A later push can supersede an older packaging run; rerun **Update Beta installer** from beta if the current runtime metadata has no successful build.

## Failures and retries

- Before approval, public is unchanged. Preparation may already have created a beta version commit. Fix beta and start again with an unused version.
- If publication fails, use **Re-run failed jobs** on the same run. It reuses the original candidate and exact ZIP bytes, retained for 30 days. Matching draft releases resume; conflicting fixed tags/assets stop publication.
- Concurrent changes to public or main stop promotion. The atomic push prevents updating only one branch. A numbered release may already exist if a later step fails.
- If the rolling Public upload fails after promotion, players already follow the new public commit. Retry publication; do not force the branch or a live world backward.
- If the original artifact expired, inspect the published state before proceeding. Do not rebuild and overwrite an existing numbered release.

Direct pushes to public bypass approval and can reach players immediately. Use promotion for normal releases. Main tracks accepted public; it is not a separate development branch.

## Build imports locally

Use a clean, committed checkout, PowerShell 7, Git and internet access:

```text
pwsh -NoProfile -File distribution/Build-Prism.ps1 -Channel public -Output dist/My-Pack-Public-Prism.zip
pwsh -NoProfile -File distribution/Build-Prism.ps1 -Channel beta -Output dist/My-Pack-Beta-Prism.zip
pwsh -NoProfile -File distribution/Build-Prism.ps1 -VersionTag v0.1.0 -Output dist/My-Pack-0.1.0-Prism.zip
```

The output filename can be chosen for local builds. Published assets use the permanent ID from `profile.json`. Existing ZIPs or checksum files are never overwritten. Metadata, runtime, icon and tool pins come from the selected committed revision, not uncommitted edits.

`-SourceRevision <commit>` selects rolling installer metadata without changing its update branch. `-VersionTag` resolves a published tag to a full SHA. Release preparation uses `-SnapshotVersion vX.Y.Z -SourceRevision <commit>` to build a fixed candidate without creating a tag. `-PackUrl http://127.0.0.1:PORT/pack/pack.toml` is available for isolated local tests only; do not distribute such a ZIP.

Each ZIP has a `.sha256` sidecar and records both pack and packaging commits. It contains only Prism metadata, instructions, notices and two pinned, hash-verified Packwiz tools. Gameplay downloads remain upstream and depend on continued provider availability.

Run `python -m unittest discover -s distribution/tests -v` for release safeguards and `python distribution/release.py validate` for managed-file and runtime checks. GitHub CI also refreshes Packwiz and refuses stale committed hashes, then builds both channels and a fixed import on Windows and Linux. These packaging checks do not launch Minecraft.

