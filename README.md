# BID-ZONE: Enterprise Construction Estimating Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**BID-ZONE** is an advanced AI-powered construction estimating platform that processes large plan sets and generates comprehensive, professionally formatted cost estimates with CSI division breakdowns.

## 🎯 Overview

BID-ZONE ingests construction plans in multiple formats (ZIP, DWG, JPEG, PDF) and uses specialized AI agents to extract detailed cost data, organize it by CSI MasterFormat divisions, and deliver perfectly formatted Excel estimates with full auditability.

## 🏗️ Architecture

### Core Components

1. **File Ingestion System** - Handles multiple file formats
   - ZIP archives
   - DWG (AutoCAD) files
   - JPEG/PNG images
   - PDF documents

2. **Document Chunking** - Intelligently decomposes plans into processable chunks

3. **Specialized AI Agents** - Extract scoped construction data
   - Structural Agent (Concrete, Steel)
   - MEP Agent (Mechanical, Electrical, Plumbing)
   - Finishes Agent (Drywall, Paint, Flooring)
   - Site Work Agent (Excavation, Paving, Utilities)

4. **Oracle Verification Layer** - Validates agent outputs for accuracy

5. **Nucleus Aggregator** - Combines and consolidates results

6. **Excel Export System** - Generates professional estimates with:
   - CSI division organization
   - Itemized costs
   - Unit pricing
   - Totals and subtotals
   - Embedded scopes
   - Audit trail

7. **Franklin OS Interface** - Primary delivery interface

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YUR-AI-CREATIONS/BID-ZONE-.git
cd BID-ZONE-
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

Process a construction plan:

```bash
python main.py --project "Office Building" --file plans.pdf
```

Process a ZIP archive:

```bash
python main.py --project "Warehouse Complex" --file complete_plans.zip
```

## 📊 Features

### Input Support
- ✅ **ZIP Archives** - Automatic extraction and processing
- ✅ **PDF Documents** - Page-by-page analysis
- ✅ **DWG Files** - Layer-based extraction
- ✅ **Images** - JPEG, PNG format support

### Output Features
- ✅ **CSI Division Organization** - MasterFormat compliant
- ✅ **Itemized Estimates** - Detailed line items
- ✅ **Unit Pricing** - Quantity, unit, and extended costs
- ✅ **Professional Formatting** - Excel with styled headers
- ✅ **Audit Trail** - Agent identification and timestamps
- ✅ **Progress Tracking** - Stage-by-stage status
- ✅ **Verification** - Quality assurance checks

### AI Agent Framework
- **Modular Design** - Easy to add new specialized agents
- **Parallel Processing** - Multiple agents work simultaneously
- **Confidence Scoring** - Track extraction quality
- **Agent Attribution** - Know which agent extracted each item

## 📁 Project Structure

```
BID-ZONE-/
├── src/
│   ├── core/
│   │   ├── ingestion.py      # File ingestion system
│   │   ├── chunking.py       # Document chunking
│   │   ├── oracle.py         # Verification layer
│   │   ├── nucleus.py        # Aggregation engine
│   │   └── excel_export.py   # Excel generation
│   ├── agents/
│   │   └── agent_framework.py # AI agent framework
│   ├── interfaces/
│   │   └── franklin_os.py     # Main interface
│   └── utils/
│       └── csi_divisions.py   # CSI standards
├── main.py                     # CLI application
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔧 Configuration

Edit `.env` file to configure:

```env
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Folders
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# AI Settings
AI_MODEL=gpt-4
AI_TEMPERATURE=0.1
MAX_TOKENS=4000
```

## 📖 Usage Examples

### Command Line

```bash
# Basic usage
python main.py --project "My Project" --file plan.pdf

# Custom output directory
python main.py --project "My Project" --file plan.pdf --output my_estimates

# Disable duplicate consolidation
python main.py --project "My Project" --file plan.pdf --no-consolidate

# Verbose mode
python main.py --project "My Project" --file plan.pdf --verbose
```

### Python API

```python
from src.interfaces.franklin_os import FranklinOS

# Initialize
franklin = FranklinOS()

# Process a project
result = franklin.process_project(
    project_name="Office Building",
    file_path="plans.pdf"
)

# Access results
print(f"Total Cost: ${result['summary']['total_cost']:,.2f}")
print(f"Excel File: {result['excel_file']}")
```

## 🎨 Excel Output Structure

The generated Excel estimate includes:

1. **Summary Sheet** - Project overview and cost summary by division
2. **Detailed Estimate** - Line-by-line items with CSI divisions
3. **CSI Divisions** - Reference guide to MasterFormat divisions
4. **Audit Trail** - Processing history and agent attribution

## 🔍 CSI Division Coverage

- Division 00: Procurement and Contracting
- Division 01: General Requirements
- Division 02: Existing Conditions
- Division 03: Concrete
- Division 04: Masonry
- Division 05: Metals
- Division 06: Wood, Plastics, and Composites
- Division 07: Thermal and Moisture Protection
- Division 08: Openings
- Division 09: Finishes
- Division 10-14: Specialties and Equipment
- Division 21-28: Fire Suppression, MEP, and Security
- Division 31-33: Sitework and Utilities

## 🛠️ Development

### Adding New Agents

Create a new agent class in `src/agents/agent_framework.py`:

```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__('custom-001', 'Custom Specialty')
    
    def _extract_data(self, chunk):
        # Your extraction logic
        return {
            'csi_division': '10',
            'items': [...],
            'scope': 'Custom scope',
            'notes': 'Extracted by custom agent'
        }
```

Register the agent in `AgentFramework`:

```python
self.agents['custom'] = CustomAgent()
```

## 📋 System Requirements

- Python 3.8 or higher
- 2GB RAM minimum (4GB recommended)
- 100MB disk space for installation
- Additional space for uploads and outputs

## 🔐 Security

- Never commit API keys to the repository
- Use environment variables for sensitive data
- Keep `.env` file private
- Review uploaded files before processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

**YUR AI CREATIONS**

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📞 Support

For issues and questions, please open an issue on GitHub.

## 🚦 Status

**Current Version:** 1.0.0  
**Status:** Production Ready

---

Built with ❤️ by YUR AI CREATIONS
