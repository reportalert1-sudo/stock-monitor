# Automated Stock Monitor Scheduler Setup Guide

## Overview
The scheduler automatically runs your stock monitor scan and saves daily snapshots without manual intervention.

## Quick Setup (Windows Task Scheduler)

### Option 1: Automatic Setup (Recommended)
Run this PowerShell command as Administrator:

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\User\.gemini\antigravity\scratch\stock_monitor\run_scheduler.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At "5:00PM"
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "Stock Monitor Daily Snapshot" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description "Automatically runs stock monitor scan and saves daily snapshot"
```

### Option 2: Manual Setup via Task Scheduler GUI

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, press Enter

2. **Create Basic Task**:
   - Click "Create Basic Task" in the right panel
   - Name: `Stock Monitor Daily Snapshot`
   - Description: `Automatically runs stock monitor scan and saves daily snapshot`

3. **Set Trigger**:
   - Trigger: `Daily`
   - Start time: `5:00 PM` (recommended for complete data after market close)
   - Recur every: `1 days`

4. **Set Action**:
   - Action: `Start a program`
   - Program/script: `C:\Users\User\.gemini\antigravity\scratch\stock_monitor\run_scheduler.bat`
   - Start in: `C:\Users\User\.gemini\antigravity\scratch\stock_monitor`

5. **Additional Settings** (Important!):
   - Check "Run whether user is logged on or not" (requires password)
   - Check "Run with highest privileges"
   - Under "Conditions" tab:
     - Uncheck "Start the task only if the computer is on AC power"
     - Check "Wake the computer to run this task" (optional)

## Recommended Schedule Times

### 🎯 Optimal: 5:00 PM ET (Recommended)
- **Why**: Yahoo Finance data is fully finalized 1 hour after market close
- **Best for**: Accurate volume and turnover metrics
- **Reliability**: Highest - all data is settled

### Alternative: 5:30 PM ET (Maximum Reliability)
- **Why**: Extra buffer for any delayed data updates
- **Best for**: Critical applications requiring 100% data accuracy
- **Reliability**: Maximum - guaranteed complete data

### Aggressive: 4:30 PM ET (Not Recommended)
- **Why**: Only 30 minutes after market close
- **Risk**: Volume/turnover data may still be updating
- **Use case**: Only if you need the earliest possible snapshot

### Time Zone Conversions (from ET):
- **5:00 PM ET** = 6:00 AM SGT (next day) | 2:00 AM PST | 10:00 PM GMT
- **5:30 PM ET** = 6:30 AM SGT (next day) | 2:30 AM PST | 10:30 PM GMT

### Yahoo Finance Data Timing:
- **Market Close**: 4:00 PM ET
- **Data Finalization**: 15-30 minutes after close (basic prices)
- **Volume Settlement**: Up to 60 minutes after close (turnover data)
- **Recommendation**: Wait at least 1 hour after close for complete data

## Testing the Scheduler

Test manually before relying on automation:

```bash
cd C:\Users\User\.gemini\antigravity\scratch\stock_monitor
run_scheduler.bat
```

Check the log file:
```bash
type logs\scheduler.log
```

## Logs

All scheduler runs are logged to:
- `logs/scheduler.log` - Contains timestamps, success/failure status, and error details

## Troubleshooting

**Scheduler doesn't run:**
- Verify Task Scheduler shows the task as "Ready"
- Check "Last Run Result" in Task Scheduler (0x0 = success)
- Ensure Python path is correct in `run_scheduler.bat`

**No snapshot created:**
- Check `logs/scheduler.log` for error messages
- Verify internet connection (needed for market data)
- Run manually to see detailed error output

**Snapshots saved but empty:**
- Market might be closed (no data available)
- API rate limits may be hit
- Check yfinance library is up to date

## Disabling the Scheduler

To temporarily disable:
- Open Task Scheduler
- Right-click "Stock Monitor Daily Snapshot"
- Select "Disable"

To permanently remove:
- Right-click the task
- Select "Delete"

## Advanced: Multiple Daily Snapshots

To capture multiple snapshots per day (e.g., market open, midday, close):

1. Create multiple tasks with different names
2. Set different trigger times for each
3. Each will save a snapshot with the same date (last one wins if same day)

Or modify `scheduler.py` to append time to the snapshot date.
