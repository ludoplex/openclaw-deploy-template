# GPU Server Setup Checklist — Wheatland Location

**Target Date:** Wednesday, Feb 12, 2026  
**Hardware:** 4× Tesla V100 32GB, AMD Threadripper, 256GB RAM (confirmed), 10GbE  
**Location:** 977 Gilchrist St, Wheatland WY (Computer Store)

---

## Phase 1: Physical Setup (30 min)

- [ ] Rack mount or position server in ventilated area
- [ ] Connect 10GbE to Netgear switch (SFP+ or RJ45)
- [ ] Verify BIOS sees all 4 GPUs
- [ ] Confirm RAM amount in BIOS
- [ ] Connect to UPS if available (recommended for Vast.ai uptime)

---

## Phase 2: OS Install (1-2 hours)

### Option A: Ubuntu Server 22.04 LTS (Recommended for Vast.ai)
```bash
# Download: https://ubuntu.com/download/server
# Create bootable USB with Rufus or Balena Etcher
# Install with:
#   - OpenSSH server enabled
#   - LVM for storage flexibility
#   - Static IP (or DHCP reservation on router)
```

### Option B: Ubuntu Desktop 22.04 (if you want GUI for monitoring)

---

## Phase 3: NVIDIA Drivers + CUDA (1 hour)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install NVIDIA driver (latest for V100)
sudo apt install -y nvidia-driver-535

# Reboot
sudo reboot

# Verify GPUs visible
nvidia-smi

# Should show 4× Tesla V100-PCIE-32GB
```

### Expected nvidia-smi output:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xxx    Driver Version: 535.xxx    CUDA Version: 12.x        |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
|   0  Tesla V100-PCIE-32GB Off |   00000000:XX:00.0 Off|                    0 |
|   1  Tesla V100-PCIE-32GB Off |   00000000:XX:00.0 Off|                    0 |
|   2  Tesla V100-PCIE-32GB Off |   00000000:XX:00.0 Off|                    0 |
|   3  Tesla V100-PCIE-32GB Off |   00000000:XX:00.0 Off|                    0 |
+-------------------------------+----------------------+----------------------+
```

---

## Phase 4: Vast.ai Host Setup (30 min)

### 4.1 Create Vast.ai Account
1. Go to https://vast.ai
2. Sign up (use MHI email for business account)
3. Complete verification

### 4.2 Install Vast CLI
```bash
# Install Docker first
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Install Vast CLI
pip install vastai
vastai set api-key YOUR_API_KEY
```

### 4.3 Register as Host
```bash
# Download and run the host setup script
wget https://s3.amazonaws.com/vast.ai/vast-install.sh
chmod +x vast-install.sh
sudo ./vast-install.sh
```

### 4.4 Configure Pricing
- Go to https://cloud.vast.ai/host/machines
- Set your rates (start at market rate ~$0.05-0.08/GPU/hr for V100)
- Set availability schedule (24/7 or custom)
- Enable "interruptible" for higher utilization

---

## Phase 5: Networking (15 min)

```bash
# Verify 10GbE link speed
ethtool eth0 | grep Speed
# Should show: Speed: 10000Mb/s

# Test bandwidth
sudo apt install iperf3
# Run speed test to verify throughput
```

### Router/Firewall Configuration
- [ ] Port forward or DMZ the server (Vast.ai needs inbound access)
- [ ] Or use Vast.ai's NAT traversal (works behind most NATs)

---

## Phase 6: Monitoring Setup (Optional but Recommended)

```bash
# Install monitoring
sudo apt install -y htop nvtop

# For remote monitoring, install Netdata
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
# Access at http://SERVER_IP:19999
```

---

## Phase 7: Verification

- [ ] All 4 GPUs visible in `nvidia-smi`
- [ ] Docker running: `docker ps`
- [ ] Vast.ai host online: check https://cloud.vast.ai/host/machines
- [ ] Test rent your own machine to verify it works

---

## Fallback: Self-Hosted LLM (if Vast.ai utilization is low)

```bash
# Install llamafile for local inference
wget https://github.com/Mozilla-Ocho/llamafile/releases/download/0.9.3/llamafile-0.9.3
chmod +x llamafile-0.9.3
./llamafile-0.9.3 --server --port 8080 -ngl 99
```

Or use Ollama:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:70b  # Big model that needs 32GB VRAM
```

---

## Estimated Revenue

| Utilization | Monthly Revenue | After Power ($86) |
|-------------|-----------------|-------------------|
| 25% | $36 | -$50 (loss) |
| 50% | $72 | -$14 (break-even-ish) |
| 75% | $108 | +$22 |
| 100% | $144 | +$58 |
| Premium rates | $288 | +$202 |

**Target:** 75%+ utilization or use for self-hosted AI when idle.

---

## Support

- Vast.ai Discord: https://discord.gg/vast
- Vast.ai Docs: https://docs.vast.ai
- NVIDIA V100 specs: https://www.nvidia.com/en-us/data-center/v100/

---

*Created: 2026-02-08*
*For: MHI Computer Store, Wheatland WY*
