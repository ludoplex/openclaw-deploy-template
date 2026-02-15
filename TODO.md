# TODO.md - Active Task List

*Updated: 2026-02-15 03:10 MST*

## 🔴 HIGH PRIORITY

### Procurement App
- [ ] Get D&H REST API credentials (request sent to RISmith@dandh.com)
- [ ] Get TD SYNNEX Digital Bridge API credentials (request sent to mikko.dizon@tdsynnex.com)
- [ ] Complete cosmo-sokol GUI implementation
- [ ] Integrate Ingram Micro API (sandbox working)
- [ ] Add Mouser API integration

### VPS Autonomy Setup
- [ ] Vincent provisions Hetzner VPS (AX41 or auction 64GB)
- [ ] Bootstrap OpenClaw on VPS
- [ ] Sync workspace via git
- [ ] Migrate credentials
- [ ] Test autonomous operation

### Amazon Automation
- [ ] Register Amazon SP-API developer account
- [ ] Build listing automation module
- [ ] Integrate with procurement inventory

### WithOdyssey CSV
- [ ] Get CSV format specification
- [ ] Build CSV generator from Zoho Inventory
- [ ] Automate upload process

---

## 🟡 MEDIUM PRIORITY

### Supplier Setup
- [ ] Follow up with D&H if no response in 48h
- [ ] Follow up with TD SYNNEX if no response in 48h
- [ ] Apply for DigiKey API access (developer.digikey.com)
- [ ] Apply for Arrow API access
- [ ] Check Ma Labs for API availability

### Computer Store
- [ ] VEX Robotics reseller account
- [ ] XYAB inventory integration (contact: Kayla Osness)

---

## 🟢 LOW PRIORITY / BACKLOG

- [ ] Icecat product data integration (free)
- [ ] ScanSource partner program evaluation
- [ ] BlueStar POS equipment channel
- [ ] **REVISIT:** Proper email sending solution (currently using Rachel SMTP + Reply-To: Vincent workaround) — fix after procurement app, WithOdyssey, and Amazon store are stable

---

## ✅ COMPLETED

- [x] Search Zoho email for supplier credentials (2026-02-14)
- [x] Create analyst reports: VPS options, supplier enumeration (2026-02-14)
- [x] Identify API request status for D&H, TD SYNNEX (2026-02-14)
- [x] Map all supplier contacts (Arrow, Ma Labs, ASI, XYAB) (2026-02-14)
- [x] Fix memory index (swapped 2.6GB tmp with 29K embeddings to main.sqlite) (2026-02-15)
- [x] Document WithOdyssey state portal URLs (Iowa, GA, LA, WY, UT, TX) (2026-02-15)
- [x] Confirm MHI vendor approval status (Wyoming, Utah, LA GATOR confirmed) (2026-02-15)
- [x] Audit config.ini for working APIs (Ingram✅, Mouser✅, Element14✅, Climb✅) (2026-02-15)
- [x] Commit 194 files to workspace repo (2026-02-15 03:25 AM)
- [x] Push to GitHub (force push due to diverged branches) (2026-02-15 03:25 AM)
- [x] Analyze mhi-procurement codebase structure (2026-02-15 03:30 AM)
- [x] Create codebase analysis: `analysis/mhi-procurement-codebase-2026-02-15.md`

---

## 🚫 BLOCKED

| Task | Blocker | Waiting On |
|------|---------|------------|
| D&H API integration | No credentials | RISmith@dandh.com response |
| TD SYNNEX integration | No credentials | mikko.dizon@tdsynnex.com response |
| Amazon automation | No SP-API access | Vincent to register developer account |
| VPS setup | ✅ Creds found | theanderproject@gmail.com / MixPost2026!Hetzner (incomplete signup) |
| WithOdyssey CSV upload | ✅ Creds received | rachelwilliams@mightyhouseinc.com / 0rcaWar$ |

---

*Update this file whenever tasks change. Use `memory_search("TODO")` to find.*
