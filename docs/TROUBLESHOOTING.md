# Troubleshooting Guide

## Common Issues

### Dashboard Won't Start

**Symptom:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
cd sop-automation-dashboard
pip install -r requirements.txt
python -m uvicorn src.dashboard.app:app --port 8080
```

---

### AI Content Generation Not Working

**Symptom:** "Local LLM not available" error

**Check:**
1. Is llamafile running?
   ```bash
   curl http://localhost:8081/health
   ```

2. Start llamafile:
   ```bash
   ./bin/llamafile.exe -m models/qwen2.5-7b-instruct-q3_k_m.gguf --server --port 8081 -ngl 99
   ```

3. Check `local_llm.py` is accessible in workspace

---

### SOP Won't Execute

**Symptom:** "SOP not found" or execution fails

**Check:**
1. Is the YAML valid?
   ```bash
   python -c "import yaml; yaml.safe_load(open('sops/entity/sop.yaml'))"
   ```

2. Required fields present?
   - `name`, `entity`, `triggers`, `steps`

3. Step type exists?
   - Valid: `social_post`, `zoho_create_record`, `approval`, `condition`, `delay`, `webhook`

---

### Zoho Integration Errors

**Symptom:** "Zoho not configured" or auth errors

**Check:**
1. Environment variables set?
   ```bash
   echo $ZOHO_CLIENT_ID
   echo $ZOHO_CLIENT_SECRET
   ```

2. OAuth tokens valid?
   - Check `GET /api/zoho/status`
   - Refresh tokens if expired

3. Module permissions?
   - Verify API access in Zoho Developer Console

---

### Content Not Publishing

**Symptom:** Draft approved but won't publish

**Check:**
1. MixPost credentials configured?
   ```bash
   echo $MIXPOST_URL
   echo $MIXPOST_TOKEN
   ```

2. Platform connected in MixPost?
   - Log into MixPost dashboard
   - Verify social account connections

3. For now, manually publish:
   - Export content from `/drafts`
   - Post directly to platform

---

### Slow Performance

**Symptom:** Dashboard loads slowly

**Check:**
1. LLM server overloaded?
   ```bash
   curl http://localhost:8081/health
   # Check slots_processing
   ```

2. Large data files?
   - Archive old drafts/requests
   - Clear `data/*.json` if needed

3. Enable production mode:
   ```bash
   uvicorn src.dashboard.app:app --workers 4
   ```

---

### HTMX Not Working

**Symptom:** Buttons don't respond, no AJAX updates

**Check:**
1. Browser console for JS errors
2. HTMX loaded in base.html?
3. Network tab - requests going through?
4. Response format - should be HTML, not JSON

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 404 | SOP/Draft not found | Check ID exists |
| 422 | Validation error | Check required fields |
| 500 | Server error | Check uvicorn logs |
| 503 | Service unavailable | Check dependencies |

## Logs

### Dashboard Logs
Watch uvicorn output:
```bash
uvicorn src.dashboard.app:app --port 8080 --reload
```

### LLM Logs
Watch llamafile output for generation issues

### Debug Mode
Add to request:
```
?debug=true
```

## Getting Help

1. Check `/api/status` for system state
2. Review recent changes in `memory/` files
3. Consult SOP_AUTHORING_GUIDE.md for syntax
4. Check GitHub issues: github.com/ludoplex/sop-automation-dashboard

## Reset to Clean State

**Warning:** This deletes all data!

```bash
rm -rf data/*.json
rm -rf data/content/*.json
python -m uvicorn src.dashboard.app:app --port 8080
```
