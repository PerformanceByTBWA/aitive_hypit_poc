$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:PATH = 'D:\oss_eval\tools\uv-0.13.2;' + $env:PATH
$env:NO_COLOR = '1'
$env:DO_NOT_TRACK = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$ref = 'references\v1012'
New-Item -ItemType Directory -Force "$ref\evidence", "$ref\io" | Out-Null
'===== help media'
& $hy media --help 2>&1 | ForEach-Object { "$_" }
'===== help probe'
& $hy media probe --help 2>&1 | ForEach-Object { "$_" }
'===== help boundaries'
& $hy media boundaries --help 2>&1 | ForEach-Object { "$_" }
'===== help tile'
& $hy media tile --help 2>&1 | ForEach-Object { "$_" }
'===== help transcribe'
& $hy transcribe --help 2>&1 | ForEach-Object { "$_" }
'===== probe'
& $hy media probe "$ref\source.mp4" 2>&1 | ForEach-Object { "$_" } | Tee-Object -FilePath "$ref\io\01_probe.txt"
