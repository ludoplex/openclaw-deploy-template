<#
.SYNOPSIS
    Create a new MixPost social provider from template

.PARAMETER Name
    Provider name (e.g., "Instagram", "LinkedIn")

.PARAMETER ApiUrl
    Base API URL

.PARAMETER OAuthUrl
    OAuth base URL

.PARAMETER TokenUrl
    Token endpoint URL

.EXAMPLE
    .\new-provider.ps1 -Name "LinkedIn" -ApiUrl "https://api.linkedin.com/v2"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    
    [string]$ApiUrl = "https://api.example.com/v1",
    [string]$OAuthUrl = "https://example.com/oauth",
    [string]$TokenUrl = "https://example.com/oauth/token",
    [string]$MaxText = "2000",
    [string]$MaxPhotos = "4",
    [string]$MaxVideos = "1",
    [string]$OutputDir = "C:\Users\user\mixpost-malone\src\SocialProviders"
)

$templateDir = "C:\Users\user\.openclaw\workspace\templates\laravel-provider"

# Check if cookiecutter is available
$cc = Get-Command cookiecutter -ErrorAction SilentlyContinue
if (-not $cc) {
    Write-Error "cookiecutter not found. Install with: pip install cookiecutter"
    exit 1
}

# Create provider
Write-Host "Creating provider: $Name" -ForegroundColor Cyan

$extraContext = @"
{
    "provider_name": "$Name",
    "api_base_url": "$ApiUrl",
    "oauth_base_url": "$OAuthUrl",
    "token_url": "$TokenUrl",
    "max_text_char": "$MaxText",
    "max_photos": "$MaxPhotos",
    "max_videos": "$MaxVideos"
}
"@

# Save context to temp file
$contextFile = [System.IO.Path]::GetTempFileName()
$extraContext | Out-File -FilePath $contextFile -Encoding UTF8

try {
    Push-Location $OutputDir
    cookiecutter $templateDir --no-input --config-file $contextFile
    Write-Host "✓ Provider created at: $OutputDir\$Name" -ForegroundColor Green
} finally {
    Pop-Location
    Remove-Item $contextFile -ErrorAction SilentlyContinue
}

Write-Host @"

Next steps:
1. Create Service class: src/Services/${Name}Service.php
2. Register in SocialProviderManager.php
3. Customize OAuth scopes in ManagesOAuth.php
4. Add provider-specific API methods

"@ -ForegroundColor Yellow
