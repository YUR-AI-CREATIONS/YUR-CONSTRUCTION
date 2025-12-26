# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- 2GB RAM minimum (4GB recommended)
- 100MB disk space

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/YUR-AI-CREATIONS/BID-ZONE-.git
cd BID-ZONE-
```

### 2. Create Virtual Environment (Recommended)

**On Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- File processing libraries (PyPDF2, Pillow, ezdxf)
- Excel generation (openpyxl, xlsxwriter)
- Data processing (pandas, numpy)
- AI integration (openai, anthropic)
- Web framework (flask, flask-cors)

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 5. Verify Installation

Run the system tests:

```bash
python test_system.py
```

You should see:
```
======================================================================
ALL TESTS PASSED ✓
======================================================================
```

## Quick Start

Process a construction plan:

```bash
python main.py --project "My Project" --file plans.pdf
```

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### Permission Errors

On Linux/Mac, you may need to make scripts executable:

```bash
chmod +x main.py
```

### Memory Issues

For large files, increase Python's memory limit or process files in smaller batches.

### File Format Issues

Supported formats:
- PDF: .pdf
- Images: .jpg, .jpeg, .png
- CAD: .dwg
- Archives: .zip

## Optional Dependencies

For advanced features:

```bash
# For better PDF handling
pip install pypdf

# For OCR support
pip install pytesseract

# For web interface
pip install flask-socketio
```

## Development Setup

For development work:

```bash
# Install in editable mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black flake8
```

## Docker Installation (Alternative)

If you prefer Docker:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:

```bash
docker build -t bid-zone .
docker run -v $(pwd)/outputs:/app/outputs bid-zone --project "Test" --file plan.pdf
```

## Next Steps

1. ✅ Installation complete
2. 📖 Read the [User Guide](USER_GUIDE.md)
3. 🚀 Process your first project
4. 📊 Review the generated Excel estimate

## Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review example files in `examples/`
