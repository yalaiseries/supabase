param(
  [string]$WebhookSecret,

  [string]$Email = "test@example.com",
  [string]$Name = "Webhook Test",
  [string]$Source = "powershell_test"
)

$ErrorActionPreference = 'Stop'

if (-not $WebhookSecret -or $WebhookSecret.Trim().Length -eq 0) {
  if ($env:REGISTRATION_WEBHOOK_SECRET -and $env:REGISTRATION_WEBHOOK_SECRET.Trim().Length -gt 0) {
    $WebhookSecret = $env:REGISTRATION_WEBHOOK_SECRET
  } else {
    $secure = Read-Host "Enter x-webhook-secret" -AsSecureString
    $WebhookSecret = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
      [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    )
  }
}

$uri = "https://xcctqbamimafkkamuwly.supabase.co/functions/v1/register-sync"

$headers = @{
  "x-webhook-secret" = $WebhookSecret
}

$payloadObj = [ordered]@{
  email    = $Email
  name     = $Name
  source   = $Source
  testedAt = (Get-Date).ToString('o')
}

$payload = $payloadObj | ConvertTo-Json

Write-Host "POST $uri" -ForegroundColor Cyan

try {
  $resp = Invoke-WebRequest -Method Post -Uri $uri -Headers $headers -ContentType "application/json" -Body $payload
  Write-Host "Status: $($resp.StatusCode)" -ForegroundColor Green
  Write-Host "Body: $($resp.Content)"
} catch {
  $ex = $_.Exception
  $r = $ex.Response
  $bodyText = ""

  # Windows PowerShell 5.1: HttpWebResponse
  if ($r -and $r.GetType().FullName -eq 'System.Net.HttpWebResponse') {
    try {
      $reader = New-Object System.IO.StreamReader($r.GetResponseStream())
      $bodyText = $reader.ReadToEnd()
    } catch { }

    Write-Host "Status: $([int]$r.StatusCode) $($r.StatusDescription)" -ForegroundColor Yellow
    if ($bodyText) { Write-Host "Body: $bodyText" }
    exit 1
  }

  # PowerShell 7+: HttpResponseMessage
  if ($r -and $r.GetType().FullName -eq 'System.Net.Http.HttpResponseMessage') {
    try {
      $bodyText = $r.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    } catch { }

    Write-Host "Status: $([int]$r.StatusCode)" -ForegroundColor Yellow
    if ($bodyText) { Write-Host "Body: $bodyText" }
    exit 1
  }

  Write-Host ($ex.Message) -ForegroundColor Red
  exit 1
}
