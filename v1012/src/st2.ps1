$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$ref = 'references\v1012'
$utf8 = New-Object System.Text.UTF8Encoding $false
function Save([string]$name, [string[]]$lines) { [IO.File]::WriteAllText((Join-Path $proj "$ref\io\$name"), ($lines -join "`n"), $utf8) }
$o = & $hy media probe "$ref\source.mp4" --json 2>&1 | ForEach-Object { "$_" }; Save '01_probe.json' $o; '===== probe json'; $o
$t0 = Get-Date
$o = & $hy media boundaries "$ref\source.mp4" --rate 30 --json 2>&1 | ForEach-Object { "$_" }; Save '03_boundaries_r30.json' $o
'===== boundaries r30 default threshold sec=' + [math]::Round(((Get-Date) - $t0).TotalSeconds, 1); $o
$o = & $hy media boundaries "$ref\source.mp4" --rate 30 2>&1 | ForEach-Object { "$_" }; Save '03_boundaries_r30.txt' $o; '===== boundaries text'; $o
$o = & $hy media tile "$ref\source.mp4" --start 0 --end 15.015 --every 1 --to "$ref\evidence\whole_1s.jpg" 2>&1 | ForEach-Object { "$_" }; '===== tile whole 1s'; $o
$o = & $hy media tile "$ref\source.mp4" --start 0 --end 15.015 --every 0.5 --columns 6 --to "$ref\evidence\whole_05s.jpg" 2>&1 | ForEach-Object { "$_" }; '===== tile whole 0.5s'; $o
