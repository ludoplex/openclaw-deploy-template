# LAN Inventory - 192.168.1.0/24

**Last Scan:** 2026-02-05 23:03 MST
**Scanner:** nmap 7.80 (-sV --top-ports 100)
**Results:** 9 targets, 8 hosts up

---

## Network Devices

### 192.168.1.1 — Router (Netgear ProRouter)
- **Hostname:** device.lan
- **MAC:** 28:94:01:3B:AC:61
- **Services:**
  - 53/tcp — DNS
  - 80/tcp — HTTP (lighttpd 1.4.55)
  - 443/tcp — HTTPS (lighttpd 1.4.55)
  - 5000/tcp — UPnP (MiniUPnPd 2.3.1)

### 192.168.1.233 — TP-Link Access Point (ArcherC54)
- **Hostname:** ArcherC54.lan
- **MAC:** 3C:6A:D2:3F:95:C4
- **Services:**
  - 22/tcp — SSH (OpenSSH 6.6.0) ❌ UNUSABLE
  - 80/tcp — HTTP
  - 443/tcp — HTTPS
  - 1900/tcp — UPnP
- **SSH Status:** Only offers `ssh-dss` + `diffie-hellman-group1-sha1` — deprecated crypto, modern clients refuse to connect
- **Tested:** 2026-02-05 — Windows OpenSSH cannot negotiate
- **Recommendation:** Flash OpenWrt — https://openwrt.org/toh/tp-link/archer_c54

---

## Computers

### 192.168.1.28 — Windows PC
- **Hostname:** DESKTOP-6FPF6DO.lan
- **MAC:** 9C:6B:00:68:8B:0E
- **OS:** Windows
- **Services:**
  - 22/tcp — SSH (OpenSSH for Windows 9.5) ✅
  - 135/tcp — MSRPC
  - 139/tcp — NetBIOS
  - 445/tcp — SMB
  - 5357/tcp — HTTPAPI (SSDP/UPnP)
- **SSH Status:** ✅ Auth works (user/password), but cmd.exe disabled by policy
- **Fix needed:** Set PowerShell as default SSH shell: `New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force`
- **Tested:** 2026-02-05

### 192.168.1.66 — Windows PC
- **Hostname:** DESKTOP-01KC04G.lan
- **MAC:** 9C:6B:00:6B:1F:91
- **OS:** Windows
- **Services:**
  - 135/tcp — MSRPC
  - 445/tcp — SMB
  - 5357/tcp — HTTPAPI (SSDP/UPnP)
- **Note:** 97 filtered ports (firewall active)

### 192.168.1.223 — Windows PC
- **Hostname:** DESKTOP-MOAPN35.lan
- **MAC:** 6C:24:08:D7:2D:F8
- **Services:** None accessible
- **Note:** All 100 ports filtered (heavy firewall)

---

## Peripherals

### 192.168.1.27 — HP Printer
- **Hostname:** HPAF786A.lan
- **MAC:** B0:0C:D1:AF:78:6B (Hewlett Packard)
- **Services:**
  - 80/tcp — HTTP (nginx)
  - 443/tcp — HTTPS (nginx)
  - 631/tcp — IPP (nginx)
  - 8080/tcp — HTTP alt (nginx)
  - 9100/tcp — JetDirect

### 192.168.1.183 — Yealink VoIP Phone
- **Hostname:** SIP-T33G.lan
- **MAC:** 44:DB:D2:86:66:9E
- **Services:**
  - 443/tcp — HTTPS (lighttpd)
  - 5101/tcp — admdog

---

## Gaming

### 192.168.1.58 — Nintendo Switch 2
- **Hostname:** None
- **MAC:** 94:8E:6D:29:C8:28 (Nintendo Co., Ltd)
- **OUI Registered:** 2025-05-28 (recent block = Switch 2)
- **Services:** All ports closed (outbound-only, typical Nintendo behavior)
- **Note:** Identified by MAC OUI lookup — Nintendo registered this prefix May 2025

---

## Virtual Networks (This Host)

### 172.17.16.0/20 — WSL/Docker
- Internal bridge for containers

### 172.27.64.0/20 — Hyper-V
- **172.27.75.128** — Hyper-V guest
- **MAC:** 00-15-5D-B6-03-E2 (Microsoft Hyper-V)

---

## Security Notes

1. **TP-Link AP (192.168.1.233)** — CRITICAL: OpenSSH 6.6.0 with only ssh-dss/DH-group1. Deprecated crypto, cannot connect with modern clients. Firmware update or replace device.
2. **192.168.1.58** — Identified as Nintendo Switch 2 (MAC lookup)
3. **DESKTOP-6FPF6DO (.28)** — SSH working, requires credentials
4. **DESKTOP-MOAPN35 (.223)** — Fully firewalled, all 100 ports filtered

---

## This Machine

- **IP:** 192.168.1.98
- **Hostname:** DESKTOP-7KTB236
