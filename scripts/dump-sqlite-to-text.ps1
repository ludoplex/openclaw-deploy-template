# dump-sqlite-to-text.ps1
# Dumps all SQLite databases to indexable text files
# Usage: .\dump-sqlite-to-text.ps1 -Path "C:\Users\user\.cursor"

param(
    [string]$Path = "C:\Users\user",
    [string]$OutDir = "C:\Users\user\.openclaw\workspace\sqlite-dumps"
)

# Create output directory
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

# Find all SQLite files
$files = Get-ChildItem -Path $Path -Recurse -Include "*.db","*.sqlite","*.sqlite3","*.vcsdb" -ErrorAction SilentlyContinue

Write-Host "Found $($files.Count) SQLite files"

foreach ($file in $files) {
    $safeName = $file.FullName -replace '[\\/:*?"<>|]', '_'
    $outFile = Join-Path $OutDir "$safeName.sql"
    
    Write-Host "Dumping: $($file.FullName)"
    
    try {
        # Dump schema and data
        & sqlite3 $file.FullName ".dump" | Out-File -FilePath $outFile -Encoding UTF8
        
        # Also dump as readable tables
        $tablesFile = Join-Path $OutDir "$safeName.tables.txt"
        $tables = & sqlite3 $file.FullName ".tables"
        
        $output = @()
        foreach ($table in ($tables -split '\s+' | Where-Object { $_ })) {
            $output += "=== TABLE: $table ==="
            $output += (& sqlite3 -header -column $file.FullName "SELECT * FROM $table LIMIT 1000;")
            $output += ""
        }
        $output | Out-File -FilePath $tablesFile -Encoding UTF8
        
        Write-Host "  -> $outFile"
    } catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
    }
}

Write-Host "`nDumps written to: $OutDir"
Write-Host "Add this path to memorySearch.extraPaths for indexing"
