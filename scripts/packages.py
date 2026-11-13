"""Write the Homebrew formula (Formula/verfy.rb) and the Scoop manifest (bucket/verfy.json) for one release.

The release job of build.yml runs it after it publishes the standalone builds, with that release's SHA256SUMS:

    python3 scripts/packages.py 0.23.0 out/SHA256SUMS

Both point at the files of that GitHub release, with their SHA-256 from the signed list. This repository is the tap and
the bucket:

    brew tap verfy-dev/verfy https://github.com/verfy-dev/verfy-releases && brew install verfy
    scoop bucket add verfy https://github.com/verfy-dev/verfy-releases && scoop install verfy
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = "verfy-dev/verfy-releases"
ROOT = Path(__file__).resolve().parent.parent
DESC = "Lockfile and guard for the MCP tools and commands your AI coding agents use"


def sums(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text("utf-8").splitlines():
        m = re.fullmatch(r"([0-9a-f]{64})\s+\*?(\S+)", line.strip())
        if m:
            out[m.group(2)] = m.group(1)
    return out


def formula(version: str, sha: dict[str, str]) -> str:
    url = f"https://github.com/{REPO}/releases/download/v{version}"
    return f'''# Written by scripts/packages.py for each release; do not edit by hand.
class Verfy < Formula
  desc "{DESC}"
  homepage "https://verfy.dev"
  version "{version}"
  license "MIT"

  on_macos do
    on_arm do
      url "{url}/verfy-macos-arm64.tar.gz"
      sha256 "{sha["verfy-macos-arm64.tar.gz"]}"
    end
  end

  on_linux do
    on_intel do
      url "{url}/verfy-linux-x64.tar.gz"
      sha256 "{sha["verfy-linux-x64.tar.gz"]}"
    end
    on_arm do
      url "{url}/verfy-linux-arm64.tar.gz"
      sha256 "{sha["verfy-linux-arm64.tar.gz"]}"
    end
  end

  def install
    # the standalone build: the verfy program with the Python it carries, kept together
    libexec.install Dir["*"]
    bin.write_exec_script libexec/"verfy"
  end

  test do
    assert_equal "verfy #{{version}}", shell_output("#{{bin}}/verfy --version").strip
    assert_match "chain verified", shell_output("VERFY_HOME=#{{testpath}}/home #{{bin}}/verfy demo")
  end
end
'''


def manifest(version: str, sha: dict[str, str]) -> str:
    url = f"https://github.com/{REPO}/releases/download/v{version}"
    data = {
        "version": version,
        "description": DESC,
        "homepage": "https://verfy.dev",
        "license": "MIT",
        "architecture": {"64bit": {"url": f"{url}/verfy-windows-x64.zip", "hash": sha["verfy-windows-x64.zip"], "extract_dir": "verfy"}},
        "bin": "verfy.exe",
        "checkver": {"github": f"https://github.com/{REPO}"},
        "autoupdate": {"architecture": {"64bit": {"url": f"https://github.com/{REPO}/releases/download/v$version/verfy-windows-x64.zip", "extract_dir": "verfy"}},
                       "hash": {"url": "$baseurl/SHA256SUMS"}},
        "notes": "Windows Smart App Control may block verfy.exe until the build is code-signed; `pip install verfy` works meanwhile.",
    }
    return json.dumps(data, indent=4) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not re.fullmatch(r"\d+\.\d+\.\d+", argv[0]):
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        return 2
    version, sha = argv[0], sums(Path(argv[1]))
    missing = [f for f in ("verfy-macos-arm64.tar.gz", "verfy-linux-x64.tar.gz", "verfy-linux-arm64.tar.gz", "verfy-windows-x64.zip") if f not in sha]
    if missing:
        print(f"not in the list: {', '.join(missing)}", file=sys.stderr)
        return 1
    current = ROOT / "bucket" / "verfy.json"
    if current.exists():
        have = json.loads(current.read_text("utf-8")).get("version", "0")
        if tuple(int(x) for x in have.split(".")) > tuple(int(x) for x in version.split(".")):
            print(f"Formula and bucket stay at {have}: {version} is older (a rebuild)")
            return 0
    (ROOT / "Formula").mkdir(exist_ok=True)
    (ROOT / "bucket").mkdir(exist_ok=True)
    (ROOT / "Formula" / "verfy.rb").write_text(formula(version, sha), "utf-8", newline="\n")
    (ROOT / "bucket" / "verfy.json").write_text(manifest(version, sha), "utf-8", newline="\n")
    print(f"Formula/verfy.rb and bucket/verfy.json for {version}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
