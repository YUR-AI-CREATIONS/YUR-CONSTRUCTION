# BID-ZONE Architecture

## System Overview

BID-ZONE is a multi-layered enterprise construction estimating platform that processes construction documentation through specialized AI agents to produce comprehensive cost estimates.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Franklin OS Interface                     │
│                   (Main Orchestration Layer)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ File         │ │  Document    │ │    Agent     │
│ Ingestion    │ │  Chunking    │ │  Framework   │
│              │ │              │ │              │
│ • ZIP        │ │ • PDF Pages  │ │ • Structural │
│ • DWG        │ │ • Layers     │ │ • MEP        │
│ • JPEG       │ │ • Images     │ │ • Finishes   │
│ • PDF        │ │ • Archives   │ │ • Site Work  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Oracle Verifier     │
            │   (QA Layer)          │
            │                       │
            │ • Validation          │
            │ • Confidence Scoring  │
            │ • Error Detection     │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Nucleus Aggregator   │
            │  (Data Consolidation) │
            │                       │
            │ • CSI Organization    │
            │ • Deduplication       │
            │ • Cost Summation      │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Excel Exporter      │
            │   (Output Generation) │
            │                       │
            │ • Formatted Sheets    │
            │ • Audit Trail         │
            │ • CSI Reference       │
            └───────────────────────┘
```

## Component Details

### 1. Franklin OS Interface

**Purpose:** Main orchestration and workflow management

**Responsibilities:**
- Coordinate all system components
- Manage processing pipeline
- Track project state
- Provide API interface
- Handle errors and logging

**Key Methods:**
- `process_project()` - Main workflow orchestrator
- `get_project_status()` - Status monitoring
- `get_system_status()` - Health checks

**Design Pattern:** Facade Pattern

### 2. File Ingestion System

**Purpose:** Handle multi-format file input

**Supported Formats:**
- ZIP: Extract and process contents recursively
- PDF: Extract pages and metadata
- DWG: Parse CAD layers and entities
- JPEG/PNG: Process images

**Key Features:**
- Format detection
- Automatic extraction
- Metadata collection
- Error handling

**Implementation:**
- `FileIngestionSystem` class
- Format-specific processors
- Extensible architecture

### 3. Document Chunking

**Purpose:** Decompose large documents into processable units

**Chunking Strategies:**
- **PDF:** One chunk per page
- **DWG:** One chunk per layer (or entire file)
- **Images:** One chunk per image
- **ZIP:** Recursive chunking of contents

**Chunk Structure:**
```python
DocumentChunk {
    chunk_id: str        # Unique identifier
    content: dict        # Chunk data
    metadata: dict       # Source information
    processed: bool      # Processing status
    results: dict        # Agent results
}
```

### 4. Agent Framework

**Purpose:** Specialized AI agents for data extraction

**Agent Architecture:**

```python
BaseAgent
├── agent_id: str
├── specialty: str
├── processing_history: list
└── methods:
    ├── process_chunk()
    └── _extract_data()
```

**Specialized Agents:**

| Agent | CSI Focus | Extracts |
|-------|-----------|----------|
| Structural | 03, 05 | Concrete, Steel |
| MEP | 21-28 | Mechanical, Electrical, Plumbing |
| Finishes | 09 | Drywall, Paint, Flooring |
| Site Work | 31-33 | Earthwork, Paving, Utilities |

**Agent Output Format:**
```python
{
    'agent_id': str,
    'specialty': str,
    'chunk_id': str,
    'timestamp': str,
    'status': str,
    'data': {
        'csi_division': str,
        'items': [
            {
                'description': str,
                'quantity': float,
                'unit': str,
                'unit_price': float,
                'total': float
            }
        ],
        'scope': str,
        'notes': str
    }
}
```

### 5. Oracle Verification Layer

**Purpose:** Quality assurance and validation

**Verification Checks:**
1. **Completeness**
   - Required fields present
   - Non-null values
   - Valid data types

2. **Calculations**
   - Quantity × Unit Price = Total
   - 1% tolerance for rounding

3. **Confidence Scoring**
   - Field completeness: 20%
   - Value reasonability: 60%
   - Calculation accuracy: 20%

**Verification Result:**
```python
{
    'verified': bool,
    'confidence_score': float,
    'issues': [str],
    'warnings': [str]
}
```

### 6. Nucleus Aggregator

**Purpose:** Consolidate and organize results

**Aggregation Process:**
1. Group by CSI division
2. Track agent attribution
3. Sum costs and counts
4. Consolidate duplicates (optional)
5. Generate statistics

**Consolidation Logic:**
- Group items by description
- Sum quantities
- Average unit prices (weighted)
- Preserve agent attribution

**Output Structure:**
```python
{
    'divisions': {
        '03': {
            'items': [],
            'agents': [],
            'scope_notes': [],
            'subtotal': float,
            'item_count': int
        }
    },
    'total_cost': float,
    'item_count': int
}
```

### 7. Excel Export System

**Purpose:** Generate formatted estimate documents

**Excel Structure:**

**Sheet 1: Summary**
- Project header
- Cost by division
- Grand total

**Sheet 2: Detailed Estimate**
- Line items organized by division
- Columns: Item #, CSI Div, Description, Scope, Qty, Unit, Unit Price, Total, Agent
- Division subtotals

**Sheet 3: CSI Divisions**
- Reference guide
- All 30+ divisions
- Descriptions

**Sheet 4: Audit Trail**
- Processing timeline
- Agent assignments
- Verification status
- Metadata

**Styling:**
- Color-coded headers
- Professional formatting
- Calculated totals
- Conditional formatting

## Data Flow

### Processing Pipeline

```
Input File
    ↓
