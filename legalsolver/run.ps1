# PowerShell script to run Legal Solver application

Write-Host "`n" + "=" * 60
Write-Host "LEGAL SOLVER - APPLICATION STARTUP"
Write-Host "=" * 60

Write-Host "`nStarting Legal Solver application..."
Write-Host "Email is pre-configured with the following settings:"
Write-Host "- Email: notification@agentsdistrict.com"
Write-Host "- SMTP Server: smtp.hostinger.com"
Write-Host "- SMTP Port: 465"

Write-Host "`nRunning application on http://127.0.0.1:5000"
python app.py 