# Check for remote access tools
Write-Host "=== Running Processes ===" 
Get-Process | Where-Object { $_.ProcessName -match 'teamviewer|anydesk|parsec|rustdesk' } | Select-Object ProcessName, Id

Write-Host "`n=== Installed Remote Tools ==="
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue | 
    Where-Object { $_.DisplayName -match 'TeamViewer|AnyDesk|Chrome Remote|Parsec|RustDesk|Remote' } | 
    Select-Object DisplayName

Write-Host "`n=== RDP Status ==="
Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections -ErrorAction SilentlyContinue
