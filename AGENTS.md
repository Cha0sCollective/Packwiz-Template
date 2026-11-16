# Repository guidance

This is a reusable Packwiz example. Keep it lightweight: ordinary Packwiz files,
native Prism metadata and concise maintainer/player documentation.

- Preserve the beta → reviewed public promotion flow; main tracks accepted public.
- Keep the upstream template unconfigured and publication disabled. Fork owners
  personalize metadata with distribution/init.py and configure their own reviewers.
- Never hard-code a fork owner's repository, server address or user name into code.
- Use official upstream downloads and retain required notices. Do not bundle gameplay JARs.
- Edit maintained content under pack/, preserve LF bytes and run packwiz refresh.
- Preserve unrelated work. Test in isolated instances, never on a live server or world.
- Test consequential packaging/release changes, including failure and retry behavior.
  Distinguish hash/ZIP checks from real Minecraft launches and gameplay validation.
- Keep branch and environment approval requirements explicit in the setup guide.
