# Laravel Social Provider

> Add a new social media provider to MixPost (mixpost-malone fork)

## When to Use
- Adding new platform support (YouTube, TikTok, Discord, etc.)
- Need OAuth + API integration for social posting

## Steps

### 1. Planning
```powershell
.\scripts\plan.ps1 -Task "Add [Platform] provider" -Constraints "Laravel, OAuth2, MixPost patterns"
```
- Research platform API docs
- Note OAuth scopes needed
- Identify post types supported

### 2. Scaffold
```powershell
.\scripts\new-provider.ps1 -Name "PlatformName" -ApiUrl "https://api.platform.com/v1"
```
Or use cookiecutter:
```bash
cookiecutter templates/laravel-provider
```

### 3. Implement Concerns
Files to create in `src/SocialProviders/{Name}/Concerns/`:
- `ManagesOAuth.php` — Auth URL, token exchange, refresh, revoke
- `ManagesResources.php` — getAccount, getEntities, getMetrics, deletePost
- `ManagesUploads.php` — (if video/media platform)

### 4. Create Service
`src/Services/{Name}Service.php`:
- credentials() — Required config fields
- credentialsForm() — UI field definitions
- documentation() — Setup instructions HTML

### 5. Register Provider
In `SocialProviderManager.php`:
```php
use Inovector\Mixpost\SocialProviders\{Name}\{Name}Provider;

// Add to $providers array
'{name}' => {Name}Provider::class,

// Add connect method
protected function connect{Name}Provider() { ... }
```

### 6. Create PR
```bash
git checkout -b feature/{name}-provider
git add -A
git commit -m "feat: add {Name} social provider"
git push -u origin feature/{name}-provider
gh pr create --title "feat: Add {Name} provider" --body "..."
```

## Checklist
- [ ] OAuth flow works (state validation!)
- [ ] Token refresh implemented
- [ ] getAccount returns valid data
- [ ] publishPost sends content
- [ ] Service has setup docs
- [ ] Registered in SocialProviderManager
- [ ] PR created for review

## Common Pitfalls
- **OAuth URLs**: Some APIs have separate OAuth endpoints (Discord: no /v10)
- **State validation**: Always validate CSRF state in requestAccessToken
- **Rate limits**: Check API docs for limits
- **Scopes**: Request minimal necessary permissions
