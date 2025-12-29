# BID-ZONE Automated Setup Script
# This PowerShell script automates environment setup, dependency installation, .env creation, and test execution for BID-ZONE.

# Clone the repository (if not already cloned)
# git clone https://github.com/YUR-AI-CREATIONS/BID-ZONE-.git
# cd BID-ZONE-

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activate virtual environment
$venvActivate = "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    . $venvActivate
} else {
    Write-Host "ERROR: Could not find venv activation script."
    exit 1
}

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .

# Create .env file with placeholders if it doesn't exist
$envPath = ".env"
if (-not (Test-Path $envPath)) {
    @"
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
GEMINI_API_KEY=your_gemini_key
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs
AI_MODEL=gpt-4
AI_TEMPERATURE=0.1
MAX_TOKENS=4000
"@ | Out-File -Encoding UTF8 $envPath
    Write-Host ".env file created with placeholder values."
} else {
    Write-Host ".env file already exists."
}

# Run tests
Write-Host "Running all tests..."
pytest tests/

Write-Host "Running tests with coverage..."
pytest --cov=src tests/

Write-Host "Running system smoke test..."
python test_system.py

Write-Host "\nBID-ZONE setup and validation complete."
