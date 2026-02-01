# Backup Information

## Mighty House Inc. SOP Repository

---

## 🚀 Quick Actions (Double-Click These)

| File | Action |
|------|--------|
| `SETUP-GIT.bat` | First-time setup → Creates Git repo and pushes to GitHub |
| `SYNC.bat` | Daily use → Pull, commit, push all changes |
| `BACKUP.bat` | Create local ZIP backup in ~/Backups folder |

---

## Repository Locations

### Primary (GitHub - Remote Backup)

| Property | Value |
|----------|-------|
| **Repository** | `mighty-house-sops` |
| **Visibility** | Private |
| **URL** | `https://github.com/ludoplex/mighty-house-sops` |

### Local Working Copy

**Path:** `c:\Users\user\Downloads\Cursor_working_directory_misc\mighty-house-sops`

### Local ZIP Backups

**Path:** `C:\Users\YOUR_USER\Backups\mighty-house-sops-YYYY-MM-DD.zip`

---

## 📋 Setup Instructions (One-Time)

### Step 1: Run Setup
```
Double-click: SETUP-GIT.bat
```

This will:
1. Initialize Git repository
2. Create local ZIP backup
3. Create private GitHub repository
4. Push all files to GitHub

### Step 2: Verify
After setup, check your GitHub account - you should see `mighty-house-sops` in your repositories.

---

## 🔄 Daily Workflow

### Before Starting Work
```
Double-click: SYNC.bat
```
(This pulls any changes from other devices)

### After Making Changes
```
Double-click: SYNC.bat
```
(This commits and pushes your changes)

### Command Line Alternative
```powershell
.\sync.ps1 "Description of changes"
```

---

## 💻 Clone to New Device

### Prerequisites
1. Install Git: https://git-scm.com/downloads
2. Install GitHub CLI: https://cli.github.com/
3. Login: `gh auth login`

### Clone
```powershell
git clone https://github.com/ludoplex/mighty-house-sops.git
```

---

## 📦 Backup Schedule

| Backup Type | Frequency | How | Location |
|-------------|-----------|-----|----------|
| Git Push | After each change | `SYNC.bat` | GitHub (cloud) |
| Local ZIP | Weekly | `BACKUP.bat` | ~/Backups folder |
| External | Monthly | Copy ZIP to USB | External drive |

---

## 🆘 Recovery Options

### From GitHub (Preferred)
```powershell
git clone https://github.com/ludoplex/mighty-house-sops.git
```

### From Local ZIP
```powershell
Expand-Archive -Path "$env:USERPROFILE\Backups\mighty-house-sops-DATE.zip" -DestinationPath "C:\RecoveryLocation"
```

---

## 📁 What's Included

| Folder/File | Contents |
|-------------|----------|
| `sops/` | All 48 Standard Operating Procedures |
| `appendices/` | 8 print-ready appendices |
| `locations/` | Location-specific documents |
| `templates/` | SOP and document templates |
| `marketing-prompts.md` | 124 Canva & Sora 2 prompts |
| `sora2-generation-plan.md` | Video generation strategy |
| `canva-platform-variations.md` | Platform-specific graphics |
| `content-calendar.md` | Annual posting schedule |

---

## 🔧 Troubleshooting

### "Not a git repository"
Run `SETUP-GIT.bat` first

### "GitHub CLI not authenticated"
```powershell
gh auth login
```

### "Updates were rejected"
```powershell
git pull origin main --rebase
git push origin main
```

### Check current status
```powershell
git status
git remote -v
gh auth status
```

---

*Last Updated: December 2024*
*See GIT-INSTRUCTIONS.md for detailed manual instructions*
