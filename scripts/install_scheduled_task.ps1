<#
Registers a Windows Scheduled Task that runs run_pipeline.py to discover new
YouTube videos for the creators in transcripts/urls.txt and fetch transcripts.

Why Task Scheduler (not WSL cron): it's VPN-independent and doesn't need the
distro to be awake on a timer. The task runs a local copy of run-hidden.vbs,
whose wsl.exe starts the distro on demand and runs the pipeline INSIDE WSL using
a dedicated Linux venv (.venv-linux). The pipeline command itself lives in
run-hidden.vbs. Nothing launches from a \\wsl.localhost\ path, which Task
Scheduler can't reliably resolve at run time (0x80070002 "file not found").

Run from an elevated PowerShell (Run as Administrator). Updating the existing
task fails with Access Denied (0x80070005) without elevation:
    powershell -ExecutionPolicy Bypass -File scripts\install_scheduled_task.ps1

Re-run any time to update the task (it uses -Force). Remove with:
    Unregister-ScheduledTask -TaskName 'YouTube URL Updater' -Confirm:$false
#>

$ErrorActionPreference = 'Stop'

# The pipeline runs inside WSL with the repo's dedicated Linux venv at
# .venv-linux (has youtube-transcript-api, which brings in requests). Create it
# with:
#   wsl -d Ubuntu -e bash -lc 'cd <repo> && uv venv .venv-linux \
#   --python 3.14 && uv pip install --python .venv-linux/bin/python \
#   youtube-transcript-api requests'
$venvPy   = '\\wsl.localhost\Ubuntu\home\YOUR_USER\path\to\claudex-setup\.venv-linux\bin\python'
$taskName = 'YouTube URL Updater'

if (-not (Test-Path $venvPy)) {
    throw "Linux venv Python not found at $venvPy - create .venv-linux in the repo first (see header)."
}

# The launcher is copied to a local folder because the task fires at logon,
# often before WSL has booted. A script on \\wsl.localhost\ is unreachable then,
# so wscript exits 1 without running anything. wsl.exe inside the local copy
# boots the distro itself. Re-run this installer after editing run-hidden.vbs.
$launcherDir = "$env:LOCALAPPDATA\claudex-setup"
New-Item -ItemType Directory -Force -Path $launcherDir | Out-Null
Copy-Item '\\wsl.localhost\Ubuntu\home\YOUR_USER\path\to\claudex-setup\scripts\run-hidden.vbs' "$launcherDir\run-hidden.vbs" -Force

$action  = New-ScheduledTaskAction -Execute "$env:WINDIR\System32\wscript.exe" -Argument "//B `"$launcherDir\run-hidden.vbs`""
# Fire at logon only (the owner dropped the hourly trigger on 2026-07-19).
# run_pipeline.py's own 24h gate still decides when to actually do work, so a
# second logon within a day is an instant no-op.
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Run only when the user is logged on.
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# Catch up on a missed run (e.g. PC was off Monday 9am); don't stop on battery.
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

Register-ScheduledTask -TaskName $taskName `
    -Action $action -Trigger $trigger -Principal $principal -Settings $settings `
    -Description 'Logon trigger; a 24h in-script gate makes it run at most once a day, anchored to actual PC usage. Discovers new videos and fetches a batch of transcripts.' `
    -Force | Out-Null

Write-Host "Registered scheduled task '$taskName' (logon; 24h in-script gate)."
Get-ScheduledTask -TaskName $taskName | Format-List TaskName, State
