$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:PATH = 'D:\oss_eval\tools\uv-0.13.2;' + $env:PATH
$env:HF_HUB_DISABLE_TELEMETRY = '1'
$env:DO_NOT_TRACK = '1'
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$ref = 'references\v1012'
$io = Join-Path $proj "$ref\io"
$out = Join-Path $proj "out\v1012"
New-Item -ItemType Directory -Force $out | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
function Hy([string]$Label, [string[]]$HyArgs) {
  $t0 = Get-Date
  $lines = & $hy @HyArgs 2>&1 | ForEach-Object { "$_" }
  $script:code = $LASTEXITCODE
  $s = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
  $script:text = ($lines -join "`n")
  "===== $Label exit=$($script:code) sec=$s :: hypit $($HyArgs -join ' ')"
  $lines
  [IO.File]::WriteAllText((Join-Path $io "$Label.txt"), ("hypit $($HyArgs -join ' ')`nexit=$($script:code) sec=$s`n" + $script:text), $utf8)
}
Hy '07a_runtime-use' @('runtime', 'use', '.\hypit.runtime.json')
Hy '07b_runtime-up' @('runtime', 'up', '--max-wait-ms', '600000')
Hy '07c_check' @('check', '.\v1012.svrun')
if ($script:code -eq 0) {
  Hy '07d_plan' @('plan', '.\v1012.svrun')
  Hy '08_build' @('build', '.\v1012.svrun', '--follow', '--max-wait-ms', '1800000')
  $ms = [regex]::Matches($script:text, '(bld_[0-9A-Za-z_]+)')
  $bid = $null; if ($ms.Count -gt 0) { $bid = $ms[$ms.Count - 1].Groups[1].Value }
  "BUILD=$bid"
  if ($bid) {
    Hy '11a_get_video' @('get', $bid, '--output', 'final.video', '--to', (Join-Path $out 'v1012_replica.mp4'))
    Hy '11b_inspect' @('inspect', $bid, '--verbose')
    Hy '11c_get_alignment' @('get', $bid, '--output', 'ad-semantic.alignment', '--to', (Join-Path $out 'alignment'))
  }
}
Hy '11d_runtime-down' @('runtime', 'down')
Hy '11e_programs-down' @('programs', 'down')
'===== ffprobe'
Get-ChildItem $out -Filter *.mp4 | ForEach-Object { & ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration,size -of compact=p=0 $_.FullName }
'===== leftover'
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'whisperx|hypit|chrome-headless-shell' } | ForEach-Object { "{0} {1}" -f $_.ProcessId, $_.Name }
