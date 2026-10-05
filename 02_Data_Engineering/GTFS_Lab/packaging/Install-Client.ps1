param(
    [string] $ProgramRoot = (Join-Path $env:LOCALAPPDATA 'Programs\Transit Data Lab\GTFS Auditor')
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Version = '1.0.0-rc.1'
$SourceRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$ProgramRoot = [System.IO.Path]::GetFullPath($ProgramRoot)
$InstallDirectory = Join-Path $ProgramRoot $Version
if ($InstallDirectory.Equals($SourceRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
    $InstallDirectory.StartsWith($SourceRoot.TrimEnd('\') + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'La carpeta de instalación no puede estar dentro del paquete de origen.'
}
if (Test-Path -LiteralPath $InstallDirectory) {
    throw "Ya existe una instalación de $Version; no se sobrescribe: $InstallDirectory"
}
if (-not (Test-Path -LiteralPath (Join-Path $SourceRoot 'tdl-client.exe')) -or
    -not (Test-Path -LiteralPath (Join-Path $SourceRoot 'tdl-worker.exe'))) {
    throw 'El paquete debe incluir tdl-client.exe y tdl-worker.exe.'
}

New-Item -ItemType Directory -Path $InstallDirectory -Force | Out-Null
foreach ($item in Get-ChildItem -LiteralPath $SourceRoot -Force) {
    Copy-Item -LiteralPath $item.FullName -Destination $InstallDirectory -Recurse -Force
}
if (-not (Test-Path -LiteralPath (Join-Path $InstallDirectory 'tdl-client.exe')) -or
    -not (Test-Path -LiteralPath (Join-Path $InstallDirectory 'tdl-worker.exe'))) {
    throw 'La copia del paquete no quedó completa; no se creó acceso directo.'
}

$StartMenu = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
New-Item -ItemType Directory -Path $StartMenu -Force | Out-Null
$ShortcutPath = Join-Path $StartMenu "Transit Data Lab GTFS Auditor $Version.lnk"
$Shell = New-Object -ComObject WScript.Shell
$Shortcut = $Shell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = Join-Path $InstallDirectory 'tdl-client.exe'
$Shortcut.WorkingDirectory = $InstallDirectory
$Shortcut.Description = "Auditor GTFS local $Version"
$Shortcut.Save()
Write-Output "Instalación completada para el usuario actual: $InstallDirectory"
