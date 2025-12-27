# BID-ZONE: Comprehensive Construction Estimating & Land Procurement Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**BID-ZONE** is an advanced AI-powered construction platform that combines enterprise-level estimating with comprehensive land procurement and development capabilities.

## 🎯 Overview

BID-ZONE provides a complete solution for construction professionals, from land acquisition through project estimation and delivery. The platform processes construction plans, performs due diligence analysis, generates development layouts, and produces professional cost estimates—all powered by specialized AI agents working in harmony.

## 🏗️ Core Capabilities

### 1. Construction Estimating
- **Multi-Format Ingestion**: ZIP, DWG, JPEG, PDF support
- **Specialized AI Agents**: Extract data by discipline (Structural, MEP, Finishes, Site Work)
- **Oracle Verification**: Quality assurance layer for accuracy
- **CSI Division Organization**: MasterFormat compliant output
- **Professional Excel Output**: Formatted estimates with audit trails

### 2. Land Procurement & Due Diligence
- **Market Analysis**: Comprehensive market research for development projects
- **Feasibility Studies**: Financial viability analysis with ROI calculations
- **Environmental Phase One**: ASTM E1527 environmental assessments
- **Financial Proforma**: Detailed projections with cash flow analysis

### 3. Land Planning & Rendering
- **Multiple Layout Options**: Generate 4-5 different development layouts
- **2D CAD-Quality Rendering**: Scaled drawings similar to AutoCAD output
- **3D Visualization**: Terrain, buildings, and infrastructure models
- **Zoning Analysis**: Automatic compliance checking

### 4. Earthwork & Grading
- **Cut/Fill Analysis**: Calculate earthwork quantities from elevation data
- **3D Cut/Fill Models**: Visual representation of cut and fill areas
- **Geotech Integration**: Process geotechnical reports for soil properties
- **Rock Excavation Analysis**: Identify and quantify rock excavation

### 5. Risk Management & Submittals
- **Automated Risk Analysis**: Identify missing items in plans
- **Cost Impact Assessment**: Quantify potential cost impacts
- **Submittal Schedules**: Generate submittal requirements from specs
- **Status Tracking**: Track submittal status and identify overdue items

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YUR-AI-CREATIONS/BID-ZONE-.git
cd BID-ZONE-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Configuration

Create a `.env` file with your API keys:

```env
# AI APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
GEMINI_API_KEY=your_gemini_key

# Folders
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# AI Settings
AI_MODEL=gpt-4
AI_TEMPERATURE=0.1
MAX_TOKENS=4000
```

### Basic Usage

#### Construction Estimating

```bash
# Process a construction plan
python main.py --project "Office Building" --file plans.pdf

# Process a ZIP archive
python main.py --project "Warehouse Complex" --file complete_plans.zip
```

#### Land Procurement Analysis

```python
from bid_zone.land_procurement import MarketAnalysis, FinancialProforma
from bid_zone.rendering import LandPlanner

# Market Analysis
market = MarketAnalysis()
analysis = market.analyze_market("123 Main St", radius_miles=5.0)
print(market.generate_report(analysis))

# Generate Land Layout Options
planner = LandPlanner()
boundary = [(0, 0), (2000, 0), (2000, 1000), (0, 1000)]
options = planner.generate_layout_options(boundary, "R-1")
print(planner.generate_comparison_report())
```

#### Complete Workflow

```bash
# Run complete workflow demonstration
python examples/complete_workflow.py
```

## 📁 Project Structure

```
BID-ZONE-/
├── src/
│   ├── core/                    # Core estimating system
│   │   ├── ingestion.py        # File ingestion system
│   │   ├── chunking.py         # Document chunking
│   │   ├── oracle.py           # Verification layer
│   │   ├── nucleus.py          # Aggregation engine
│   │   └── excel_export.py     # Excel generation
│   ├── agents/
│   │   └── agent_framework.py  # AI agent framework
│   ├── bid_zone/               # Extended capabilities
│   │   ├── land_procurement/   # Due diligence modules
│   │   ├── estimating/         # AI estimating
│   │   ├── rendering/          # 2D/3D visualization
│   │   ├── earthwork/          # Cut/fill analysis
│   │   └── reports/            # Report generation
│   ├── interfaces/
│   │   └── franklin_os.py      # Main orchestration
│   └── utils/
│       └── csi_divisions.py    # CSI standards
├── examples/                    # Usage examples
├── main.py                     # CLI application
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🎨 Key Features

### Agent Framework
- **Modular Design**: Easy to add new specialized agents
- **Parallel Processing**: Multiple agents work simultaneously
- **Confidence Scoring**: Track extraction quality
- **Agent Coordination**: Prevents overtalk and hallucination
- **Smart Selection**: Intelligent agent routing for efficiency

### Document Processing
- **Large File Handling**: Automatic chunking for oversized documents
- **Multi-API Vision**: OpenAI, Google Vision, Gemini integration
- **OCR Support**: Process scanned and hand-drawn plans
- **Progress Tracking**: Stage-by-stage status updates

### Professional Output
- **Excel Estimates**: CSI division organized with formatting
- **PDF Reports**: Comprehensive branded deliverables
- **2D/3D Visualizations**: CAD-quality renderings
- **Executive Summaries**: High-level project overviews

## 🔧 System Requirements

- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB disk space for installation
- Additional space for uploads and outputs
- API keys for AI services (OpenAI recommended minimum)

## 🐳 Docker Deployment

### Docker Compose Setup

```yaml
version: '3.8'
services:
  bid-zone:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
```

### One-Button Deploy

```bash
# Build and deploy
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 📖 Documentation

Comprehensive guides available:
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details
- [INSTALLATION.md](INSTALLATION.md) - Detailed installation guide
- [USER_GUIDE.md](USER_GUIDE.md) - User manual
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Smoke tests
python test_system.py
```

## 🔐 Security

- Never commit API keys to the repository
- Use environment variables for sensitive data
- Keep `.env` file private
- Review uploaded files before processing
- Implement rate limiting for production deployments

## 📋 Use Cases

### For Land Developers
- Evaluate acquisition opportunities with complete due diligence
- Generate multiple layout options to maximize value
- Create financial proformas with detailed projections
- Assess market conditions and absorption rates

### For Contractors & Estimators
- Quickly estimate projects from plans using AI
- Identify risks and missing items before bidding
- Generate professional estimates organized by division
- Track earthwork quantities with precision

### For Civil Engineers
- Analyze cut/fill quantities from grading plans
- Process geotechnical data for design parameters
- Generate 2D/3D visualizations of projects
- Create shop drawings and submittals

### For Project Managers
- Track submittal schedules and status
- Generate comprehensive project reports
- Manage risk throughout the project lifecycle
- Coordinate between design and construction

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

**YUR AI CREATIONS**

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 🚦 Status

**Current Version:** 1.0.0  
**Status:** Production Ready

---

Built with ❤️ by YUR AI CREATIONS
