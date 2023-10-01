Add-Type -AssemblyName System.Windows.Forms

# Activate the Microsoft Edge window
$edgeProcess = Get-Process | Where-Object { $_.MainWindowTitle -like "*Microsoft Edge*" } | Select-Object -First 1

if ($edgeProcess) {
    $edgeProcess | ForEach-Object {
        $_.SetForegroundWindow()
        
        # Wait for a moment to ensure the window is active
        Start-Sleep -Seconds 2

        # Send Ctrl+P to open the print dialog
        [System.Windows.Forms.SendKeys]::SendWait("^p")

        # Wait for the print dialog to open
        Start-Sleep -Seconds 2

        # Send Enter to print (assuming "Save as PDF" is the default option)
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

        # Wait for the save dialog to open
        Start-Sleep -Seconds 2

        # Send Enter to save the PDF with the default name and location
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")

        # Wait for the save to complete
        Start-Sleep -Seconds 2
    }
} else {
    Write-Output "Microsoft Edge is not running."
}
