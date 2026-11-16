$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$proj = 'D:\oss_eval\hypit\proj_serum'
Set-Location $proj
$env:NO_COLOR = '1'
'===== npm install dev tools + font'
& npm install -D typescript@5.9.3 '@types/node@24.10.1' --no-audit --no-fund 2>&1 | Select-Object -Last 4 | ForEach-Object { "$_" }
& npm install '@fontsource/nanum-pen-script' --no-audit --no-fund 2>&1 | Select-Object -Last 4 | ForEach-Object { "$_" }
'===== tsc build'
& npx tsc -p 'packages\addirect-scenes\tsconfig.json' 2>&1 | Select-Object -First 60 | ForEach-Object { "$_" }
"tsc exit=$LASTEXITCODE"
Get-ChildItem 'packages\addirect-scenes\dist' -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name
'===== link package'
& npm install 'file:packages/addirect-scenes' --no-audit --no-fund 2>&1 | Select-Object -Last 4 | ForEach-Object { "$_" }
Get-Content package.json
'===== vocabulary'
& (Join-Path $proj 'node_modules\.bin\hypit.cmd') vocabulary '@ptbwa/addirect-scenes' 2>&1 | Select-Object -First 40 | ForEach-Object { "$_" }
