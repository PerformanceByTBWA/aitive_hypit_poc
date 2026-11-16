$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$bid = 'bld_20261111T082016026Z_61FF51E113'
$out = Join-Path $proj 'out\v1012'
'===== leftover'
(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'whisperx|hypit|chrome-headless-shell' } | Measure-Object).Count
foreach ($o in @('caption-timing', 'speech.ad', 'ad-media.extent')) {
  "===== get $o"
  & $hy get $bid --output $o --to (Join-Path $out ($o -replace '\.', '_')) 2>&1 | ForEach-Object { "$_" }
}
'===== tile replica'
& $hy media tile "$out\v1012_replica.mp4" --start 0 --end 15 --every 0.5 --columns 6 --transcript 'references\v1012\transcript.json' --to "$out\replica_05s.jpg" 2>&1 | ForEach-Object { "$_" }
& $hy media frames "$out\v1012_replica.mp4" --at '3.2,6.0,11.6,14.0' --to "$out\replica_full" 2>&1 | ForEach-Object { "$_" }
& ffmpeg -y -v error -i "$out\v1012_replica.mp4" -vf 'scale=960:-2' -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart "$out\v1012_replica_web.mp4"
& ffmpeg -y -v error -i 'references\v1012\source.mp4' -vf 'scale=960:-2' -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart "$out\v1012_source_web.mp4"
Get-ChildItem -Recurse $out | Select-Object FullName, Length | Format-Table -AutoSize | Out-String -Width 220
