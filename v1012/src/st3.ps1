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
$utf8 = New-Object System.Text.UTF8Encoding $false
function Hy([string]$Label, [string[]]$HyArgs) {
  $t0 = Get-Date
  $lines = & $hy @HyArgs 2>&1 | ForEach-Object { "$_" }
  $c = $LASTEXITCODE
  $s = [math]::Round(((Get-Date) - $t0).TotalSeconds, 1)
  "===== $Label exit=$c sec=$s :: hypit $($HyArgs -join ' ')"
  $lines
  [IO.File]::WriteAllText((Join-Path $proj "$ref\io\$Label.txt"), ("hypit $($HyArgs -join ' ')`nexit=$c sec=$s`n" + ($lines -join "`n")), $utf8)
}
Hy '02a_runtime-use' @('runtime', 'use', '.\hypit.runtime.json')
Hy '02b_runtime-up' @('runtime', 'up', '--max-wait-ms', '600000')
Hy '02c_doctor' @('doctor')
Hy '02d_transcribe' @('transcribe', "$ref\source.mp4", '--language', 'ko', '--to', "$ref\transcript.json")
Hy '02e_runtime-down' @('runtime', 'down')
Hy '02f_programs-down' @('programs', 'down')
'===== leftover'
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'whisperx|hypit|chrome-headless-shell' } | ForEach-Object { "{0} {1}" -f $_.ProcessId, $_.Name }
