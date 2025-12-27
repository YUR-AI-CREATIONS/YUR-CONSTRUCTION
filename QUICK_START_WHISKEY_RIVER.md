# Quick Start Guide: Whiskey River Water Line & Paving Estimate

This guide shows how to generate the detailed estimate you requested for the Whiskey River project.

## What You Asked For

> "All right so on Whiskey River give me estimate on the water line and the paving The detailed estimate"

## Running the Estimator

```bash
# Simply run this command:
python process_construction_docs.py
```

That's it! The script will automatically:
1. Find the "JCK BATCH PLANT - WATER LINE PLANS.pdf" in your repository
2. Generate detailed takeoffs for water line and paving
3. Include all the nitty-gritty details you specified

## What You Get

### 💧 Water Line (from JCK BATCH PLANT plans)
```
985 LF of 8" PVC Water Line
Unit Price: $62.89/LF
Total: $61,942.14

Details:
- Excavation: 486.4 CY
- Bedding material: 48.6 CY
- Backfill: Calculated after pipe volume
- Crew: 6 workers @ $2,500/day
- Production: 600-800 LF/day
- Duration: 1.4 days
```

### 🛣️ Paving (Subdivision roads)
```
3,333 SY (30,000 SF)
6" thick, 3000 PSI
#3 rebar @ 16" on center
Lime stabilized subgrade
Unit Price: $68.58/SY
Total: $228,588.25

Details:
- Concrete: 555.5 CY @ $170/CY
- Rebar: 49.99 Tons (calculated for #3 @ 16" OC)
- Subgrade treatment: $26,664 (lime stabilization)
- Forming: $15,000
- Finishing: $45,000
- Finishers: 300 SF/day production rate
```

### ⛏️ Earthwork with Cut/Fill Analysis
```
Cut: 1,500 CY
Fill: 1,200 CY

Soil Type: Silty Clay (Texas regional data)
Swell Factor: 1.25 (volume increases 25% when excavated)
Shrinkage Factor: 0.90 (volume decreases 10% when compacted)

Adjusted Volumes:
- Cut: 1,875 CY (after swell)
- Fill: 1,333 CY (required borrow, after shrinkage)
- Net Export: 542 CY

Total: $44,833.33
```

### 🚶 Additional Items (Sidewalks)
```
2,200 SF (244 SY)
4" thick, 3000 PSI
Broom finish
Total: $9,017.93
```

### 🚿 Sanitary Sewer
```
1,100 LF of 8" PVC
Depth: 6 feet average
Crew Days: 1.6 days
Total: $76,507.30
```

## 📊 Grand Total: $420,888.95

## 📅 Construction Schedule (48 days total)

The schedule accounts for weather (January/February = 70% productivity):

```
Week 1:     Mobilization (5 days)
Week 2:     Earthwork - Cut/Fill (8 days, weather-adjusted)
Week 3:     Water Line + Sewer (4 days)
Week 4-5:   Base Prep + Paving (8 days)
Week 6-7:   Sidewalks (8 days)
Week 8:     Final Grading & Cleanup (3 days)
```

## 📄 Generated Files

Look in the `outputs/` folder for:

1. **Excel Workbook** (`Whiskey_River_Development_*.xlsx`)
   - Summary sheet with division totals
   - Detailed estimate with ALL line items
   - Submittals column (links to product data)
   - AIA Agreement column (links to subcontractor agreements)
   - CSI division reference
   - Audit trail

2. **AIA Agreement Templates** (`outputs/aia_agreements/`)
   - AIA A401: Subcontractor agreements for each division
   - AIA G702: Payment applications
   - AIA G703: Continuation sheets with line items

3. **JSON Summary** (`Whiskey_River_Development_summary.json`)
   - Machine-readable format
   - All quantities and costs
   - Schedule activities
   - Document metadata

## 🔍 Detailed Breakdown by Division

### Division 03 - Concrete
| Item | Description | Qty | Unit | Price | Total |
|------|-------------|-----|------|-------|-------|
| 03-001 | 6" Paving, 3000 PSI, #3 @ 16" OC | 3,333 | SY | $68.58 | $228,588.25 |
| 03-002 | 4" Sidewalks, broom finish | 244 | SY | $36.89 | $9,017.93 |
| **Subtotal** | | | | | **$237,606.18** |

