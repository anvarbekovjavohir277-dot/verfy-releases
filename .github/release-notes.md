![verfy posture, verfy setup and verfy doctor](https://raw.githubusercontent.com/verfy-dev/verfy-releases/main/docs/assets/verfy-setup.gif)

## Try it in a minute

```bash
pip install "verfy==VERFY_VERSION"      # or a standalone build below, which carries its own Python
verfy posture                     # risky settings in the coding agents on this computer; changes nothing
verfy setup                       # what Verfy would add to each agent; --write does it, keeping backups
```

What `verfy posture` reports on a computer where agents were left wide open (real output):

```text
HIGH     Claude Code: permissions.defaultMode = bypassPermissions
         Claude Code runs every tool without asking you. Verfy's hook still checks each call, but nothing else does.
         Fix: Use "default" or "acceptEdits".  (~/.claude/settings.json)
HIGH     Codex CLI: approval_policy = "never"
         Codex never asks you before it runs a command. Verfy's hook still checks each call, but nothing else does.
         Fix: Use "on-request" or "untrusted".  (~/.codex/config.toml)
MEDIUM   Claude Code: permissions.allow contains Bash(*)
         Every shell command is allowed without a prompt. Verfy still asks about the risky ones it recognises.
         Fix: Allow specific commands, such as Bash(npm test).  (~/.claude/settings.json)
```

## Fail a pull request when an MCP tool changes

Copy [examples/ci/verfy.yml](https://github.com/verfy-dev/verfy-releases/blob/main/examples/ci/verfy.yml) to `.github/workflows/verfy.yml`, after `verfy lock check --update` and committing `verfy.lock`:

```yaml
name: Verfy MCP Lock
on: [pull_request, push]
permissions:
  contents: read
jobs:
  lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: verfy-dev/verfy-action@v1
```

## What changed

VERFY_CHANGES

## The downloads

Standalone builds of [verfy VERFY_VERSION](https://pypi.org/project/verfy/VERFY_VERSION/) from PyPI, with Python included, built and tested by this repository's workflow, and `verfy-vscode.vsix`, the extension for VS Code, Cursor and Devin Desktop (in the editor: Extensions > ... > Install from VSIX). Install: https://verfy.dev/install

Check a download: `sha256sum -c SHA256SUMS --ignore-missing`, and that this workflow built it: `gh attestation verify verfy-linux-x64.tar.gz -R verfy-dev/verfy-releases`, or with cosign as [SECURITY.md](SECURITY.md#check-a-release) shows.
