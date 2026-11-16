$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$ref = 'references\v1012'
'===== tile whole 1s'
& $hy media tile "$ref\source.mp4" --start 0 --end 15 --every 1 --to "$ref\evidence\whole_1s.jpg" 2>&1 | ForEach-Object { "$_" }
'===== tile whole 0.5s'
& $hy media tile "$ref\source.mp4" --start 0 --end 15 --every 0.5 --columns 6 --to "$ref\evidence\whole_05s.jpg" 2>&1 | ForEach-Object { "$_" }
