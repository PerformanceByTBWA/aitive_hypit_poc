$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:PATH = 'D:\oss_eval\tools\uv-0.13.2;' + $env:PATH
$env:HF_HUB_DISABLE_TELEMETRY = '1'
$env:DO_NOT_TRACK = '1'
$env:NO_COLOR = '1'
$hy = Join-Path $proj 'node_modules\.bin\hypit.cmd'
$io = Join-Path $proj 'references\remake\io'
$out = Join-Path $proj 'out\remake'
New-Item -ItemType Directory -Force $out, $io | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false
function Hy([string]$Label, [string[]]$HyArgs) {
  $t0 = Get-Date
  $lines = & $hy @HyArgs 2>&1 | ForEach-Object { "$_" }
  $script:code = $LASTEXITCODE
  $s = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
  $script:text = ($lines -join "`n")
  "===== $Label exit=$($script:code) sec=$s :: hypit $($HyArgs -join ' ')"
  $lines | Select-Object -Last 45
  [IO.File]::WriteAllText((Join-Path $io "$Label.txt"), ("hypit $($HyArgs -join ' ')`nexit=$($script:code) sec=$s`n" + $script:text), $utf8)
}
Hy 'rm_07a_runtime-use' @('runtime', 'use', '.\hypit.runtime.json')
Hy 'rm_07b_runtime-up' @('runtime', 'up', '--max-wait-ms', '600000')
Hy 'rm_07c_check' @('check', '.\remake.svrun')
Hy 'rm_07d_plan' @('plan', '.\remake.svrun')
Hy 'rm_08_build' @('build', '.\remake.svrun', '--follow', '--max-wait-ms', '1800000')
$ms = [regex]::Matches($script:text, '(bld_[0-9A-Za-z_]+)')
$bid = $null; if ($ms.Count -gt 0) { $bid = $ms[$ms.Count - 1].Groups[1].Value }
"BUILD=$bid"
if ($bid -and $script:code -eq 0) {
  Hy 'rm_11a_get_video' @('get', $bid, '--output', 'final.video', '--to', (Join-Path $out 'remake.mp4'))
  Hy 'rm_11b_inspect' @('inspect', $bid, '--verbose')
}
if ($bid -and $script:code -ne 0) { Hy 'rm_08_logs' @('logs', $bid, '--lines', '80') }
Hy 'rm_11e_runtime-down' @('runtime', 'down')
Hy 'rm_11f_programs-down' @('programs', 'down')
if (Test-Path (Join-Path $out 'remake.mp4')) {
  & $hy media tile (Join-Path $out 'remake.mp4') --start 0 --end 15 --every 0.5 --columns 6 --to (Join-Path $out 'remake_05s.jpg') 2>&1 | ForEach-Object { "$_" }
  & ffmpeg -y -v error -i (Join-Path $out 'remake.mp4') -vf 'scale=960:-2' -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart (Join-Path $out 'remake_web.mp4')
  & ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames:format=duration,size -of compact=p=0 (Join-Path $out 'remake.mp4')
}
