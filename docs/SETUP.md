# Set up your pack

## 1. Create your repository

Use a **public GitHub repository** for the raw Packwiz URLs and this Actions workflow. GitHub's required environment reviewers are available for public repositories on current plans; private repositories need different download authentication and may need a different plan.

Choose either:

- **Fork** this repository and select **Copy the public branch only**.
- **Use this template → Create a new repository** and leave **Include all branches off**.

Do not use the all-branches template option: GitHub gives those generated branches unrelated histories, which breaks the ancestor checks used by promotion. Create the other branches from the personalized default branch below.

Install Git, Python 3.11+, [Packwiz](https://packwiz.infra.link/installation/), and PowerShell 7 (`pwsh`) for local packaging. GitHub CLI (`gh`) is needed only for running release commands locally; Actions already supplies it. Put Packwiz on PATH.

## 2. Personalize the empty pack

Replace the example owner, repository and names in these commands. Start from a fresh clone with no local edits:

```text
git clone https://github.com/YOUR-OWNER/YOUR-PACK.git
cd YOUR-PACK
git branch -M public
python distribution/init.py --repository YOUR-OWNER/YOUR-PACK --name "My Pack" --id My-Pack --author "Your Name"
python distribution/release.py validate
git add distribution/repository.json distribution/profile.json pack
git commit -m "Personalize pack template"
git push -u origin public
git push origin public:main public:beta
git fetch origin
git switch -c beta --track origin/beta
```

On systems where Python is named `python3`, use that command instead. The initializer edits only local metadata and runs ordinary `packwiz refresh`. It does not create branches, push or publish.

Set **Settings → General → Default branch** to `public`. The three branches must share history. If you copied extra branches and the push refuses, stop and inspect them; do not force-push away existing work.

The `--id` controls Prism instance identities and asset names, such as `My-Pack-Public-Prism.zip`. Keep it stable once downloads exist. `distribution/repository.json` must name your own repository and contain `"template": false`; release commands also verify the current GitHub repository and `origin` before writing.

## 3. Configure release approval

Repository settings and Actions variables are **not inherited** when someone forks or generates a template.

1. Enable GitHub Actions in your fork if GitHub shows an enablement prompt.
2. Under **Settings → Environments**, create `public-release`.
3. Add yourself or your maintainers as **required reviewers**. For a solo maintainer, leave **Prevent self-review** disabled.
4. Disable **Allow administrators to bypass configured protection rules** and allow deployments from the `public` branch.
5. Ensure your repository/organization Actions policy permits the pinned actions and the workflow's declared `contents: write` permission. Branch rules must allow the approved automation to update `public` and `main`, and preparation to update `beta`.
6. Under **Settings → Secrets and variables → Actions → Variables**, create the repository variable `PACKWIZ_RELEASES_ENABLED` with the exact value `true`.

No PAT is needed: workflows use the repository's automatic `GITHUB_TOKEN`. The preparation step checks that a reviewer gate exists and self-approval is available. A missing gate stops the release before changing beta.

Enable publishing only after steps 1–5. The upstream template keeps this variable unset and `template` enabled, so it never publishes example pack releases.

## 4. Add your content and make the first release

On `beta`, run Packwiz commands inside `pack/`, add your intended configuration, and push. Read [Contributing](CONTRIBUTING.md) for dependency and world compatibility checks. **Update Beta installer** runs on beta pushes; it can also be dispatched manually from beta after setup.

Run **Actions → Promote beta to public** from **public**, enter `0.1.0` for your first release, and explicitly accept the Minecraft EULA if you agree to it. The workflow does not assume any old tag or download exists. For later releases, use a greater stable version such as `0.1.1`.

Review the artifact and both server phase logs. Approve the waiting `public-release` deployment when satisfied. Pull beta afterward because preparation may have created a version commit. Read [release operations](../distribution/README.md) before handling retries.

The generic server test checks lifecycle and vanilla block/item persistence. It does not test every mod, client behavior or world upgrades; add pack-specific checks and test those behaviors separately.

## Sources

- [GitHub template repositories and branch history](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
- [GitHub deployment environments and reviewer availability](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [Packwiz getting started](https://packwiz.infra.link/tutorials/creating/getting-started/)

