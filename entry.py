"""Entry point of the standalone verfy build.

The CLI sometimes starts itself as `<python> -m verfy ...` (verfy demo). In this
build sys.executable is verfy itself, so accept those two forms here.
"""
import sys

from verfy import demo_server
from verfy.cli import main

if __name__ == "__main__":
    if sys.argv[1:3] == ["-m", "verfy.demo_server"]:
        sys.argv = [sys.argv[0], *sys.argv[3:]]
        sys.exit(demo_server.main())
    if sys.argv[1:3] == ["-m", "verfy"]:
        sys.argv = [sys.argv[0], *sys.argv[3:]]
    sys.exit(main())
