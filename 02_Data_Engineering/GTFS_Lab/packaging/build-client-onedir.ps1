param(
    [Parameter(Mandatory = $true)]
    [string] $DuckDBCliPath,

    [Parameter(Mandatory = $true)]
    [string] $OutputRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$LabRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$RepoRoot = (Resolve-Path (Join-Path $LabRoot '..\..')).Path
$BuildRoot = [System.IO.Path]::GetFullPath($OutputRoot)
if ($BuildRoot.Equals($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
    $BuildRoot.StartsWith($RepoRoot.TrimEnd('\') + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'OutputRoot debe estar fuera del checkout para no mezclar binarios con fuentes.'
}
if (Test-Path -LiteralPath $BuildRoot) {
    throw "OutputRoot ya existe; el build no sobrescribe artefactos: $BuildRoot"
}
$DuckDBCli = (Resolve-Path -LiteralPath $DuckDBCliPath).Path
$GitStatus = (& git -C $RepoRoot status --porcelain --untracked-files=all | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { throw 'No se pudo comprobar el estado Git de las fuentes.' }
if ($GitStatus) { throw 'El build reproducible requiere un worktree Git limpio.' }
$DuckDBVersion = (& $DuckDBCli --version | Out-String).Trim()
if ($DuckDBVersion -notmatch '^v?1\.5\.5\b') {
    throw "Se requiere DuckDB CLI 1.5.5; detectado: $DuckDBVersion"
}
$BuildPython = Get-Command python -ErrorAction Stop
$PythonVersion = (& $BuildPython.Source --version | Out-String).Trim()
if ($PythonVersion -ne 'Python 3.12.10') {
    throw "El build reproducible requiere Python 3.12.10; detectado: $PythonVersion"
}

New-Item -ItemType Directory -Path $BuildRoot | Out-Null
$Venv = Join-Path $BuildRoot '.venv'
$DistPath = Join-Path $BuildRoot 'dist'
$WorkPath = Join-Path $BuildRoot 'work'
& $BuildPython.Source -m venv $Venv
if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno de build aislado.' }
$VenvPython = Join-Path $Venv 'Scripts\python.exe'
& $VenvPython -m pip install --disable-pip-version-check --requirement (Join-Path $PSScriptRoot 'client-build-requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación reproducible de dependencias de build.' }

$PreviousDuckDBCli = $env:TDL_DUCKDB_CLI
try {
    $env:TDL_DUCKDB_CLI = $DuckDBCli
    & $VenvPython -m PyInstaller --noconfirm --clean --distpath $DistPath --workpath $WorkPath (Join-Path $PSScriptRoot 'tdl_client_onedir.spec')
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller no terminó correctamente.' }
} finally {
    if ($null -eq $PreviousDuckDBCli) { Remove-Item Env:TDL_DUCKDB_CLI -ErrorAction SilentlyContinue }
    else { $env:TDL_DUCKDB_CLI = $PreviousDuckDBCli }
}

$PackageRoot = Join-Path $DistPath 'tdl-client'
$GuiExe = Join-Path $PackageRoot 'tdl-client.exe'
$WorkerExe = Join-Path $PackageRoot 'tdl-worker.exe'
if (-not (Test-Path -LiteralPath $GuiExe) -or -not (Test-Path -LiteralPath $WorkerExe)) {
    throw 'La salida onedir no contiene GUI y worker.'
}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Install-Client.ps1') -Destination $PackageRoot
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Uninstall-Client.ps1') -Destination $PackageRoot

$Head = (& git -C $RepoRoot rev-parse HEAD | Out-String).Trim()
$BuildPythonVersion = (& $VenvPython --version | Out-String).Trim()
$PyInstallerVersion = (& $VenvPython -c 'import PyInstaller; print(PyInstaller.__version__)' | Out-String).Trim()
$ReportLabVersion = (& $VenvPython -c 'import reportlab; print(reportlab.Version)' | Out-String).Trim()
$Metadata = [ordered]@{
    product = 'Transit Data Lab Windows GTFS Client'
    product_version = '1.0.0-rc.1'
    source_commit = $Head
    python = $BuildPythonVersion
    pyinstaller = $PyInstallerVersion
    reportlab = $ReportLabVersion
    duckdb_cli = $DuckDBVersion
    package_layout = 'onedir'
    output_files = @('tdl-client/tdl-client.exe', 'tdl-client/tdl-worker.exe')
    code_signing = 'NOT_USED; certificate suitability not assessed'
    smartScreen_reputation = 'NOT_ESTABLISHED'
}
$Metadata | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $BuildRoot 'build-metadata.json') -Encoding utf8
Write-Output "BUILD=PASS"
Write-Output "OUTPUT=$PackageRoot"
Write-Output "SOURCE_COMMIT=$Head"
Write-Output "PYTHON=$BuildPythonVersion"
Write-Output "PYINSTALLER=$PyInstallerVersion"
Write-Output "REPORTLAB=$ReportLabVersion"
Write-Output "DUCKDB_CLI=$DuckDBVersion"
