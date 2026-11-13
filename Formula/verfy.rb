# Written by scripts/packages.py for each release; do not edit by hand.
class Verfy < Formula
  desc "Lockfile and guard for the MCP tools and commands your AI coding agents use"
  homepage "https://verfy.dev"
  version "0.23.1"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/verfy-dev/verfy-releases/releases/download/v0.23.1/verfy-macos-arm64.tar.gz"
      sha256 "ad156486e15e6895c03ca118e2320a072d574a00c33895480a20b89b3651b42e"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/verfy-dev/verfy-releases/releases/download/v0.23.1/verfy-linux-x64.tar.gz"
      sha256 "588d94ff64a876562f46d1663370be967c75da8595a165216f06829ab96875db"
    end
    on_arm do
      url "https://github.com/verfy-dev/verfy-releases/releases/download/v0.23.1/verfy-linux-arm64.tar.gz"
      sha256 "778511769b6e9a099749e6bedca0c5f1a4948e723486bb83ec142f5707531a24"
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
