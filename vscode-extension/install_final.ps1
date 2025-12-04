$extDir = "$env:USERPROFILE\.vscode\extensions\pawa-ai.pawa-ai-1.0.2"

Write-Host "Removing old versions..."
Get-ChildItem "$env:USERPROFILE\.vscode\extensions" | Where-Object { $_.Name -like "pawa*" } | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Installing to: $extDir"
New-Item -ItemType Directory -Force -Path $extDir | Out-Null

Write-Host "Extracting VSIX..."
Copy-Item "pawa-ai-1.0.2.vsix" "pawa-ai-1.0.2.zip" -Force
Expand-Archive -Path "pawa-ai-1.0.2.zip" -DestinationPath "temp_install" -Force

Write-Host "Copying files..."
Copy-Item "temp_install\extension\*" -Destination $extDir -Recurse -Force

Write-Host "Cleaning up..."
Remove-Item "temp_install" -Recurse -Force
Remove-Item "pawa-ai-1.0.2.zip" -Force

Write-Host ""
Write-Host "SUCCESS! Extension installed to: $extDir"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Close ALL VS Code windows"
Write-Host "  2. Reopen VS Code"
Write-Host "  3. Press Ctrl+Shift+A to open chat"
Write-Host ""
