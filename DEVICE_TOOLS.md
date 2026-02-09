# DEVICE_TOOLS.md - Local Device Utilities Inventory

**Machine:** DESKTOP-7KTB236  
**OS:** Windows 11 (10.0.26200)  
**Updated:** 2026-02-08  

All agents should reference this file to find local utilities.

---

## 🔧 Key Development Tools

| Tool | Path | Notes |
|------|------|-------|
| Python 3.12 | `C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe` | Primary interpreter |
| pip | `C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\pip.exe` | Package manager |
| Node.js 24 | `C:\Program Files\nodejs\node.exe` | JavaScript runtime |
| npm | `C:\Program Files\nodejs\npm.ps1` | Node package manager |
| Bun | `C:\Users\user\.bun\bin\bun.exe` | Fast JS runtime |
| Git | `C:\Program Files\Git\mingw64\bin\git.exe` | Version control |
| GitHub CLI | `C:\Program Files\GitHub CLI\gh.exe` | GitHub API |
| Docker | `C:\Program Files\Docker\Docker\resources\bin\docker.exe` | Containers |
| Go 1.25 | `C:\Program Files\Go\bin\go.exe` | Go compiler |
| .NET 8 | `C:\Program Files\dotnet\dotnet.exe` | .NET runtime |

## 🗄️ Cloud Storage

