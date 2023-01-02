
# Set working dir to ps1 script
$dir = Split-Path -Path (Resolve-Path $PSCommandPath)
Set-Location -Path $dir

Remove-Item 'music' -Force -Recurse 2>$null
Remove-Item 'music-backup'  -Force -Recurse 2>$null
Copy-Item 'original-music-files' 'music' -Recurse