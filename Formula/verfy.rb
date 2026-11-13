# Written by scripts/packages.py for each release; do not edit by hand.
class Verfy < Formula
  desc "Lockfile and guard for the MCP tools and commands your AI coding agents use"
  homepage "https://verfy.dev"
  version "0.23.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases/download/v0.23.0/verfy-macos-arm64.tar.gz"
      sha256 "5b51b1db58bfd623bb2b07b48aa77559c2ccdc611fe8f4638f38fb7d9dfbc3c1"
    end
  end

  on_linux do
    on_intel do
      url "https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases/download/v0.23.0/verfy-linux-x64.tar.gz"
      sha256 "fb27f42952a02fefbe18dab894bfb227205d29a63f89409fcaafaabb4a3a892a"
    end
    on_arm do
      url "https://github.com/anvarbekovjavohir277-dot/verfy-releases/releases/download/v0.23.0/verfy-linux-arm64.tar.gz"
      sha256 "d73abd30dabb25169edda93fee1e51d9fb7a6ff89b918ff4840be4162ad0aca8"
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
