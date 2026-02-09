# Arena.ai GPU Server Transport Context
**Extracted:** 2026-02-08

## Server Specs (Confirmed)
- **CPU:** AMD Threadripper WS
- **RAM:** 256GB
- **GPUs:** 4× Tesla V100 32GB PCIe
- **Chassis:** 4U rack mount
- **PSUs:** 2×
- **Networking:** 10GbE + Netgear switch

## Transport Details
- **Route:** California → Denver (flight) → Wheatland WY
- **Method:** Checked baggage (likely Southwest based on recommendations)
- **Risk Level:** HIGH — heatsink and 2 GPUs left mounted during transport

## Transport Risks Identified (from Arena AI models)
1. **GPU PCIe Slot Damage:** V100s weigh 2.4kg each, act as cantilevers
2. **Motherboard Flex:** Threadripper boards flex in the middle under stress
3. **Heatsink Socket Damage:** Heavy tower cooler acts as lever on CPU socket
4. **Estimated Damage Risk:** 70-80% with poor bracing, 50% even with foam bracing

## Wednesday Inspection Checklist
- [ ] Visual inspect motherboard for cracks/flex
- [ ] Check all PCIe slots for damage
- [ ] Verify GPU seating (reseat if needed)
- [ ] Check heatsink mount is still secure
- [ ] Run nvidia-smi to verify all 4 GPUs detected
- [ ] Check for ECC errors in GPU memory
- [ ] Stress test before Vast.ai registration

## Recommendations from Arena Discussion
1. Best: FedEx Freight Priority with $20-30K insurance (~$400-650)
2. Good: Southwest oversize baggage in SKB/Pelican case (~$225)
3. Critical: Remove GPUs and carry-on, remove heatsink
4. Used: Foam in box, heatsink + 2 GPUs left mounted (risky)

## Post-Transport Actions
If GPUs not detected or showing errors:
1. Reseat all GPUs
2. Check PCIe power connections
3. Inspect slots for bent pins
4. Test GPUs individually in slot 0
