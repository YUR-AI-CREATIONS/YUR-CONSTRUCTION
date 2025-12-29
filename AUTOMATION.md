
# Automated Setup

To fully automate BID-ZONE installation, configuration, and validation:

1. Open a PowerShell terminal in the project root.
2. Run:

   ```powershell
   ./setup.ps1
   ```

- This script will:
  - Create a virtual environment (if missing)
  - Install dependencies and the package in editable mode
  - Create a `.env` file with required placeholders (if missing)
  - Run all tests, coverage, and system smoke tests

- After running, edit `.env` to add your real API keys.
- Review the output for any errors or manual steps required.

See `.github/copilot-instructions.md` for more details.
