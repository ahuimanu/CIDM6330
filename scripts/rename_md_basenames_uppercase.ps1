# Rename Markdown files: uppercase basenames, preserve extension
# Usage (PowerShell from repo root):
#   .\scripts\rename_md_basenames_uppercase.ps1

$files = Get-ChildItem -Recurse -File -Include *.md,*.MD
foreach ($f in $files) {
  $dir = $f.DirectoryName
  $newName = $f.BaseName.ToUpper() + $f.Extension
  $newPath = Join-Path $dir $newName
  if ($f.FullName -ne $newPath) {
    Write-Host "Renaming: $($f.FullName) -> $newPath"
    $tmp = Join-Path $dir ("tmp-"+[guid]::NewGuid().ToString())
    Move-Item -LiteralPath $f.FullName -Destination $tmp
    Move-Item -LiteralPath $tmp -Destination $newPath
  }
}
Write-Host "Done."