### OneDrive (Desktop App)
- **Executable:** `C:\Users\user\AppData\Local\Microsoft\OneDrive\OneDrive.exe`
- **Settings:** `C:\Users\user\AppData\Local\Microsoft\OneDrive\settings\`
- **Sync Folder:** `C:\Users\user\OneDrive`
- **Accounts:**
  - Personal (synced)
  - Business1 (configured but NOT syncing locally)
- **Status:** ✅ Running

### Google Drive (Desktop App)
- **Executable:** `C:\Program Files\Google\Drive File Stream\*` (GoogleDriveFS)
- **Sync Folder:** `C:\Users\user\Google Drive\My Drive`
- **Process:** GoogleDriveFS (running)
- **Status:** ✅ Running

### IBM Cloud Drive
- **Status:** ❌ NOT FOUND - May require separate login/config
- **Action:** Check IBM PartnerWorld for cloud storage access

### rclone (Cloud CLI)
- **Status:** ✅ INSTALLED
- **Path:** `C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.73.0-windows-amd64\rclone.exe`
- **Config:** `C:\Users\user\AppData\Roaming\rclone\rclone.conf`
- **Use for:** CLI access to OneDrive, Google Drive, S3, IBM Cloud, etc.
- **Setup needed:** Run `rclone config` to add OneDrive/Google Drive remotes (OAuth flow required)

## 🌐 Web & Browser Automation

| Tool | Path | Notes |
|------|------|-------|
| Playwright | `C:\Users\user\AppData\Local\Programs\Python\Python312\Scripts\playwright.exe` | Browser automation |
| Chrome | Installed | Via OpenClaw relay or Playwright |
| Chromium | `C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Nicegram.nicegram\Nicegram.app\Contents\Frameworks\nicegram_browser.framework\Versions\A\Helpers\nicegram_browser.app\Contents\MacOS\nicegram_browser` | Headless option |
| nmap | `C:\Program Files (x86)\Nmap\nmap.exe` | Network scanner |

## 📁 File Utilities

| Tool | Path | Notes |
|------|------|-------|
| 7-Zip | `C:\Program Files\7-Zip\7z.exe` | Compression |
| ffmpeg | `C:\Users\user\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe` | Media processing |
| pdftotext | `C:\Program Files\Git\mingw64\bin\pdftotext.exe` | PDF extraction |
| sqlite3 | `C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\SQLite.SQLite_*\tools\sqlite3.exe` | Database CLI |
| File Pilot | `C:\Users\user\AppData\Local\Voidstar\FilePilot\FPilot.exe` | File manager |

## 🔐 Security & SSH

| Tool | Path | Notes |
|------|------|-------|
| SSH | `C:\Program Files\Git\usr\bin\ssh.exe` | SSH client |
| OpenSSH | `C:\WINDOWS\System32\OpenSSH\ssh.exe` | Windows native |
| Tailscale | `C:\Program Files\Tailscale\tailscale.exe` | VPN mesh |
| 1Password | `C:\Users\user\AppData\Local\Microsoft\WindowsApps\1Password.exe` | Password manager |
| GPG | `C:\Program Files\Git\usr\bin\gpg.exe` | Encryption |

## 🎮 Gaming/LAN Center

| Tool | Path | Notes |
|------|------|-------|
| ggLeap | Installed | LAN center management |
| Steam | Installed | Gaming platform |
| Discord | `C:\Users\user\AppData\Local\Discord\*` | Communication |
| Cemu | `C:\Users\user\AppData\Local\Microsoft\WinGet\Links\Cemu.exe` | Wii U emulator |

## 🤖 AI/ML Tools

| Tool | Path | Notes |
|------|------|-------|
| llamafile | `C:\Users\user\.openclaw\workspace\bin\llamafile.exe` | Local LLM |
| Qwen 2.5 7B | `C:\Users\user\.openclaw\workspace\models\qwen2.5-7b-instruct-q3_k_m.gguf` | Local model |
| Jan | Installed | Local AI chat |
| Claude Code | `C:\Users\user\.local\bin\claude.exe` | Anthropic CLI |
| OpenCode | Installed | Code assistant |
| Cursor | `C:\Program Files\cursor\*` | AI IDE |

## 📦 Package Managers

| Tool | Path | Notes |
|------|------|-------|
| winget | `C:\Users\user\AppData\Local\Microsoft\WindowsApps\winget.exe` | Windows packages |
| pip | See Python section | Python packages |
| npm | See Node section | Node packages |
| nuget | `C:\Users\user\AppData\Local\Microsoft\WinGet\Packages\Microsoft.NuGet_*\nuget.exe` | .NET packages |

## 🐧 WSL/Linux

| Tool | Path | Notes |
|------|------|-------|
| WSL | `C:\WINDOWS\system32\wsl.exe` | Windows Subsystem Linux |
| Ubuntu 22.04 | `C:\Users\user\AppData\Local\Microsoft\WindowsApps\ubuntu2204.exe` | Ubuntu distro |

## 📊 Business/Office

| Tool | Path | Notes |
|------|------|-------|
| LibreOffice | Installed | Office suite |
| Perfect Memory | Installed | Note-taking |
| HandBrake | Installed | Video transcoding |

## 🔌 IDEs & Editors

| Tool | Path | Notes |
|------|------|-------|
| CLion | `C:\Program Files\JetBrains\CLion 2025.3.1\bin\clion64.exe` | C/C++ IDE |
| Cursor | `C:\Program Files\cursor\*` | AI Code Editor |
| VS Code | Not found in PATH | May need install |
| Android Studio | Installed | Android dev |

## ⚠️ MISSING - RECOMMENDED INSTALLS

```powershell
# Cloud storage CLI (CRITICAL for cloud access)
winget install rclone.rclone

# VS Code (if not installed)
winget install Microsoft.VisualStudioCode

# AWS CLI (for S3/cloud)
winget install Amazon.AWSCLI

# Azure CLI
winget install Microsoft.AzureCLI
```

---

## 🔧 Usage Examples

### Access OneDrive via CLI (after rclone install)
```powershell
# Configure OneDrive remote
rclone config
# Choose: onedrive → follow OAuth flow

# List files
rclone ls onedrive:

# Search for EIN documents
rclone ls onedrive: --include "*ein*" --include "*tax*" --include "*SS-4*"

# Download specific folder
rclone copy onedrive:Legal ./local-legal/
```

### Access Google Drive via CLI (after rclone install)
```powershell
# Configure Google Drive remote
rclone config
# Choose: drive → follow OAuth flow

# List files
rclone ls gdrive:

# Search files
rclone ls gdrive: --include "*mhi*" --include "*mighty*"
```

### Use Playwright for automation
```powershell
# Run with persistent state
playwright codegen --save-storage=state.json https://onedrive.live.com
```

---

*Updated by agents as new tools are discovered/installed.*
