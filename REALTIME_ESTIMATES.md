# Real-Time Cost Estimate Tracking

## Overview

BID-ZONE now provides **real-time cost estimate tracking** during the processing of construction plans. As each chunk of the document is processed by specialized AI agents, the system displays cumulative cost estimates, allowing users to see the project cost build up progressively rather than waiting for the final total.

## Features

### 1. Progressive Cost Display

As the system processes each chunk of your construction plans, it now displays:
- **Cumulative cost estimate** after each chunk
- **Total items extracted** so far
- **Processing progress** (current chunk / total chunks)

Example output:
```
[Franklin OS] Processing chunk 1/8...
[Franklin OS] ├─ Chunk 1 complete
[Franklin OS] ├─ Items extracted: 4 agents × multiple items
[Franklin OS] ├─ Cumulative cost estimate: $305,750.00
[Franklin OS] └─ Total items so far: 11

[Franklin OS] Processing chunk 2/8...
[Franklin OS] ├─ Chunk 2 complete
[Franklin OS] ├─ Items extracted: 4 agents × multiple items
[Franklin OS] ├─ Cumulative cost estimate: $611,500.00
[Franklin OS] └─ Total items so far: 22
```

### 2. Division-Level Breakdown

After aggregation, the system now displays a detailed breakdown by CSI Division:

```
[Franklin OS] Cost breakdown by CSI Division:
[Franklin OS]   Division 03: $1,120,000.00 (2 items)
[Franklin OS]   Division 09: $234,000.00 (3 items)
[Franklin OS]   Division 22: $552,000.00 (3 items)
[Franklin OS]   Division 31: $540,000.00 (3 items)
```

### 3. Enhanced Stage Information

The processing results now include additional information in the `agent_processing` stage:
- `final_estimate`: Final cost estimate from all agents
- `total_items`: Total number of items extracted

Example:
```python
result = franklin.process_project(
    project_name="Office Building",
    file_path="plans.pdf"
)

# Access real-time data
agent_stage = result['stages']['agent_processing']
print(f"Final estimate: ${agent_stage['final_estimate']:,.2f}")
print(f"Total items: {agent_stage['total_items']}")
```

### 4. Real-Time API Endpoint

A new API endpoint `/api/estimate/current` allows you to query the current estimate while processing is in progress:

```bash
# Get current estimate
curl http://localhost:5000/api/estimate/current
```

Response:
```json
{
  "project_name": "Office Building",
  "processing_stage": "AI Agent Processing",
  "current_estimate": 1528750.00,
  "current_items": 55,
  "status": "processing",
  "stages": {...}
}
```

## Usage

### CLI Usage

Simply run the main application as usual. Real-time estimates are displayed automatically:

```bash
python main.py --project "My Project" --file plans.pdf
```

The verbose flag provides even more detail:

```bash
python main.py --project "My Project" --file plans.pdf --verbose
```

### Programmatic Usage

```python
from src.interfaces.franklin_os import FranklinOS

# Initialize Franklin OS
franklin = FranklinOS()

# Process a project - real-time estimates displayed automatically
result = franklin.process_project(
    project_name="Office Building",
    file_path="plans.pdf"
)

# Access final results
print(f"Total Cost: ${result['summary']['total_cost']:,.2f}")
print(f"Items: {result['summary']['item_count']}")

# Access agent-level estimates
agent_stage = result['stages']['agent_processing']
print(f"Agent Estimate: ${agent_stage['final_estimate']:,.2f}")
```

### Query Current Status

While a project is processing, you can query its current status:

```python
# Get current project status
status = franklin.get_project_status()

if status:
    print(f"Project: {status['name']}")
    print(f"Stage: {status['processing_stage']}")
    print(f"Current Estimate: ${status['current_estimate']:,.2f}")
    print(f"Items So Far: {status['current_items']}")
```

## API Endpoints

### GET /api/estimate/current

Get the current estimate of the project being processed.

**Response (200 OK):**
```json
{
  "project_name": "Office Building",
  "processing_stage": "AI Agent Processing",
  "current_estimate": 1528750.00,
  "current_items": 55,
  "status": "processing",
  "stages": {
    "ingestion": {...},
    "chunking": {...},
    "agent_processing": {...}
  }
}
```

