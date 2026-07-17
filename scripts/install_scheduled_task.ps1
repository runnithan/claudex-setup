<#
Registers a Windows Scheduled Task that runs run_pipeline.py to discover new
YouTube videos for the creators in transcripts/urls.txt and fetch transcripts.

Why Task Scheduler (not WSL cron): it's VPN-independent and doesn't need the
distro to be awake on a timer. The task action launches a local wsl.exe, which
starts the distro on demand and runs the pipeline INSIDE WSL using a dedicated
Linux venv (.venv-linux). This avoids pointing the task at a \\wsl.localhost\
executable, which Task Scheduler can't reliably resolve at run time (it fails
with 0x80070002 "file not found").

Run from an ordinary PowerShell (no admin needed):
    powershell -ExecutionPolicy Bypass -File scripts\install_scheduled_task.ps1

Re-run any time to update the task (it uses -Force). Remove with:
    Unregister-ScheduledTask -TaskName 'YouTube URL Updater' -Confirm:$false
#>

$ErrorActionPreference = 'Stop'

# Run the pipeline inside WSL via a local wsl.exe (always resolvable) using the
# repo's dedicated Linux venv at .venv-linux (has youtube-transcript-api plus
# curl_cffi for TLS/browser impersonation — see references/transcript-fetch-throttling.md).
# Create it with: wsl -d Ubuntu -e bash -lc 'cd <repo> && uv venv .venv-linux \
#   --python 3.14 && uv pip install --python .venv-linux/bin/python \
#   youtube-transcript-api curl_cffi'
$wsl     = "$env:WINDIR\System32\wsl.exe"
$wslArgs = '-d Ubuntu -e bash -lc "cd /home/YOUR_USER/path/to/claudex-setup && .venv-linux/bin/python scripts/run_pipeline.py"'
$venvPy  = '\\wsl.localhost\Ubuntu\home\YOUR_USER\path\to\claudex-setup\.venv-linux\bin\python'
$taskName = 'YouTube URL Updater'

if (-not (Test-Path $venvPy)) {
    throw "Linux venv Python not found at $venvPy - create .venv-linux in the repo first (see header)."
}

$action  = New-ScheduledTaskAction -Execute "$env:WINDIR\System32\wscript.exe" -Argument '//B "\\wsl.localhost\Ubuntu\home\YOUR_USER\path\to\claudex-setup\scripts\run-hidden.vbs"'
# Fire at login + hourly; run_pipeline.py's own 24h gate decides when to actually
# do work, so the cadence is "~once a day since it last ran", anchored to real
# usage rather than a clock slot. Gated wake-ups are instant no-ops.
$trigger = @(
    New-ScheduledTaskTrigger -AtLogOn
    (New-ScheduledTaskTrigger -Once -At (Get-Date).Date `
        -RepetitionInterval (New-TimeSpan -Hours 1))
)

# Run only when the user is logged on (so the \\wsl.localhost share is available).
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Catch up on a missed run (e.g. PC was off Monday 9am); don't stop on battery.
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

Register-ScheduledTask -TaskName $taskName `
    -Action $action -Trigger $trigger -Principal $principal -Settings $settings `
    -Description 'Login + hourly trigger; a 24h in-script gate makes it run ~once a day, anchored to actual PC usage. Discovers new videos and fetches a batch of transcripts.' `
    -Force | Out-Null

Write-Host "Registered scheduled task '$taskName' (login + hourly; 24h in-script gate)."
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State
