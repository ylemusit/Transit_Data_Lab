param(
    [string] $ProgramRoot = (Join-Path $env:LOCALAPPDATA 'Programs\Transit Data Lab\GTFS Auditor')
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Version = '1.0.0-rc.1'
$ProgramRoot = [System.IO.Path]::GetFullPath($ProgramRoot).TrimEnd('\')
$InstallDirectory = [System.IO.Path]::GetFullPath((Join-Path $ProgramRoot $Version))
if (-not $InstallDirectory.StartsWith($ProgramRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'La ruta de desinstalación no pertenece al directorio de programa configurado.'
}
if (-not (Test-Path -LiteralPath $InstallDirectory)) {
    Write-Output 'No existe esta versión instalada.'
    return
}

$Confirmation = Read-Host "Escribe S para eliminar únicamente $InstallDirectory"
if ($Confirmation -cne 'S') {
    Write-Output 'Desinstalación cancelada.'
    return
}
$StartMenuShortcut = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Transit Data Lab GTFS Auditor $Version.lnk"
if (Test-Path -LiteralPath $StartMenuShortcut) {
    Remove-Item -LiteralPath $StartMenuShortcut -Force
}
Remove-Item -LiteralPath $InstallDirectory -Recurse -Force
Write-Output 'Se quitó la versión seleccionada y su acceso directo.'
