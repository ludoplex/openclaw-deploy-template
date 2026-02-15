# jsonl-to-md.ps1
# Converts OpenClaw/Claude JSONL session transcripts to searchable Markdown
# Handles: type="message" with message.role and message.content arrays

param(
    [string]$Path = "C:\Users\user\.openclaw\agents",
    [string]$OutDir = "C:\Users\user\.openclaw\workspace\session-transcripts"
)

New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

$files = Get-ChildItem -Path $Path -Recurse -Filter "*.jsonl" -ErrorAction SilentlyContinue

Write-Host "Found $($files.Count) JSONL files"

foreach ($file in $files) {
    $relativePath = $file.FullName.Substring($Path.Length).TrimStart('\')
    $mdName = $relativePath -replace '[\\/]', '_' -replace '\.jsonl$', '.md'
    $outFile = Join-Path $OutDir $mdName
    
    Write-Host "Converting: $($file.Name)"
    
    try {
        $content = @("# Session Transcript: $($file.Name)", "", "Source: ``$($file.FullName)``", "")
        $messageCount = 0
        
        Get-Content $file.FullName | ForEach-Object {
            try {
                $json = $_ | ConvertFrom-Json
                
                # Handle OpenClaw message format
                if ($json.type -eq "message" -and $json.message) {
                    $role = $json.message.role
                    $msgContent = $json.message.content
                    
                    if ($role -and $msgContent) {
                        $roleUpper = $role.ToUpper()
                        $text = ""
                        
                        # Content can be array or string
                        if ($msgContent -is [array]) {
                            foreach ($item in $msgContent) {
                                if ($item.type -eq "text" -and $item.text) {
                                    $text += $item.text + "`n"
                                }
                                elseif ($item.type -eq "thinking" -and $item.thinking) {
                                    $text += "<thinking>`n$($item.thinking)`n</thinking>`n"
                                }
                            }
                        } else {
                            $text = $msgContent.ToString()
                        }
                        
                        if ($text.Trim()) {
                            $content += "## $roleUpper"
                            $content += ""
                            $content += $text.Trim()
                            $content += ""
                            $messageCount++
                        }
                    }
                }
                # Handle simpler role/content format
                elseif ($json.role -and $json.content) {
                    $role = $json.role.ToUpper()
                    $text = if ($json.content -is [array]) {
                        ($json.content | Where-Object { $_.type -eq 'text' } | ForEach-Object { $_.text }) -join "`n"
                    } else {
                        $json.content.ToString()
                    }
                    
                    if ($text.Trim()) {
                        $content += "## $role"
                        $content += ""
                        $content += $text.Trim()
                        $content += ""
                        $messageCount++
                    }
                }
            } catch {
                # Skip malformed lines
            }
        }
        
        if ($messageCount -gt 0) {
            $content | Out-File -FilePath $outFile -Encoding UTF8
            Write-Host "  -> $outFile ($messageCount messages)"
        } else {
            Write-Host "  SKIPPED (no messages)"
        }
    } catch {
        Write-Host "  ERROR: $_" -ForegroundColor Red
    }
}

Write-Host "`nConverted to: $OutDir"
