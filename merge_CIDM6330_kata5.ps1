$src = "CIDM6330\Katas\Kata5"
$root = (Get-Location).Path
$backup = Get-ChildItem -Path $root -Directory | Where-Object { $_.Name -like 'CIDM6330_backup_*' } | Select-Object -First 1
if (-not $backup) { $backup = Join-Path $root ("CIDM6330_backup_{0}" -f (Get-Date -Format "yyyyMMdd_HHmmss")); New-Item -ItemType Directory -Path $backup -Force | Out-Null } else { $backup = $backup.FullName }
$srcRoot = (Get-Item $src).FullName
Get-ChildItem -LiteralPath $src -File -Recurse -Force | ForEach-Object {
    $item = $_
    $relative = $item.FullName.Substring($srcRoot.Length + 1)
    $dest = Join-Path $root "Katas\Kata5\$relative"
    $destDir = Split-Path $dest -Parent
    if (!(Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    if (Test-Path $dest) {
        $srcTime = (Get-Item $item.FullName).LastWriteTimeUtc
        $dstTime = (Get-Item $dest).LastWriteTimeUtc
        if ($srcTime -gt $dstTime) {
            $backupPath = Join-Path $backup "Katas\Kata5\$relative"
            $backupDir = Split-Path $backupPath -Parent
            if (!(Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir -Force | Out-Null }
            Move-Item -Force -LiteralPath $dest -Destination $backupPath
            Move-Item -Force -LiteralPath $item.FullName -Destination $dest
        } else {
            $backupPath = Join-Path $backup "Katas\Kata5\$relative"
            $backupDir = Split-Path $backupPath -Parent
            if (!(Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir -Force | Out-Null }
            Move-Item -Force -LiteralPath $item.FullName -Destination $backupPath
        }
    } else {
        Move-Item -Force -LiteralPath $item.FullName -Destination $dest
    }
}
# remove empty dirs under CIDM6330\Katas\Kata5
Get-ChildItem -LiteralPath $src -Directory -Recurse -Force | Sort-Object FullName -Descending | ForEach-Object {
    if (-not (Get-ChildItem -LiteralPath $_.FullName -Force -Recurse -ErrorAction SilentlyContinue)) {
        Remove-Item -LiteralPath $_.FullName -Force -Recurse -ErrorAction SilentlyContinue
    }
}
# if CIDM6330 now empty, remove it
if (-not (Get-ChildItem -LiteralPath "CIDM6330" -Force -Recurse -ErrorAction SilentlyContinue)) { Remove-Item -LiteralPath "CIDM6330" -Force -Recurse -ErrorAction SilentlyContinue }
