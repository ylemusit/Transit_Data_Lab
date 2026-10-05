"""Temporary technical entrypoint used only for a local PyInstaller onedir probe."""
from gtfs_lab.client_workflow import main

if __name__ == "__main__":
    raise SystemExit(main())
