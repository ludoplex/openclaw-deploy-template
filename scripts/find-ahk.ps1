Get-ChildItem "C:\Program Files\AutoHotkey" -Recurse -Filter "*.exe" -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem "$env:LOCALAPPDATA\Programs" -Recurse -Filter "*autohotkey*.exe" -ErrorAction SilentlyContinue | Select-Object FullName
where.exe autohotkey* 2>$null
