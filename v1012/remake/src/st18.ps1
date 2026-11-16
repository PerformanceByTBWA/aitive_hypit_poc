$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
Set-Location 'D:\oss_eval\hypit\proj_serum'
'===== tsc rebuild'
& npx tsc -p 'packages\addirect-scenes\tsconfig.json' 2>&1 | Select-Object -First 40 | ForEach-Object { "$_" }
"tsc exit=$LASTEXITCODE"
Remove-Item -Force 'out\remake\remake.mp4', 'out\remake\remake_05s.jpg', 'out\remake\remake_web.mp4' -ErrorAction SilentlyContinue
& powershell -NoProfile -ExecutionPolicy Bypass -File 'D:\oss_eval\hypit\st17.ps1'
