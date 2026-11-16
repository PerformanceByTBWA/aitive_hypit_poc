$ProgressPreference = 'SilentlyContinue'
$src = 'D:\oss_eval\hypit\proj_serum\references\v1012\source.mp4'
foreach ($r in @(@('0', '1.5'), @('4.40', '4.70'), @('6.65', '7.30'), @('9.70', '10.35'), @('12.30', '12.60'), @('14.50', '15.0'), @('1.7', '4.3'))) {
  $o = & ffmpeg -hide_banner -nostats -ss $r[0] -to $r[1] -i $src -vn -af 'volumedetect' -f null NUL 2>&1 | Select-String -Pattern 'mean_volume|max_volume' | ForEach-Object { $_.Line -replace '.*\] ', '' }
  "{0}-{1}s  {2}" -f $r[0], $r[1], ($o -join '  ')
}
