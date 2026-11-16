# Play your pack with Prism

The upstream template is an empty example and has no player releases. After your maintainer publishes the first release, open your pack repository's **Releases** page and download the attached `YOUR-ID-Public-Prism.zip`, `YOUR-ID-Beta-Prism.zip`, or a numbered ZIP. Do not use GitHub's source-code archive.

Install [Prism Launcher](https://prismlauncher.org/), choose **Add Instance → Import**, and select the ZIP or paste its download link. Use Java 21, sign in with a Minecraft account, and allow the Packwiz pre-launch command when prompted. It downloads the pack files from their providers before launch.

| Download | Updates |
| --- | --- |
| `channel-public` release | Follows the public branch |
| `channel-beta` release | Follows beta, including changes not yet server-tested |
| Numbered `vX.Y.Z` release | Stays on the exact recorded commit |

Public and Beta have distinct instance identities. Use a separate instance when switching channels or versions. Back up worlds; a fixed modpack snapshot is not a world rollback.

Packwiz updates managed pack files. Changes to the Minecraft version, loader or launcher settings require importing a new ZIP or updating Prism's runtime yourself. Existing instances do not acquire new launcher metadata just because a rolling ZIP was rebuilt.
