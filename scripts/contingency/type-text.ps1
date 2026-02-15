# Type text into the currently focused window
param(
    [string]$Text = "Hello from Peridot",
    [switch]$Enter
)

Add-Type -AssemblyName System.Windows.Forms
Start-Sleep -Milliseconds 200

# Escape special characters for SendKeys
$escaped = $Text -replace '[\+\^\%\~\(\)\{\}\[\]]', '{$0}'

[System.Windows.Forms.SendKeys]::SendWait($escaped)

if ($Enter) {
    Start-Sleep -Milliseconds 100
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
}

Write-Host "Typed: $Text"
