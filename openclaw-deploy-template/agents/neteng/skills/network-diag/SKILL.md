---
name: network-diag
description: Network diagnostics. ping/tracert/nslookup/Test-NetConnection.
---

# Network Diagnostics

## Connectivity
```powershell
Test-NetConnection -ComputerName host -Port 443
Test-Connection -ComputerName host -Count 4

# Unix
ping -c 4 host
nc -zv host 443
```

## Routing
```powershell
Test-NetConnection -ComputerName host -TraceRoute
tracert host  # Windows
traceroute host  # Unix
```

## DNS
```powershell
Resolve-DnsName host -Type A
nslookup -type=MX domain.com 8.8.8.8
```

## Quick Checks
| Issue | Command |
|-------|---------|
| Port blocked | `tnc host -Port 443` |
| DNS fail | `Resolve-DnsName host` |
| Latency | `Test-Connection host` |
| Route | `tracert host` |
| Local IP | `Get-NetIPAddress -AddressFamily IPv4` |

## Gotchas
- `tnc` = alias for Test-NetConnection
- ICMP may be blocked; use TCP test
- Check both internal DNS and 8.8.8.8
