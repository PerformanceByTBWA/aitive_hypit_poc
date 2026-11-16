$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
'===== check'
& $hy check '.\remake.svrun' 2>&1 | ForEach-Object { "$_" }
"exit=$LASTEXITCODE"
