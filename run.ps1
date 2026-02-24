Write-Output "Installing dependencies (if needed)..."
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Output "Starting server with venv Python (background)..."
Start-Process -FilePath .\.venv\Scripts\python.exe -ArgumentList "-m", "uvicorn", "main:app", "--reload"
