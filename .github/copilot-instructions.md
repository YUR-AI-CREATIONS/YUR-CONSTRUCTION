

# Copilot Instructions for BID-ZONE

## System Overview
BID-ZONE is an AI-driven construction platform for estimating, land procurement, and development workflows. The architecture is modular, with clear separation between core logic, agent orchestration, and domain-specific modules.

### Architecture & Data Flow
- **Core logic**: `src/core/` handles document ingestion, chunking, verification (oracle), and Excel export.
- **Agents**: `src/agents/` contains the agent orchestration framework. Extend or register new agents in `agent_framework.py`.
- **Domain modules**: `src/bid_zone/` is organized by construction domain (estimating, earthwork, land procurement, rendering, reporting). Each submodule encapsulates a workflow step.
- **Orchestration**: `src/interfaces/franklin_os.py` coordinates agent and module execution.
- **Data flow**: Document ingestion → AI/estimation → calculation → reporting (Excel, AIA forms, schedules).

## Key Developer Workflows
- **Run full workflow**: `python main.py --project "Project Name" --file plans.pdf` (PDF or ZIP)
- **Demo end-to-end**: `python examples/complete_workflow.py`
- **Batch document processing**: `process_construction_docs.py` auto-discovers PDFs, runs estimates, outputs to `outputs/`
- **Land procurement & planning**: Use `bid_zone.land_procurement` and `bid_zone.rendering` modules for feasibility and layout generation

## Project Structure & Patterns
- **Estimation logic**: `src/bid_zone/estimating/detailed_calculator.py` (edit for cost/productivity/unit rates)
- **Schedule/report logic**: `src/bid_zone/reports/schedule_generator.py` (weather/productivity factors), `aia_templates.py` (AIA forms)
- **CSI MasterFormat**: `src/bid_zone/utils/csi_divisions.py` (all estimates organized by CSI Division)
- **Excel output**: Always includes audit trail and submittal/AIA links
- **Examples**: `examples/` for usage demos and workflow scripts

## Conventions & Integration
- **Extend agents**: via `src/agents/agent_framework.py` and register in orchestration (`franklin_os.py`)
- **API keys**: Set in `.env` (see README)
- **Outputs**: All generated files go to `outputs/` (create if missing)
- **Python version**: 3.8+; dependencies in `requirements.txt`
- **External APIs**: OpenAI, Anthropic, Google, Gemini (set keys in `.env`)

## Examples & References
- `README.md`: High-level overview, quick start
- `COMPREHENSIVE_PROCESSOR_README.md`: Technical details, output examples
- `examples/`: End-to-end workflow scripts

---
**For unclear or missing conventions, review code comments in the relevant module or open an issue for clarification.**


## Testing & Validation

- **Run all tests:**
	- `pytest tests/`
- **Run with coverage:**
	- `pytest --cov=src tests/`
- **Smoke/system test:**
	- `python test_system.py`

Test files are located at the project root and in the `tests/` directory. Use these commands to validate changes before submitting or integrating new code.


## Quick Start & Installation

- **Clone repository:**
	- `git clone https://github.com/YUR-AI-CREATIONS/BID-ZONE-.git`
	- `cd BID-ZONE-`
- **Create virtual environment:**
	- `python -m venv venv`
	- Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
- **Install dependencies:**
	- `pip install -r requirements.txt`
- **Install package (editable):**
	- `pip install -e .`
- **Configure environment:**
	- Create `.env` with required API keys and folders:
		```
		OPENAI_API_KEY=your_openai_key
		ANTHROPIC_API_KEY=your_anthropic_key
		GOOGLE_API_KEY=your_google_key
		GEMINI_API_KEY=your_gemini_key
		UPLOAD_FOLDER=uploads
		OUTPUT_FOLDER=outputs
		AI_MODEL=gpt-4
		AI_TEMPERATURE=0.1
		MAX_TOKENS=4000
		```

## Basic Usage Examples

- **Construction Estimating:**
	- `python main.py --project "Office Building" --file plans.pdf`
	- `python main.py --project "Warehouse Complex" --file complete_plans.zip`
- **Land Procurement Analysis:**
	- `from bid_zone.land_procurement import MarketAnalysis, FinancialProforma`
	- `from bid_zone.rendering import LandPlanner`
	- See `README.md` for code examples.
- **Complete Workflow Demo:**
	- `python examples/complete_workflow.py`

## Docker Deployment

- **Build and deploy:**
	- `docker-compose up -d`
- **Check status:**
	- `docker-compose ps`
- **View logs:**
	- `docker-compose logs -f`

Refer to `DEPLOYMENT.md`, `INSTALLATION.md`, and `README.md` for more details.


## Automated Setup Script

For a fully automated setup, use the provided PowerShell script:

- `setup.ps1` will:
	- Create a virtual environment (if missing)
	- Install dependencies and the package in editable mode
	- Create a `.env` file with required placeholders (if missing)
	- Run all tests, coverage, and system smoke tests

**Usage:**

```powershell
./setup.ps1
```

Run from the project root in a PowerShell terminal. Review output for any errors or required manual steps (e.g., entering API keys in `.env`).