**Response (404 Not Found):**
```json
{
  "message": "No project currently being processed"
}
```

### GET /api/status

Get overall system status (already existing, no changes).

## Benefits

1. **Transparency**: See costs accumulate in real-time rather than waiting for final results
2. **Progress Tracking**: Understand how far along the processing is
3. **Early Insights**: Get a sense of project scale early in processing
4. **Better UX**: More engaging user experience with visible progress
5. **Debugging**: Easier to identify issues if costs seem unexpected
6. **API Integration**: Monitor processing remotely via API calls

## Implementation Details

The real-time estimate tracking is implemented in the `FranklinOS` class:

1. **State Tracking**: New instance variables track current estimate and items:
   - `self.current_estimate`
   - `self.current_items`
   - `self.processing_stage`

2. **Progressive Calculation**: As each chunk is processed, costs are calculated and accumulated immediately

3. **Enhanced Output**: Clear, formatted output shows progress after each chunk

4. **API Support**: New endpoint provides programmatic access to current estimates

## Testing

Two test scripts are included:

1. **test_realtime_estimate.py**: Tests the core functionality
   ```bash
   python test_realtime_estimate.py
   ```

2. **test_api_realtime.py**: Tests the API endpoint
   ```bash
   # Start server first
   python api_server.py
   
   # In another terminal
   python test_api_realtime.py
   ```

## Example Output

Complete example of processing with real-time estimates:

```
======================================================================
BID-ZONE: Enterprise Construction Estimating Platform
======================================================================

[Franklin OS] Stage 1: Ingesting file: plans.pdf
[Franklin OS] Stage 2: Chunking documents
[Franklin OS] Created 8 chunks
[Franklin OS] Stage 3: Processing with AI agents
[Franklin OS] Processing chunk 1/8...
[Franklin OS] ├─ Chunk 1 complete
[Franklin OS] ├─ Items extracted: 4 agents × multiple items
[Franklin OS] ├─ Cumulative cost estimate: $305,750.00
[Franklin OS] └─ Total items so far: 11

[Franklin OS] Processing chunk 2/8...
[Franklin OS] ├─ Chunk 2 complete
[Franklin OS] ├─ Items extracted: 4 agents × multiple items
[Franklin OS] ├─ Cumulative cost estimate: $611,500.00
[Franklin OS] └─ Total items so far: 22

... (continues for all chunks) ...

[Franklin OS] Agents processed 32 results
[Franklin OS] Final estimate from agents: $2,446,000.00
[Franklin OS] Stage 4: Oracle verification
[Franklin OS] Verification: passed (confidence: 100.00%)
[Franklin OS] Stage 5: Aggregating results
[Franklin OS] Aggregated: $2,446,000.00 (88 items)
[Franklin OS] Cost breakdown by CSI Division:
[Franklin OS]   Division 03: $1,120,000.00 (2 items)
[Franklin OS]   Division 09: $234,000.00 (3 items)
[Franklin OS]   Division 22: $552,000.00 (3 items)
[Franklin OS]   Division 31: $540,000.00 (3 items)
[Franklin OS] Stage 6: Generating Excel estimate
[Franklin OS] Excel estimate created: outputs/plans_20251227_050302.xlsx
[Franklin OS] Project complete!

======================================================================
PROCESSING COMPLETE
======================================================================

Project: Office Building
Status: complete
Excel File: outputs/plans_20251227_050302.xlsx

Summary:
  Total Cost: $2,446,000.00
  Line Items: 88
  CSI Divisions: 4
  Verification Confidence: 100.0%
```

## Notes

- Real-time estimates are cumulative as each chunk completes
- Final estimates may differ slightly after aggregation and consolidation
- The feature adds minimal processing overhead
- All existing functionality remains unchanged
- Backwards compatible with existing code

## Related Files

- `src/interfaces/franklin_os.py` - Core implementation
- `api_server.py` - API endpoint implementation
- `test_realtime_estimate.py` - Functional tests
- `test_api_realtime.py` - API tests
