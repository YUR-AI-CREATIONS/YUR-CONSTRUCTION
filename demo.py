"""
BID-ZONE Platform Demonstration

This script demonstrates the complete workflow of the BID-ZONE
construction estimating platform.
"""

import sys
from pathlib import Path

print("\n" + "="*80)
print(" " * 20 + "BID-ZONE PLATFORM DEMONSTRATION")
print("="*80)

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  BID-ZONE: Enterprise Construction Estimating Platform                   ║
║                                                                           ║
║  A comprehensive AI-powered system that transforms construction plans    ║
║  into detailed, professionally formatted cost estimates.                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")

print("\n📋 PLATFORM CAPABILITIES\n")
print("  ✓ Multi-format file ingestion (ZIP, DWG, JPEG, PDF)")
print("  ✓ Intelligent document chunking")
print("  ✓ Specialized AI agents (4 domains)")
print("  ✓ Oracle verification layer")
print("  ✓ Nucleus aggregation engine")
print("  ✓ Professional Excel exports")
print("  ✓ CSI MasterFormat organization")
print("  ✓ Complete audit trail")

print("\n" + "-"*80)
print("\n🏗️  SYSTEM ARCHITECTURE\n")
print("""
    ┌─────────────────────────────────────┐
    │      Franklin OS Interface          │  ← Main orchestration layer
    └──────────────┬──────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────────┐
│  File   │  │Document │  │    Agent    │
│Ingestion│  │Chunking │  │  Framework  │
└────┬────┘  └────┬────┘  └─────┬───────┘
     │            │              │
     └────────────┼──────────────┘
                  │
                  ▼
         ┌────────────────┐
         │Oracle Verifier │  ← Quality assurance
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │    Nucleus     │  ← Data aggregation
         │  Aggregator    │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │Excel Exporter  │  ← Output generation
         └────────────────┘
""")

print("\n" + "-"*80)
print("\n🤖 SPECIALIZED AI AGENTS\n")

agents = [
    ("Structural Agent", "structural-001", "Concrete, Steel, Foundations", "03, 05"),
    ("MEP Agent", "mep-001", "Mechanical, Electrical, Plumbing", "21-28"),
    ("Finishes Agent", "finishes-001", "Drywall, Paint, Flooring", "09"),
    ("Site Work Agent", "sitework-001", "Earthwork, Paving, Utilities", "31-33")
]

for name, agent_id, specialty, divisions in agents:
    print(f"  {name}")
    print(f"    ID: {agent_id}")
    print(f"    Specialty: {specialty}")
    print(f"    CSI Divisions: {divisions}")
    print()

print("-"*80)
print("\n📊 PROCESSING WORKFLOW\n")

workflow_steps = [
    ("1", "File Upload", "User provides construction plans"),
    ("2", "Ingestion", "System extracts and validates files"),
    ("3", "Chunking", "Plans decomposed into processable units"),
    ("4", "Agent Processing", "Specialized agents extract cost data"),
    ("5", "Verification", "Oracle validates outputs & scores confidence"),
    ("6", "Aggregation", "Nucleus consolidates results by CSI division"),
    ("7", "Export", "Generate formatted Excel estimate"),
    ("8", "Delivery", "Return estimate with audit trail")
]

for step, name, description in workflow_steps:
    print(f"  Step {step}: {name}")
    print(f"          {description}")
    print()

print("-"*80)
print("\n📄 EXCEL OUTPUT STRUCTURE\n")

sheets = [
    ("Summary", "Project overview, cost by division, grand total"),
    ("Detailed Estimate", "Line items with quantities, units, prices"),
    ("CSI Divisions", "Reference guide to MasterFormat divisions"),
    ("Audit Trail", "Processing history and agent attribution")
]

for sheet_name, description in sheets:
    print(f"  Sheet: {sheet_name}")
    print(f"         {description}")
    print()

print("-"*80)
print("\n🎯 USAGE EXAMPLES\n")

print("  Basic usage:")
print("    $ python main.py --project 'Office Building' --file plans.pdf")
print()
print("  Process ZIP archive:")
print("    $ python main.py --project 'Warehouse' --file complete_set.zip")
print()
print("  With custom output:")
print("    $ python main.py --project 'Renovation' --file plans.pdf --output estimates")
print()
print("  Verbose mode:")
print("    $ python main.py --project 'Complex' --file plans.pdf --verbose")

print("\n" + "-"*80)
print("\n✅ SYSTEM STATUS\n")

# Run quick system check
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.interfaces.franklin_os import FranklinOS
    
    franklin = FranklinOS()
    status = franklin.get_system_status()
    
    print(f"  System Status: {status['system_status'].upper()}")
    print(f"  Available Agents: {len(status['agents_available'])}")
    print(f"  Projects Processed: {status['projects_processed']}")
    print()
    
    print("  Agent Details:")
    agent_stats = franklin.get_agent_statistics()
    for agent_type, stats in agent_stats.items():
        print(f"    • {agent_type}: {stats['specialty']}")
    
    print("\n  ✅ All systems operational and ready!")
    
except Exception as e:
    print(f"  ⚠️  Note: System check requires dependencies installed")
    print(f"     Run: pip install -r requirements.txt")

print("\n" + "-"*80)
print("\n📚 DOCUMENTATION\n")

docs = [
    ("README.md", "Overview and quick start guide"),
    ("INSTALLATION.md", "Detailed installation instructions"),
    ("USER_GUIDE.md", "Comprehensive user documentation"),
    ("ARCHITECTURE.md", "Technical architecture details")
]

for doc, description in docs:
    print(f"  {doc:20} - {description}")

print("\n" + "-"*80)
print("\n🚀 GET STARTED\n")

print("""
  1. Install dependencies:
     $ pip install -r requirements.txt

  2. Configure environment:
     $ cp .env.example .env
     $ # Edit .env with your API keys

  3. Run system tests:
     $ python test_system.py

  4. Process your first project:
     $ python main.py --project 'Test' --file your_plan.pdf

  5. Review the Excel output in the outputs/ folder
""")

print("-"*80)
print("\n📞 SUPPORT & RESOURCES\n")

print("  GitHub: https://github.com/YUR-AI-CREATIONS/BID-ZONE-")
print("  Issues: https://github.com/YUR-AI-CREATIONS/BID-ZONE-/issues")
print("  License: MIT")
print("  Author: YUR AI CREATIONS")

print("\n" + "="*80)
print(" " * 25 + "Ready to revolutionize construction estimating!")
print("="*80 + "\n")
