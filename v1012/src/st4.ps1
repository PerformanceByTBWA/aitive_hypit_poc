$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$ref = 'references\v1012'
$ev = "$ref\evidence"
$tx = "$ref\transcript.json"
$utf8 = New-Object System.Text.UTF8Encoding $false
$ranges = @'
[
 {"id":"c01_1333","start":1.15,"end":1.55},
 {"id":"c02_2967","start":2.80,"end":3.20},
 {"id":"c03_4667","start":4.50,"end":4.90},
 {"id":"c04_6333","start":6.15,"end":6.55},
 {"id":"c05_7233","start":7.05,"end":7.45},
 {"id":"c06_8433","start":8.25,"end":8.65},
 {"id":"c07_1020","start":10.0,"end":10.45},
 {"id":"c08_1260","start":12.4,"end":12.85}
]
'@
[IO.File]::WriteAllText((Join-Path $proj "$ref\io\04_ranges.json"), $ranges, $utf8)
function Hy([string]$Label, [string[]]$HyArgs) {
  $t0 = Get-Date
  $lines = & $hy @HyArgs 2>&1 | ForEach-Object { "$_" }
  $c = $LASTEXITCODE
  $s = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
  "===== $Label exit=$c sec=$s"
  $lines
  [IO.File]::WriteAllText((Join-Path $proj "$ref\io\$Label.txt"), ("hypit $($HyArgs -join ' ')`nexit=$c sec=$s`n" + ($lines -join "`n")), $utf8)
}
Hy '04a_tile_words_05s' @('media', 'tile', "$ref\source.mp4", '--start', '0', '--end', '15', '--every', '0.5', '--columns', '6', '--transcript', $tx, '--to', "$ev\words_05s.jpg")
Hy '04b_tiles_cuts_everyframe' @('media', 'tiles', "$ref\source.mp4", '--ranges', "$ref\io\04_ranges.json", '--every-frame', '--columns', '6', '--rows', '2', '--cell', '320', '--transcript', $tx, '--to', "$ev\cuts")
Hy '04c_tile_ttalkkak' @('media', 'tile', "$ref\source.mp4", '--around', '딸깍!', '--transcript', $tx, '--padding', '0.6', '--every', '0.1', '--columns', '6', '--cell', '320', '--to', "$ev\ttalkkak.jpg")
Hy '04d_tile_hook' @('media', 'tile', "$ref\source.mp4", '--start', '0', '--end', '3', '--every', '0.25', '--columns', '6', '--cell', '320', '--transcript', $tx, '--to', "$ev\hook.jpg")
Hy '04e_tile_endcard' @('media', 'tile', "$ref\source.mp4", '--start', '10', '--end', '15', '--every', '0.25', '--columns', '5', '--cell', '320', '--transcript', $tx, '--to', "$ev\endcard.jpg")
Hy '04f_frames_full' @('media', 'frames', "$ref\source.mp4", '--at', '1.0,2.2,4.2,5.2,6.2,8.2,9.2,10.6,11.2,12.3,14.5', '--to', "$ev\full")
Hy '04g_tile_proc' @('media', 'tile', "$ref\source.mp4", '--start', '7.2', '--end', '10.4', '--every', '0.2', '--columns', '4', '--cell', '400', '--transcript', $tx, '--to', "$ev\process.jpg")
'===== list'
Get-ChildItem -Recurse $ev | Select-Object FullName, Length | Format-Table -AutoSize | Out-String -Width 200
