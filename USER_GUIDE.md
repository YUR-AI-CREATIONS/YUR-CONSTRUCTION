# User Guide

## Introduction

BID-ZONE is an enterprise-grade construction estimating platform that uses AI to analyze construction plans and generate detailed cost estimates.

## Getting Started

### Basic Workflow

1. **Prepare Your Files** - Construction plans in PDF, ZIP, DWG, or image format
2. **Run BID-ZONE** - Process files using the command-line interface
3. **Review Output** - Examine the generated Excel estimate
4. **Audit Results** - Check the audit trail for transparency

## Command-Line Interface

### Basic Usage

```bash
python main.py --project "Project Name" --file path/to/plan.pdf
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project` | Project name (required) | - |
| `--file` | Path to plan file (required) | - |
| `--output` | Output directory | `outputs` |
| `--no-consolidate` | Disable duplicate consolidation | False |
| `--verbose` | Enable verbose output | False |

### Examples

**Process a single PDF:**
```bash
python main.py --project "Office Building" --file plans.pdf
```

**Process a ZIP archive:**
```bash
python main.py --project "Warehouse" --file complete_set.zip
```

**Custom output directory:**
```bash
python main.py --project "Renovation" --file plans.pdf --output my_estimates
```

**Verbose mode:**
```bash
python main.py --project "Complex" --file plans.pdf --verbose
```

## Understanding the Output

### Excel Estimate Structure

The generated Excel file contains four sheets:

#### 1. Summary Sheet
- Project information
- Cost summary by CSI division
- Grand total
- High-level overview

#### 2. Detailed Estimate
- Line-by-line cost items
- Organized by CSI division
- Includes:
  - Item descriptions
  - Quantities
  - Units of measure
  - Unit prices
  - Extended totals
  - Scope notes
  - Agent identification

#### 3. CSI Divisions
- Reference guide to MasterFormat divisions
- Division codes and names
- Descriptions

#### 4. Audit Trail
- Processing timestamps
- Agent assignments
- Chunk processing status
- Verification results
- Processing metadata

### Reading the Estimate

**Cost Structure:**
```
Item # | CSI Div | Description | Scope | Qty | Unit | Unit Price | Total | Agent
1      | 03      | Concrete    | Found | 100 | CY   | $150.00    | $15K  | structural-001
```

**Division Totals:**
- Each division shows subtotal
- Grand total at bottom
- Easy to compare costs by trade

## File Input Guidelines

### Supported Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| PDF | .pdf | Plan sets, specifications |
| ZIP | .zip | Multiple files in archive |
| DWG | .dwg | AutoCAD drawings |
| JPEG | .jpg, .jpeg | Scanned plans |
| PNG | .png | Digital images |

### Best Practices

**For Best Results:**
- Use high-resolution PDFs (300 DPI or higher)
- Include complete plan sets
- Organize ZIP archives logically
- Name files descriptively
- Keep file sizes under 100MB

**File Organization:**
```
project_plans.zip
├── site_plan.pdf
├── foundation_plan.pdf
├── floor_plans.pdf
├── elevations.pdf
└── details.pdf
```

## AI Agent Specialties

### Structural Agent
- Concrete work
- Steel framing
- Foundations
- Load-bearing elements

### MEP Agent
- Mechanical systems (HVAC)
- Electrical systems
- Plumbing fixtures and piping
- Fire suppression

### Finishes Agent
- Drywall and framing
- Paint and coatings
- Flooring materials
- Ceiling systems

### Site Work Agent
- Excavation and grading
- Paving and surfacing
- Site utilities
- Landscaping

## Verification and Quality

### Oracle Verification

Every estimate goes through verification:
- ✓ Item completeness check
- ✓ Calculation validation
- ✓ Required field verification
- ✓ Confidence scoring

### Confidence Scores

| Score | Meaning |
|-------|---------|
| 90-100% | High confidence |
| 70-89% | Good confidence |
| 50-69% | Moderate confidence |
| <50% | Review recommended |

### Common Issues

**Low Confidence Scores:**
- Poor image quality
- Incomplete plans
- Handwritten notes (not OCR'd)
- Non-standard format

**How to Improve:**
- Provide clearer source files
- Include specifications
- Add detail sheets
- Use digital CAD files when available

## Advanced Features

### Duplicate Consolidation

By default, BID-ZONE consolidates duplicate items:

```bash
# Enable (default)
python main.py --project "Name" --file plan.pdf

# Disable
python main.py --project "Name" --file plan.pdf --no-consolidate
```

**What It Does:**
- Combines items with same description
- Sums quantities and totals
- Averages unit prices
- Tracks merged items

### Python API

Use BID-ZONE programmatically:

```python
from src.interfaces.franklin_os import FranklinOS

# Initialize
franklin = FranklinOS(config={
    'output_folder': 'my_outputs'
})

# Process project
result = franklin.process_project(
    project_name="Office Building",
    file_path="plans.pdf",
    consolidate_duplicates=True
)

# Access results
print(f"Total: ${result['summary']['total_cost']:,.2f}")
print(f"Excel: {result['excel_file']}")

# Get system status
status = franklin.get_system_status()
print(status)
```

## Workflow Integration

### With Project Management Tools

1. Export estimates to Excel
2. Import into project management software
3. Track costs against estimates
4. Update as needed

### With Accounting Systems

1. Generate estimates in BID-ZONE
2. Export line items
3. Import to accounting software
4. Track actuals vs. estimates

## Tips and Best Practices

### 1. File Preparation
- Clean, legible plans
- Complete plan sets
- Current revisions
- Digital formats preferred

### 2. Project Organization
- Use descriptive project names
- Maintain folder structure
- Keep source files
- Archive estimates

### 3. Review Process
- Check confidence scores
- Verify quantities
- Review unit prices
- Validate totals
- Spot-check calculations

### 4. Customization
- Add your own unit prices
- Adjust quantities as needed
- Include markups separately
- Document assumptions

## Troubleshooting

### No Items Extracted
- Check file format
- Verify file integrity
- Ensure plans are readable
- Try different file format

### Incorrect Quantities
- Verify scale on plans
- Check unit of measure
- Review extraction notes
- Manual adjustment may be needed

### Missing Divisions
- Not all divisions may apply
- Agent specialties vary
- Some items may not be visible in plans
- Add manually if needed

## Support and Resources

### Documentation
- README.md - Overview
- INSTALLATION.md - Setup guide
- This file - User guide

### Examples
- `examples/example_usage.py` - Code examples
- `test_data/` - Sample files

### Testing
- `test_system.py` - Validation tests

### Getting Help
- Open GitHub issue
- Check documentation
- Review examples
- Contact support

## Frequently Asked Questions

**Q: What file size limits exist?**
A: Default is 100MB. Configure in .env file.

**Q: Can I add my own agents?**
A: Yes! See agent_framework.py for examples.

**Q: Are estimates accurate?**
A: Estimates are AI-generated and should be reviewed. Confidence scores indicate quality.

**Q: Can I edit the Excel output?**
A: Yes, Excel files are fully editable.

**Q: Does it work offline?**
A: No, AI processing requires API access.

**Q: What about privacy?**
A: Files are processed securely. Check your AI provider's terms.

## Next Steps

1. ✅ Process your first project
2. 📊 Review the Excel estimate
3. ✏️ Customize as needed
4. 🔄 Integrate into workflow

Happy estimating!
