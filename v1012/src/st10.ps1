$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:PATH = 'D:\oss_eval\tools\uv-0.13.2;' + $env:PATH
$env:HF_HUB_DISABLE_TELEMETRY = '1'
$env:DO_NOT_TRACK = '1'
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$io = Join-Path $proj 'references\v1012\io'
$out = Join-Path $proj 'out\v1012_gen'
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
'===== gpu'
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader
Hy 'gen_09_probe' @('media', 'probe', 'references\v1012\gen\seedance_raw.mp4', '--json')
Hy 'gen_07a_runtime-use' @('runtime', 'use', '.\hypit.runtime.json')
Hy 'gen_07b_runtime-up' @('runtime', 'up', '--max-wait-ms', '600000')
Hy 'gen_07c_check' @('check', '.\v1012_gen.svrun')
if ($script:code -eq 0) {
  Hy 'gen_07d_plan' @('plan', '.\v1012_gen.svrun')
  Hy 'gen_08_build' @('build', '.\v1012_gen.svrun', '--follow', '--max-wait-ms', '1800000')
  $ms = [regex]::Matches($script:text, '(bld_[0-9A-Za-z_]+)')
  $bid = $null; if ($ms.Count -gt 0) { $bid = $ms[$ms.Count - 1].Groups[1].Value }
  "BUILD=$bid"
  if ($bid) {
    Hy 'gen_11a_get_video' @('get', $bid, '--output', 'final.video', '--to', (Join-Path $out 'v1012_gen.mp4'))
    Hy 'gen_11b_inspect' @('inspect', $bid, '--verbose')
    Hy 'gen_11c_get_gen_extent' @('get', $bid, '--output', 'gen-media.extent', '--to', (Join-Path $out 'gen-media_extent'))
    Hy 'gen_11d_get_caption_timing' @('get', $bid, '--output', 'caption-timing', '--to', (Join-Path $out 'caption-timing'))
  }
}
Hy 'gen_11e_runtime-down' @('runtime', 'down')
Hy 'gen_11f_programs-down' @('programs', 'down')
if (Test-Path (Join-Path $out 'v1012_gen.mp4')) {
  & $hy media tile (Join-Path $out 'v1012_gen.mp4') --start 0 --end 15 --every 0.5 --columns 6 --transcript 'references\v1012\transcript.json' --to (Join-Path $out 'gen_05s.jpg') 2>&1 | ForEach-Object { "$_" }
  & $hy media frames (Join-Path $out 'v1012_gen.mp4') --at '0.6,2.0,3.6,6.8' --to (Join-Path $out 'gen_full') 2>&1 | ForEach-Object { "$_" }
  & ffmpeg -y -v error -i (Join-Path $out 'v1012_gen.mp4') -vf 'scale=960:-2' -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart (Join-Path $out 'v1012_gen_web.mp4')
  & ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration,size -of compact=p=0 (Join-Path $out 'v1012_gen.mp4')
}
'===== leftover'
(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'whisperx|hypit|chrome-headless-shell' } | Measure-Object).Count
