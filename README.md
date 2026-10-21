# verfy standalone builds

Ready-to-run builds of the [verfy](https://pypi.org/project/verfy/) CLI that carry their own Python, so nothing else has to be installed first.

```bash
curl -fsSL https://verfy-tech.vercel.app/install.sh | sh          # macOS (Apple silicon) and Linux (x64, arm64)
```

```powershell
irm https://verfy-tech.vercel.app/install.ps1 | iex                # Windows (x64)
```

The script downloads the build for your system from the latest release here, checks it against the release's `SHA256SUMS`, and puts `verfy` on your PATH. Set `VERFY_VERSION=0.2.0` first to install a specific version. With Python 3.10 or newer you can also run `pip install verfy`.

## How the builds are made

[`.github/workflows/build.yml`](.github/workflows/build.yml) installs the release from PyPI, freezes it with PyInstaller (one folder, not one file, so it starts fast), runs a few checks on each platform and attaches the archives and `SHA256SUMS` to a GitHub release. It checks PyPI every 6 hours and builds only versions that have no release yet.

- Builds: `windows-x64`, `linux-x64` and `linux-arm64` (glibc 2.35 or newer), `macos-arm64`. Intel Macs: use `pip install verfy`.
- The builds are **not code-signed**. Windows or macOS may warn the first time you run one that you downloaded with a browser.
- `SHA256SUMS` comes from the same release, so it catches a broken or partial download; it does not protect against someone who can change the release itself.

## Uninstall

- macOS and Linux: `rm -rf ~/.local/share/verfy ~/.local/bin/verfy`, then remove the PATH line the installer added to your shell profile, if any.
- Windows: delete `%LOCALAPPDATA%\Programs\verfy` and remove that folder's `current` entry from your user PATH.

Your keys, policy and receipts live in `~/.verfy` and are not touched by either.

MIT license.
