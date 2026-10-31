# Verfy

Verfy checks every tool call a coding agent makes against deterministic allow, ask and deny rules (no model decides), locks MCP tools and instruction files so a quiet change fails CI, and writes an Ed25519-signed receipt for each checked call. Website and docs: https://verfy-tech.vercel.app

This repository holds what you need to install and use it: ready-to-run builds, the Claude Code plugin, the security policy, the advisories and the research. The CLI's source code is in [anvarbekovjavohir277-dot/verfy](https://github.com/anvarbekovjavohir277-dot/verfy) (MIT); the Verfy name and logo are covered by the [trademark policy](TRADEMARKS.md).

## Install

```bash
pip install verfy                                                  # Python 3.10 or newer
curl -fsSL https://verfy-tech.vercel.app/install.sh | sh          # or a build with its own Python: macOS (Apple silicon), Linux (x64, arm64)
```

```powershell
irm https://verfy-tech.vercel.app/install.ps1 | iex                # Windows (x64)
```

The script downloads the build for your system from the latest release here, checks it against the release's `SHA256SUMS`, and puts `verfy` on your PATH. Set `VERFY_VERSION=0.7.0` first to install a specific version. Then run `verfy init`.

Claude Code plugin (it calls the `verfy` command, so install the CLI first):

```bash
claude plugin marketplace add anvarbekovjavohir277-dot/verfy-releases
claude plugin install verfy@verfy
```

Fail a pull request when an MCP tool changes (pin the version you use):

```yaml
- uses: actions/setup-python@v7
  with: { python-version: "3.13" }
- run: pip install "verfy==0.7.0" && verfy lock check --config .mcp.json --lock verfy.lock
```

## In this repository

- [Releases](https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases): the standalone builds and their `SHA256SUMS`.
- [`plugins/verfy`](plugins/verfy): the Claude Code plugin.
- [`SECURITY.md`](SECURITY.md): how to report a vulnerability or a bypass privately, and the hall of fame. [`docs/SECURITY_LIMITATIONS.md`](docs/SECURITY_LIMITATIONS.md): what Verfy does not stop.
- [`advisories/`](advisories): Verfy Advisories, open data with a public source for each.
- [`docs/research`](docs/research/2026-10-mcp-tool-changes.md) and [`research/`](research): how often MCP servers change their tools between releases (October 2026).
- [`CHANGELOG.md`](CHANGELOG.md) and [`examples/ci`](examples/ci), a locked MCP config used by the CI test here.

## How the builds are made

[`.github/workflows/build.yml`](.github/workflows/build.yml) installs the release from PyPI, freezes it with PyInstaller (one folder, not one file, so it starts fast), runs a few checks on each platform and attaches the archives and `SHA256SUMS` to a GitHub release. It checks PyPI every 6 hours and builds only versions that have no release yet.

- Builds: `windows-x64`, `linux-x64` and `linux-arm64` (glibc 2.35 or newer), `macos-arm64`. Intel Macs: use `pip install verfy`.
- The builds are **not code-signed**. Windows or macOS may warn the first time you run one that you downloaded with a browser.
- `SHA256SUMS` comes from the same release, so it catches a broken or partial download; it does not protect against someone who can change the release itself.

## Uninstall

- macOS and Linux: `rm -rf ~/.local/share/verfy ~/.local/bin/verfy`, then remove the PATH line the installer added to your shell profile, if any.
- Windows: delete `%LOCALAPPDATA%\Programs\verfy` and remove that folder's `current` entry from your user PATH.
- pip: `pip uninstall verfy`. The plugin: `claude plugin uninstall verfy@verfy`.

Your keys, policy and receipts live in `~/.verfy` and are not touched by any of these.

MIT license.
