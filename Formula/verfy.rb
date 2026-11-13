# Written by scripts/packages.py for each release; do not edit by hand.
class Verfy < Formula
  desc "Lockfile and guard for the MCP tools and commands your AI coding agents use"
  homepage "https://verfy.dev"
  version "0.22.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases/download/v0.22.0/verfy-macos-arm64.tar.gz"
      sha256 "f85905cad6eecd4178fa9d3c868a486629e382b4d3dde7b3d5488a9959414600"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases/download/v0.22.0/verfy-linux-x64.tar.gz"
      sha256 "84db6cdb20a1176b0451cf29844bb92d6af898766cc76339490e8e334807027f"
    end
    on_arm do
      url "https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases/download/v0.22.0/verfy-linux-arm64.tar.gz"
      sha256 "17880b5b31594a79e7a15c74f5fd0c95a86d2a075c69f5fccfa1c1defb445146"
    end
  end

  def install
    # the standalone build: the verfy program with the Python it carries, kept together
    libexec.install Dir["*"]
    bin.write_exec_script libexec/"verfy"
  end

  test do
    assert_equal "verfy #{version}", shell_output("#{bin}/verfy --version").strip
    assert_match "chain verified", shell_output("VERFY_HOME=#{testpath}/home #{bin}/verfy demo")
  end
end
