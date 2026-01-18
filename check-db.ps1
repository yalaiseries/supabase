# Check what's actually in the winners_payload table
$projectRef = "xcctqbamimafkkamuwly"
$url = "https://$projectRef.supabase.co"

# Get service role key from secrets
$secrets = supabase secrets list --project-ref $projectRef | Out-String
if ($secrets -match "SERVICE_ROLE_KEY\s+\|\s+([a-f0-9]+)") {
    Write-Host "Found SERVICE_ROLE_KEY hash: $($Matches[1])"
    Write-Host ""
    Write-Host "The database query is returning 0 rows."
    Write-Host "This means either:"
    Write-Host "1. The table is empty (data was never uploaded)"
    Write-Host "2. The data was uploaded but deleted"
    Write-Host "3. There's an RLS policy blocking reads"
    Write-Host ""
    Write-Host "Let's check the Supabase dashboard:"
    Write-Host "https://supabase.com/dashboard/project/$projectRef/editor"
    Write-Host ""
    Write-Host "Look for the 'winners_payload' table and check if it has any rows."
}
