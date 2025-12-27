# BID-ZONE

**Construction Estimating and Land Procurement Due Diligence Software**

A comprehensive platform for construction estimation, land development analysis, and project management.

## Features

### Land Procurement Due Diligence
- **Market Analysis**: Comprehensive market research for residential development projects
- **Feasibility Studies**: Financial viability analysis with ROI calculations
- **Environmental Phase One**: ASTM E1527 environmental assessments
- **Financial Proforma**: Detailed financial projections with cash flow analysis

### Land Planning & Rendering
- **Multiple Layout Options**: Generate 4-5 different development layouts based on zoning
- **2D CAD-Quality Rendering**: Scaled drawings similar to AutoCAD output
- **3D Visualization**: Generate 3D models of terrain, buildings, and infrastructure
- **Zoning Analysis**: Automatic compliance checking with zoning requirements

### AI-Powered Estimating
- **Multi-API Vision Analysis**: Integrates OpenAI Vision, Google Vision, and Gemini Vision
- **PDF Processing**: Extract quantities from construction plans automatically
- **OCR for Scanned Documents**: Process hand-drawn or scanned plans
- **Itemized Estimates**: Professional estimates organized by CSI divisions
- **Metadata Extraction**: Parse plan metadata and in-field conditions

### Risk Management
- **Automated Risk Analysis**: Identify missing items in plans
- **Cost Impact Assessment**: Quantify potential cost impacts of risks
- **Mitigation Strategies**: Generate recommendations for risk reduction
- **Contingency Recommendations**: Data-driven contingency percentages

### Earthwork & Grading
- **Cut/Fill Analysis**: Calculate earthwork quantities from elevation data
- **3D Cut/Fill Models**: Visual representation of cut and fill areas
- **Swell/Shrinkage Factors**: Accurate volume calculations based on soil type
- **Geotech Integration**: Process geotechnical reports for soil properties
- **Rock Excavation Analysis**: Identify and quantify rock excavation requirements

### Submittal Management
- **Automated Submittal Schedules**: Generate submittal requirements from specs
- **Shop Drawing Requirements**: Detailed requirements for rebar, steel, earthwork
- **Status Tracking**: Track submittal status and identify overdue items
- **Professional Logs**: Generate submittal logs and reports

### Professional Reporting
- **Comprehensive Estimates**: Detailed estimates with division breakdowns
- **Executive Summaries**: High-level project summaries for stakeholders
- **Export Capabilities**: PDF, Excel, CSV, JSON export formats
- **Branded Reports**: Professional packages ready for client delivery

## Installation

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

## Quick Start

```python
from bid_zone.land_procurement import MarketAnalysis, FinancialProforma
from bid_zone.rendering import LandPlanner
from bid_zone.estimating import AIEstimator

# Market Analysis
market = MarketAnalysis()
analysis = market.analyze_market("123 Main St", radius_miles=5.0)
print(market.generate_report(analysis))

# Generate Land Layout Options
planner = LandPlanner()
boundary = [(0, 0), (2000, 0), (2000, 1000), (0, 1000)]
options = planner.generate_layout_options(boundary, "R-1")
print(planner.generate_comparison_report())

# AI-Powered Estimating
estimator = AIEstimator()
results = estimator.analyze_document("plans.pdf", use_api="all")
print(estimator.generate_report())
```

## Examples

See the `examples/` directory for complete workflow demonstrations:

```bash
python examples/complete_workflow.py
```

This will run through:
1. Complete land procurement due diligence
2. Multiple land layout generation
3. AI-powered document analysis and estimating
4. Cut/fill analysis with geotech integration
5. 2D/3D rendering examples
6. Report generation

## API Configuration

To use AI vision features, set your API keys as environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export GOOGLE_API_KEY="your-google-key"
export GEMINI_API_KEY="your-gemini-key"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-key
GEMINI_API_KEY=your-gemini-key
```

## Module Structure

```
bid_zone/
├── land_procurement/      # Market analysis, feasibility, environmental
├── estimating/           # AI estimating, document processing, risk analysis
├── rendering/            # 2D/3D rendering, land planning
├── earthwork/            # Cut/fill analysis, geotech processing
├── reports/              # Report generation, submittal management
└── utils/                # Utility functions
```

## Requirements

- Python 3.9+
- OpenAI API (for AI vision features)
- Google Cloud Vision API (optional)
- Gemini API (optional)

See `requirements.txt` for complete dependency list.

## Use Cases

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

## Documentation

Detailed documentation for each module:

- [Land Procurement Guide](docs/land_procurement.md)
- [AI Estimating Guide](docs/estimating.md)
- [Rendering & Planning Guide](docs/rendering.md)
- [Earthwork Analysis Guide](docs/earthwork.md)
- [Report Generation Guide](docs/reports.md)

## Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=bid_zone tests/
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Roadmap

- [ ] Web-based UI for easier interaction
- [ ] Real-time collaboration features
- [ ] Integration with major estimating databases (RSMeans, etc.)
- [ ] Mobile app for field data collection
- [ ] Machine learning for cost prediction
- [ ] Advanced 3D rendering with texture mapping
- [ ] Integration with BIM (Building Information Modeling)
- [ ] Automated permit application generation

## Acknowledgments

Built with industry-standard practices and tools:
- OpenAI GPT-4 Vision for intelligent document analysis
- Google Cloud Vision for OCR and image processing
- Gemini for advanced AI capabilities
- Standard construction industry databases and references
