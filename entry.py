"""Entry point of the standalone verfy build.

The CLI sometimes starts itself as `<python> -m verfy ...` (verfy demo). In this
build sys.executable is verfy itself, so accept those two forms here.
"""
import os
import sys

from verfy import demo_server
from verfy.cli import main


def _without_own_path(argv: list[str]) -> list[str]:
    # On some Windows machines the program receives its own path again as the
    # first argument; verfy never takes its own executable as a command.
    if len(argv) > 1:
        try:
            if os.path.samefile(argv[1], sys.executable):
                return [argv[0], *argv[2:]]
        except (OSError, ValueError):
            pass
    return argv


if __name__ == "__main__":
    sys.argv = _without_own_path(sys.argv)
    if sys.argv[1:3] == ["-m", "verfy.demo_server"]:
        sys.argv = [sys.argv[0], *sys.argv[3:]]
        sys.exit(demo_server.main())
    if sys.argv[1:3] == ["-m", "verfy"]:
        sys.argv = [sys.argv[0], *sys.argv[3:]]
    sys.exit(main())
