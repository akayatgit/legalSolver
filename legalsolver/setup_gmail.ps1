# PowerShell script to set up Gmail environment variables for Legal Solver

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "LEGAL SOLVER - GMAIL APP PASSWORD SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for Gmail address
$emailAddress = Read-Host -Prompt "Enter your Gmail address"

# Prompt for App Password (with masking)
$securePassword = Read-Host -Prompt "Enter your Gmail App Password" -AsSecureString
$bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$appPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)

# Set environment variables for current session
Write-Host "`nSetting environment variables for current session..." -ForegroundColor Yellow
$env:EMAIL_USER = $emailAddress
$env:EMAIL_PASSWORD = $appPassword
Write-Host "Environment variables set for current session." -ForegroundColor Green

# Set environment variables permanently (user level)
Write-Host "`nSetting environment variables permanently (user level)..." -ForegroundColor Yellow
[System.Environment]::SetEnvironmentVariable("EMAIL_USER", $emailAddress, "User")
[System.Environment]::SetEnvironmentVariable("EMAIL_PASSWORD", $appPassword, "User")
Write-Host "Environment variables set permanently at user level." -ForegroundColor Green

Write-Host "`nWould you like to test the Gmail configuration now? (Y/N)" -ForegroundColor Cyan
$testNow = Read-Host
if ($testNow -eq "Y" -or $testNow -eq "y") {
    Write-Host "`nRunning Gmail configuration test..." -ForegroundColor Yellow
    python test_gmail_config.py
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "You can now run the Legal Solver application with Gmail notifications." -ForegroundColor Green
Write-Host "To start the application, run: python run.py" -ForegroundColor Cyan 