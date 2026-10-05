"""Keep bundled command-line runtime dependencies discoverable by children."""
import os
import sys

if getattr(sys, "frozen", False):
    _runtime_dir = str(getattr(sys, "_MEIPASS", os.path.dirname(sys.executable)))
    os.environ["PATH"] = _runtime_dir + os.pathsep + os.environ.get("PATH", "")