### Division 31 - Earthwork
| Item | Description | Qty | Unit | Price | Total |
|------|-------------|-----|------|-------|-------|
| 31-001 | Mass Grading, silty clay | 2,700 | CY | $16.60 | $44,833.33 |
| **Subtotal** | | | | | **$44,833.33** |

### Division 33 - Utilities
| Item | Description | Qty | Unit | Price | Total |
|------|-------------|-----|------|-------|-------|
| 33-001 | 8" Water Line w/ bedding | 985 | LF | $62.89 | $61,942.14 |
| 33-002 | 8" Sanitary Sewer w/ MH | 1,100 | LF | $69.55 | $76,507.30 |
| **Subtotal** | | | | | **$138,449.44** |

## 💡 Understanding the Calculations

### Paving per Square Yard
- Area: 30,000 SF ÷ 9 = 3,333 SY
- Thickness: 6 inches (0.5 feet)
- Concrete: 3,333 SY × 0.5 FT ÷ 27 = 555.5 CY
- Rebar: #3 @ 16" OC = ~0.015 tons/SY = 49.99 tons
- Cost breakdown:
  - Concrete: $94,435 (555.5 CY × $170)
  - Rebar: $47,491 (49.99 tons × $950)
  - Subgrade: $26,664 (3,333 SY × $8)
  - Forming: $15,000 (30,000 SF × $0.50)
  - Finishing: $45,000 (30,000 SF × $1.50)
  - **Total: $228,588**

### Utilities per Linear Foot
Water line @ $62.89/LF includes:
- Pipe material: $45/LF (8" PVC)
- Excavation: $7.29/LF (trench @ $15/CY)
- Bedding: $1.72/LF (6" sand @ $35/CY)
- Backfill: $5.43/LF (@ $12/CY)
- Labor: $3.45/LF (crew cost @ $2,500/day ÷ 700 LF)

### Earthwork with Swell/Shrinkage
- Bank measure cut: 1,500 CY
- Loose measure (after excavation): 1,500 × 1.25 = 1,875 CY
- Compacted fill needed: 1,200 CY
- Borrow required: 1,200 ÷ 0.90 = 1,333 CY (bank measure)
- Haul away: 1,875 - 1,333 = 542 CY @ $8/CY

## 🌦️ Weather & Productivity Notes

**Starting in January:**
- Concrete work limited due to cold temperatures
- 70% productivity factor applied to earthwork
- Rain delays expected for utility installation
- Schedule includes contingency for weather

**Recommendations:**
- Use portable batch plant for faster concrete production (1,700-2,000 CY/day vs 1,000 CY/day with trucks)
- Start earthwork in late February/early March for better productivity
- Have heated enclosures ready for concrete curing in cold weather
- Consider accelerators for concrete if pouring in cold weather

## 📋 Submittals Required

For each division, you'll need:

**Division 03 - Concrete:**
- Mix designs (3000 PSI)
- Rebar shop drawings
- Admixture product data
- Concrete strength test reports

**Division 31 - Earthwork:**
- Compaction test procedures
- Fill material source & testing
- Erosion control plan
- SWPPP documentation

**Division 33 - Utilities:**
- Pipe shop drawings (8" PVC)
- Pressure test procedures
- Manhole details
- Connection details

## 🤝 Subcontractor Agreements

AIA A401 agreements are generated for:
- Concrete subcontractor ($237,606)
- Earthwork subcontractor ($44,833)
- Utilities subcontractor ($138,449)

Each includes:
- Scope of work
- Payment terms (monthly applications)
- Retainage schedule (10% → 5%)
- Insurance requirements
- Warranty provisions (1 year)

## Need More Detail?

For the full documentation with all formulas and technical details, see:
- `COMPREHENSIVE_PROCESSOR_README.md` - Complete technical documentation
- Excel file - Interactive workbook with all line items
- JSON file - Machine-readable data for integration

## Questions?

The system has all the logic built in. Just run:
```bash
python process_construction_docs.py
```

Everything you specified is calculated automatically:
✅ Per square yard for flat paving  
✅ Thickness (6 inches)  
✅ 3000 PSI strength  
✅ #3 rebar @ 16 inches on center  
✅ Lime stabilized subgrade  
✅ Tonnage calculations  
✅ All utilities nitty-gritty details  
✅ Earthwork cut/fill with contours  
✅ Swelling factors by soil type  
✅ Weather-adjusted schedule  
✅ Crew productivity rates  
✅ Submittal links  
✅ AIA agreements per division  
