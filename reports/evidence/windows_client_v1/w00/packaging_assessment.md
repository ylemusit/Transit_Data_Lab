# PyInstaller onedir feasibility — W00-R

- PyInstaller: 6.22.3; Python: 3.12.10; Windows 11 x64 build 26300.
- onedir analysis and build: PASS; local CLI --help: PASS.
- Probe directory size: 19877773 bytes.
- DuckDB CLI: NOT BUNDLED. The current workflow invokes an external DuckDB executable; discovery requires an explicit binary and a deliberate runtime path strategy.
- Clean-machine launch, full audit, lxml native-library loading in clean environment, SmartScreen/signing, installer, updates, and antivirus: NOT TESTED.
- PyInstaller reported optional/platform imports (grp, pwd, posix, fcntl, jsonschema, Java modules); no build error. Dynamic resource paths remain unverified.
- Assessment: PACKAGING_FEASIBILITY = LIMITED; this is not a release artifact.

The generated probe executable and build logs are retained under pyinstaller_probe/ as local feasibility evidence.
