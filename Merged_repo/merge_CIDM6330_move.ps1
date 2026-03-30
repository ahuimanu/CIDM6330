$src = "CIDM6330"
$root = (Get-Location).Path
$backup = Join-Path $root ("CIDM6330_backup_{0}" -f (Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
$srcRoot = (Get-Item $src).FullName
Get-ChildItem -LiteralPath $src -File -Recurse -Force | ForEach-Object {
    $item = $_
    $relative = $item.FullName.Substring($srcRoot.Length + 1)
    $dest = Join-Path $root $relative
    $destDir = Split-Path $dest -Parent
    if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    if (Test-Path $dest) {
        $srcTime = (Get-Item $item.FullName).LastWriteTimeUtc
        $dstTime = (Get-Item $dest).LastWriteTimeUtc
        if ($srcTime -gt $dstTime) {
            $backupPath = Join-Path $backup $relative
            $backupDir = Split-Path $backupPath -Parent
            if (!(Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir -Force | Out-Null }
            Move-Item -Force -LiteralPath $dest -Destination $backupPath
            Move-Item -Force -LiteralPath $item.FullName -Destination $dest
        } else {
            $backupPath = Join-Path $backup $relative
            $backupDir = Split-Path $backupPath -Parent
            if (!(Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir -Force | Out-Null }
            Move-Item -Force -LiteralPath $item.FullName -Destination $backupPath
        }
    } else {
        Move-Item -Force -LiteralPath $item.FullName -Destination $dest
    }
}
# Optionally remove empty directories under CIDM6330 (only if empty)
Get-ChildItem -LiteralPath $src -Directory -Recurse -Force | Sort-Object FullName -Descending | ForEach-Object {
    if (-not (Get-ChildItem -LiteralPath $_.FullName -Force -Recurse -ErrorAction SilentlyContinue)) {
        Remove-Item -LiteralPath $_.FullName -Force -Recurse -ErrorAction SilentlyContinue
    }
}
# If CIDM6330 is now empty, remove it
if (-not (Get-ChildItem -LiteralPath $src -Force -Recurse -ErrorAction SilentlyContinue)) {
    Remove-Item -LiteralPath $src -Force -Recurse -ErrorAction SilentlyContinue
}
