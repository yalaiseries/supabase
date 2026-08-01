param(
    [Parameter(Mandatory = $true)]
    [string]$SupabaseUrl,

    [Parameter(Mandatory = $false)]
    [string]$ServiceRoleKey = $env:SERVICE_ROLE_KEY,

    [Parameter(Mandatory = $false)]
    [string]$BatchDir = "invite/batches_2026-02-26",

    [Parameter(Mandatory = $false)]
    [string]$ReportRoot = "reports/invite_batches",

    [Parameter(Mandatory = $false)]
    [int]$CooldownSeconds = 900,

    [Parameter(Mandatory = $false)]
    [int]$StartBatch = 1,

    [Parameter(Mandatory = $false)]
    [int]$EndBatch = 999,

    [Parameter(Mandatory = $false)]
    [string]$RedirectTo = "https://aihackathon.pro/members.html?type=recovery",

    [Parameter(Mandatory = $false)]
    [int]$PerEmailDelaySeconds = 5,

    [Parameter(Mandatory = $false)]
    [int]$Retry429 = 1,

    [Parameter(Mandatory = $false)]
    [int]$RetryWaitSeconds = 30,

    [Parameter(Mandatory = $false)]
    [int]$StopOnConsecutive429 = 2,

    [switch]$StopOnAnyFailure
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($ServiceRoleKey)) {
    throw "Missing ServiceRoleKey. Pass -ServiceRoleKey or set SERVICE_ROLE_KEY environment variable."
}

if (-not (Test-Path -Path $BatchDir)) {
    throw "BatchDir not found: $BatchDir"
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportDir = Join-Path $ReportRoot $timestamp
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

$batchFiles = Get-ChildItem -Path $BatchDir -Filter "batch_*.csv" | Sort-Object Name
if (-not $batchFiles -or $batchFiles.Count -eq 0) {
    throw "No batch files found in $BatchDir"
}

$selected = @()
foreach ($file in $batchFiles) {
    if ($file.BaseName -match "^batch_(\d+)$") {
        $batchNo = [int]$Matches[1]
        if ($batchNo -ge $StartBatch -and $batchNo -le $EndBatch) {
            $selected += [PSCustomObject]@{
                BatchNo = $batchNo
                File = $file
            }
        }
    }
}

if ($selected.Count -eq 0) {
    throw "No batches matched StartBatch=$StartBatch EndBatch=$EndBatch"
}

$selected = @($selected | Sort-Object BatchNo)

$summary = @()
$idx = 0
$total = $selected.Count

Write-Host "Starting invite batches..." -ForegroundColor Cyan
Write-Host "Total selected batches: $total"
Write-Host "Report directory: $reportDir"

foreach ($item in $selected) {
    $idx++
    $batchNo = $item.BatchNo
    $batchFile = $item.File.FullName
    $batchLabel = "batch_{0:D2}" -f $batchNo
    $reportPath = Join-Path $reportDir ("{0}_report.csv" -f $batchLabel)
    $consoleLogPath = Join-Path $reportDir ("{0}_console.log" -f $batchLabel)

    Write-Host ""
    Write-Host ("[{0}/{1}] Running {2}" -f $idx, $total, $batchLabel) -ForegroundColor Yellow
    Write-Host ("Input: {0}" -f $batchFile)

    $output = & python bulk_send_auth_links.py `
        --supabase-url $SupabaseUrl `
        --service-role-key $ServiceRoleKey `
        --input $batchFile `
        --email-column "email" `
        --name-column "full_name" `
        --mode "invite" `
        --redirect-to $RedirectTo `
        --sleep-seconds $PerEmailDelaySeconds `
        --retry-429 $Retry429 `
        --retry-wait-seconds $RetryWaitSeconds `
        --stop-on-consecutive-429 $StopOnConsecutive429 `
        --report $reportPath 2>&1

    $exitCode = $LASTEXITCODE
    $output | Out-File -FilePath $consoleLogPath -Encoding utf8

    $status = if ($exitCode -eq 0) { "ok" } else { "failed" }
    Write-Host ("Exit code: {0} ({1})" -f $exitCode, $status)
    Write-Host ("Report: {0}" -f $reportPath)

    $summary += [PSCustomObject]@{
        batch = $batchLabel
        input = $batchFile
        report = $reportPath
        console_log = $consoleLogPath
        exit_code = $exitCode
        status = $status
    }

    if ($exitCode -ne 0 -and $StopOnAnyFailure) {
        Write-Host "Stopping due to failure (StopOnAnyFailure enabled)." -ForegroundColor Red
        break
    }

    if ($idx -lt $total) {
        Write-Host ("Cooling down for {0} seconds..." -f $CooldownSeconds) -ForegroundColor DarkCyan
        Start-Sleep -Seconds $CooldownSeconds
    }
}

$summaryPath = Join-Path $reportDir "run_summary.csv"
$summary | Export-Csv -Path $summaryPath -NoTypeInformation -Encoding UTF8

$okCount = @($summary | Where-Object { $_.exit_code -eq 0 }).Count
$failCount = @($summary | Where-Object { $_.exit_code -ne 0 }).Count

Write-Host ""
Write-Host "Run complete." -ForegroundColor Green
Write-Host ("Successful batches: {0}" -f $okCount)
Write-Host ("Failed batches: {0}" -f $failCount)
Write-Host ("Summary: {0}" -f $summaryPath)

if ($failCount -gt 0) {
    exit 1
}

exit 0
