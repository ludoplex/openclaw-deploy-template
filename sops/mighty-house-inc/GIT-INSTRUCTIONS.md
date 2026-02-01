# Mighty House SOPs - Git & GitHub Instructions

## 📦 Initial Setup (One-Time)

### Option A: Run the Script (Recommended)
```
Double-click: SETUP-GIT.bat
```

### Option B: Manual Setup

#### Step 1: Open PowerShell in this folder
- Right-click in the folder → "Open in Terminal" or "Open PowerShell window here"

#### Step 2: Initialize Git
```powershell
git init
git add -A
git commit -m "Initial commit: Mighty House SOPs"
```

#### Step 3: Create GitHub Repository
```powershell
# Create private repo and push (requires GitHub CLI)
gh repo create mighty-house-sops --private --source=. --remote=origin --push
```

#### Step 4: Verify
```powershell
git remote -v
# Should show: origin https://github.com/ludoplex/mighty-house-sops.git
```

---

## 🔄 Daily Sync Commands

### Pull Latest Changes (Before Starting Work)
```powershell
git pull origin main
```

### Push Your Changes (After Making Updates)
```powershell
git add -A
git commit -m "Describe what you changed"
git push origin main
```

### Quick Sync Script
```powershell
# Pull, add, commit, push in one go
git pull origin main
git add -A
git commit -m "Update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main
```

---

## 💻 Clone to a New Device

### Prerequisites
1. Install Git: https://git-scm.com/downloads
2. Install GitHub CLI: https://cli.github.com/
3. Login to GitHub CLI: `gh auth login`

### Clone Command
```powershell
# Replace ludoplex with your GitHub username
git clone https://github.com/ludoplex/mighty-house-sops.git
cd mighty-house-sops
```

---

## 📂 Local Backup Locations

| Backup Type | Location |
|-------------|----------|
| Automated (from script) | `C:\Users\YOUR_USER\Backups\mighty-house-sops-DATE.zip` |
| Git History | `.git` folder (automatic with every commit) |
| GitHub | `https://github.com/ludoplex/mighty-house-sops` |

---

## 🆘 Common Issues

### "Not a git repository"
```powershell
git init
```

### "Remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/ludoplex/mighty-house-sops.git
```

### "Updates were rejected"
```powershell
git pull origin main --rebase
git push origin main
```

### "GitHub CLI not authenticated"
```powershell
gh auth login
# Follow prompts, choose HTTPS, authenticate in browser
```

### "Permission denied"
- Make sure you're logged into the correct GitHub account
- Check: `gh auth status`

---

## 📱 Sync on Multiple Devices

### Device 1 (Main/Office)
```powershell
# Make changes, then:
git add -A
git commit -m "Updated SOPs from office"
git push origin main
```

### Device 2 (Laptop/Home)
```powershell
# First, get latest:
git pull origin main

# Make changes, then:
git add -A
git commit -m "Updated from home"
git push origin main
```

### Best Practice
- **Always pull before starting work**
- **Always push when done for the day**
- **Write clear commit messages**

---

## 🗓️ Recommended Backup Schedule

| Frequency | Action |
|-----------|--------|
| Daily | `git push` after any changes |
| Weekly | Run `SETUP-GIT.bat` to create local zip backup |
| Monthly | Download repo as ZIP from GitHub → Save to external drive |

---

## 📋 File Structure

```
mighty-house-sops/
├── README.md              # Main index
├── SETUP-GIT.bat          # One-click setup
├── setup-repo.ps1         # PowerShell setup script
├── GIT-INSTRUCTIONS.md    # This file
├── .gitignore             # Ignored files list
├── sops/                  # All SOP documents
├── appendices/            # Print materials
├── templates/             # Templates
├── checklists/            # Checklists
├── locations/             # Location-specific docs
├── assets/                # Images, logos
├── marketing-prompts.md   # Canva/Sora prompts
├── sora2-generation-plan.md  # Video generation plan
├── canva-platform-variations.md  # Platform graphics
└── content-calendar.md    # Posting schedule
```

---

*Last updated: December 2024*