Ingestion (extract/parse)
    ↓
Chunking (decompose)
    ↓
Agent Processing (extract data)
    ↓
Oracle Verification (validate)
    ↓
Nucleus Aggregation (consolidate)
    ↓
Excel Export (format)
    ↓
Output File
```

### State Management

**Project State:**
```python
{
    'name': str,
    'status': str,        # processing, complete, error
    'start_time': str,
    'end_time': str,
    'stages': {
        'ingestion': {...},
        'chunking': {...},
        'agent_processing': {...},
        'verification': {...},
        'aggregation': {...},
        'export': {...}
    },
    'excel_file': str,
    'summary': {...}
}
```

## Design Patterns

### 1. Facade Pattern (Franklin OS)
Provides simplified interface to complex subsystems

### 2. Strategy Pattern (Agent Framework)
Different agents implement same interface with specialized strategies

### 3. Pipeline Pattern (Processing Flow)
Sequential stages process data through pipeline

### 4. Factory Pattern (Chunking)
Different chunkers created based on file type

## Extensibility

### Adding New Agents

```python
class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__('custom-001', 'Custom Specialty')
    
    def _extract_data(self, chunk):
        # Custom extraction logic
        return {
            'csi_division': 'XX',
            'items': [...],
            'scope': 'Description',
            'notes': 'Details'
        }

# Register in AgentFramework
framework.agents['custom'] = CustomAgent()
```

### Adding File Formats

```python
def _process_new_format(self, file_path):
    # Custom file processing
    return [{
        'path': str(file_path),
        'type': '.ext',
        'data': {...}
    }]

# Add to supported formats
self.supported_formats.append('.ext')
```

### Custom Verification Rules

```python
def custom_validator(item):
    # Custom validation logic
    if not meets_criteria(item):
        return ["Custom validation error"]
    return []

# Add to Oracle
oracle.add_validator(custom_validator)
```

## Performance Considerations

### Scalability

**File Size:**
- Chunks processed independently
- Parallel agent processing possible
- Memory-efficient streaming

**Processing Time:**
- Typical: 5-30 seconds per page
- Depends on:
  - File complexity
  - Number of agents
  - AI provider latency

### Optimization Opportunities

1. **Parallel Processing**
   - Process chunks concurrently
   - Multiple agents simultaneously
   - Async I/O for files

2. **Caching**
   - Cache parsed documents
   - Store intermediate results
   - Reuse agent responses

3. **Batch Processing**
   - Group similar chunks
   - Batch API calls
   - Reduce overhead

## Security Considerations

### Data Privacy
- Files processed in memory
- Temporary files cleaned up
- No persistent storage of plans
- API keys in environment variables

### Input Validation
- File type verification
- Size limits
- Format validation
- Malware scanning (recommended)

### Output Protection
- Excel files password-protectable
- Audit trail for accountability
- Access control on outputs

## Error Handling

### Error Categories

1. **Input Errors**
   - Invalid file format
   - File not found
   - Corrupt files

2. **Processing Errors**
   - Agent failures
   - Verification failures
   - Calculation errors

3. **Output Errors**
   - File write failures
   - Format errors
   - Disk space issues

### Recovery Strategies

- Graceful degradation
- Partial result saving
- Error logging
- User notification

## Testing Strategy

### Unit Tests
- Individual component testing
- Mock dependencies
- Edge case coverage

### Integration Tests
- Pipeline testing
- Component interaction
- End-to-end workflows

### System Tests
- Full workflow validation
- Real file processing
- Output verification

## Future Enhancements

### Planned Features
1. Web interface
2. Real-time progress tracking
3. Custom agent training
4. Integration APIs
5. Batch processing
6. Cloud deployment
7. Mobile app
8. Collaboration features

### Technology Considerations
- Microservices architecture
- Container orchestration
- Database integration
- Message queues
- API gateway

## Maintenance

### Monitoring
- Processing times
- Success rates
- Error frequencies
- System health

### Updates
- Agent improvements
- Format support
- Library updates
- Security patches

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-26  
**Maintainer:** YUR AI CREATIONS
