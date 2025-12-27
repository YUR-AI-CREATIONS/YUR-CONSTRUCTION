# Comprehensive Construction Document Processor

This script processes real construction documents and generates detailed, industry-standard estimates with all required elements.

## Features

The `process_construction_docs.py` script provides:

### 📊 Detailed Quantified Takeoffs
- **Paving**: Square yards (SY), thickness, PSI strength, rebar specifications (#3 @ 16" OC), lime-stabilized subgrade
- **Utilities**: Linear feet (LF), pipe diameter, excavation volumes, bedding volumes, crew productivity (600-800 LF/day)
- **Earthwork**: Cut/fill analysis with swell factors (1.25 for silty clay), shrinkage factors (0.90), import/export calculations
- **Concrete**: Volume (CY), area (SF/SY), thickness, PSI, finish type, rebar tonnage, crew productivity (300 SF/day/finisher)

### 📑 Excel Output with All Details
Generated Excel workbook includes:
- **Summary Sheet**: Project overview and division totals
- **Detailed Estimate Sheet**: Line-by-line with:
  - Item number
  - CSI Division
  - Description
  - Scope of work
  - Quantity
  - Unit
  - Unit price
  - Total price
  - **Submittal links** (embedded hyperlinks to product data)
  - **AIA Agreement links** (embedded hyperlinks to subcontractor agreements)
  - Processing agent
- **CSI Divisions Sheet**: MasterFormat reference
- **Audit Trail Sheet**: Processing metadata

### 📅 Integrated Construction Schedule
- Industry-standard activity sequencing (mobilization → earthwork → utilities → paving → concrete → cleanup)
- Productivity rates based on real-world standards:
  - Earthwork: 500 CY/day
  - Utilities: 600-800 LF/day
  - Concrete paving: 1,500 SY/day
  - Finishers: 300 SF/day/finisher
- **Weather adjustments**: January/February reduced to 70% productivity for cold/rainy conditions
- Activity dependencies and critical path
- Cost breakdown by activity
- Gantt-style text output

### 📄 AIA Agreement Templates
Generates complete subcontractor packages for each division:
- **AIA A401**: Standard Form of Agreement Between Contractor and Subcontractor
- **AIA G702**: Application and Certificate for Payment
- **AIA G703**: Continuation Sheet (line item details)

All forms include:
- Project information
- Scope of work by division
- Contract amounts
- Payment terms
- Warranty provisions
- Insurance requirements

### 🔢 Advanced Construction Calculations

#### Paving
```python
# Example: 3,333 SY at 6" thick, 3000 PSI
- Concrete volume: Area × thickness / 27 = CY
- Rebar tonnage: Based on spacing and size
- Subgrade treatment cost
- Forming and finishing costs
- Unit cost per SY includes all components
```

#### Utilities
```python
# Example: 985 LF of 8" water line
- Trench excavation: Width (dia + 24") × depth × length / 27
- Bedding volume: 6" under pipe
- Backfill volume: Excavation - pipe volume - bedding
- Crew days: Length / 700 LF/day production rate
- Cost includes: excavation, pipe, bedding, backfill, labor
```

#### Earthwork
```python
# Example: 1,500 CY cut, 1,200 CY fill
- Swell factor: 1.25 for silty clay (volume increases when excavated)
- Shrinkage factor: 0.90 (volume decreases when compacted)
- Adjusted cut: 1,500 × 1.25 = 1,875 CY
- Adjusted fill: 1,200 / 0.90 = 1,333 CY
- Import/export: Difference between adjusted volumes
```

#### Weather-Adjusted Scheduling
```python
# January/February: 70% productivity
# Base duration: 5 days
# Adjusted duration: 5 / 0.70 = 7.1 days (rounded to 8)
# Lost days: 3 days due to weather
```

## Usage

### Basic Usage

```bash
# Process construction documents in repository
python process_construction_docs.py
```

The script will:
1. Find all PDF files in the repository root
2. Process the "JCK BATCH PLANT - WATER LINE PLANS.pdf" (if present)
3. Generate detailed estimates based on document analysis
4. Create Excel workbook with all details
5. Generate construction schedule
6. Generate AIA agreement templates for each division
7. Output JSON summary

### Output Files

All files are generated in the `outputs/` directory:

```
outputs/
├── Whiskey_River_Development_20251227_050604.xlsx  # Complete estimate
├── Whiskey_River_Development_summary.json           # JSON summary
└── aia_agreements/
    ├── AIA_A401_03_Concrete.txt                    # Subcontractor agreement
    ├── AIA_G702_03_Concrete.txt                    # Payment application
    ├── AIA_G703_03_Concrete.txt                    # Continuation sheet
    ├── AIA_A401_31_Earthwork.txt
    ├── AIA_G702_31_Earthwork.txt
    ├── AIA_G703_31_Earthwork.txt
    ├── AIA_A401_33_Utilities.txt
    ├── AIA_G702_33_Utilities.txt
    └── AIA_G703_33_Utilities.txt
```

## Example Output

### Console Output
```
================================================================================
PROCESSING: Whiskey River Development
================================================================================

💧 Water Line Estimate:
  ✓ 985 LF @ $62.89/LF = $61,942.14
    Excavation: 486.4 CY
    Bedding: 48.6 CY
    Crew Days: 1.4 days @ 700 LF/day

🛣️  Paving Estimate:
  ✓ 3,333 SY @ $68.58/SY = $228,588.25
    Concrete: 555.5 CY @ $170/CY
    Rebar: 49.99 Tons
    Thickness: 6.0"
    Strength: 3000 PSI
    Crew Days: 1.0 days

⛏️  Earthwork Estimate:
  ✓ Cut: 1,500 CY
    Fill: 1,200 CY
    Swell Factor: 1.25
    Shrinkage Factor: 0.90
    Adjusted Cut: 1,875 CY (after swell)
    Adjusted Fill: 1,333 CY (after shrinkage)
    Import/Export: 542 CY (Export)
    Total Cost: $44,833.33

================================================================================
GRAND TOTAL: $420,888.95
Total Line Items: 5
================================================================================
```

### Schedule Output
```
CONSTRUCTION SCHEDULE - GANTT CHART
====================================
Project: Whiskey River Development
Start Date: 2025-12-27
Total Duration: 48 days

ID         Activity                                 Duration   Start        End          Cost           
===================================================================================================
MOB-001    Mobilization and Site Setup                   5.0 d 2025-12-27   2026-01-01   $       10,000
EW-001     Mass Grading and Earthwork                    8.0 d 2026-01-01   2026-01-13   $       36,000
UT-001     Water Line Installation                       2.0 d 2026-01-13   2026-01-15   $        5,000
UT-002     Sanitary Sewer Installation                   2.0 d 2026-01-15   2026-01-19   $        5,000
PV-001     Base Preparation and Compaction               5.0 d 2026-01-19   2026-01-26   $       17,500
PV-002     Concrete Paving 6.0" @ 3000 PSI               3.0 d 2026-01-26   2026-01-29   $       15,000
CN-001     Sidewalk Installation                         8.0 d 2026-01-29   2026-02-10   $        9,600
CLN-001    Final Grading, Cleanup, and Punchlist         3.0 d 2026-02-10   2026-02-13   $        4,500
===================================================================================================
                                                               Total: $      102,600
```

## Customization

### Adjusting Unit Prices

Edit `src/bid_zone/estimating/detailed_calculator.py`:

```python
class DetailedCalculator:
    def __init__(self):
        # Standard unit costs (adjust as needed)
        self.concrete_cost_per_cy = 170.0  # $170/CY for 3000 PSI
        self.rebar_cost_per_ton = 950.0
        self.excavation_cost_per_cy = 15.0
        self.utility_crew_cost_per_day = 2500.0
```

### Adjusting Productivity Rates

Edit productivity rates in the same file:

```python
        # Productivity rates
        self.finisher_production_sf_per_day = 300.0
        self.utility_crew_production_lf_per_day = 700.0
        self.portable_batch_plant_capacity_cy_per_day = 1850.0
```

### Adjusting Weather Factors

Edit `src/bid_zone/reports/schedule_generator.py`:

```python
        # Weather adjustment factors by month
        self.weather_factors = {
            1: 0.70,   # January - cold, rainy (70% productivity)
            2: 0.70,   # February - cold, rainy
            3: 0.85,   # March - improving
            # ... etc
        }
```

## Integration with Existing System

This comprehensive processor integrates with the existing BID-ZONE system:

- Uses existing `AIEstimator` for document analysis
- Uses existing `ExcelExporter` for workbook generation
- Extends functionality with new calculation modules
- Compatible with existing agent framework
- Can be called from API server or command line

## Technical Details

### Module Dependencies

- `DetailedCalculator`: Construction-specific calculations
  - Paving with concrete, rebar, subgrade
  - Utilities with excavation, bedding, backfill
  - Earthwork with swell/shrinkage factors
  - Concrete pours with productivity scheduling
  
- `ScheduleGenerator`: Construction scheduling
  - Activity sequencing with dependencies
  - Productivity-based duration calculation
  - Weather factor adjustments
  - Critical path identification
  
- `AIATemplateGenerator`: Industry-standard forms
  - AIA A401 subcontractor agreements
  - AIA G702 payment applications
  - AIA G703 continuation sheets

### Data Flow

```
Construction Documents (PDF)
    ↓
Document Analysis (AIEstimator)
    ↓
Detailed Calculations (DetailedCalculator)
    ↓
Estimate Items organized by CSI Division
    ↓
├── Excel Export (with submittals & AIA links)
├── Schedule Generation (with weather adjustment)
└── AIA Agreement Templates (per division)
```

## Support

For questions or issues:
1. Check this README for usage instructions
2. Review example output in `outputs/` directory
3. Examine source code comments for calculation details
4. Open an issue on GitHub

## License

MIT License - See LICENSE file for details
