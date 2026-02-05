---
name: ad-powershell
description: ActiveDirectory cmdlets. User/group/OU ops. LDAP filters.
metadata: { "openclaw": { "requires": { "bins": ["pwsh"] } } }
---

# AD PowerShell

## Import
```powershell
Import-Module ActiveDirectory
```

## User Ops
```powershell
# Create
New-ADUser -Name "J Doe" -SamAccountName jdoe -UserPrincipalName jdoe@domain.com -Enabled $true -AccountPassword (Read-Host -AsSecureString)

# Unlock/Reset
Unlock-ADAccount -Identity jdoe
Set-ADAccountPassword -Identity jdoe -Reset -NewPassword (ConvertTo-SecureString "P@ss" -AsPlainText -Force)

# Disable
Disable-ADAccount -Identity jdoe
```

## Group Ops
```powershell
Add-ADGroupMember -Identity "IT Staff" -Members jdoe
Get-ADGroupMember -Identity "Domain Admins" -Recursive
```

## Queries
```powershell
# LDAP filter
Get-ADUser -Filter {Enabled -eq $false} -Properties LastLogonDate
Get-ADUser -LDAPFilter "(memberOf=CN=IT,OU=Groups,DC=domain,DC=com)"

# OU scope
Get-ADUser -SearchBase "OU=Sales,DC=domain,DC=com" -Filter *
```

## Gotchas
- Run as admin or use `-Credential`
- `-WhatIf` for dry run
- Replication delay: wait 15min cross-site
