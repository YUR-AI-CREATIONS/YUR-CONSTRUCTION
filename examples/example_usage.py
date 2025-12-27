"""
Example: Using BID-ZONE Platform

This example demonstrates how to use the BID-ZONE platform
to process construction plans and generate estimates.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.interfaces.franklin_os import FranklinOS
from src.core.ingestion import FileIngestionSystem
from src.core.chunking import DocumentChunker
from src.agents.agent_framework import AgentFramework
import json


def example_basic_usage():
    """Basic usage example"""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)
    print()
    
    # Initialize Franklin OS
    franklin = FranklinOS(config={
        'upload_folder': 'examples/uploads',
        'output_folder': 'examples/outputs'
    })
    
    # Show system status
    status = franklin.get_system_status()
    print("System Status:")
    print(json.dumps(status, indent=2))
    print()
    
    # Get agent statistics
    agent_stats = franklin.get_agent_statistics()
    print("Available Agents:")
    for agent_type, stats in agent_stats.items():
        print(f"  - {agent_type}: {stats['specialty']}")
    print()


def example_file_ingestion():
    """Example of file ingestion"""
    print("=" * 70)
    print("Example 2: File Ingestion")
    print("=" * 70)
    print()
    
    ingestion = FileIngestionSystem()
    
    print("Supported formats:")
    print(f"  {', '.join(ingestion.supported_formats)}")
    print()
    
    print("File ingestion handles:")
    print("  - ZIP archives (extracts and processes contents)")
    print("  - PDF documents (page-by-page)")
    print("  - DWG files (layer extraction)")
    print("  - Images (JPEG, PNG)")
    print()


def example_agent_framework():
    """Example of agent framework"""
    print("=" * 70)
    print("Example 3: AI Agent Framework")
    print("=" * 70)
    print()
    
    framework = AgentFramework()
    
    print("Specialized Agents:")
    for agent_type, agent in framework.agents.items():
        print(f"\n{agent_type.upper()}")
        print(f"  Agent ID: {agent.agent_id}")
        print(f"  Specialty: {agent.specialty}")
    print()


def example_document_chunking():
    """Example of document chunking"""
    print("=" * 70)
    print("Example 4: Document Chunking")
    print("=" * 70)
    print()
    
    chunker = DocumentChunker()
    
    # Simulate a file info structure
    file_info = {
        'file_type': '.pdf',
        'original_file': 'example_plan.pdf',
        'extracted_files': [
            {
                'path': 'example_plan.pdf',
                'type': '.pdf',
                'num_pages': 25,
                'size': 5242880
            }
        ]
    }
    
    chunks = chunker.chunk_document(file_info)
    
    print(f"Chunking Strategy for PDF:")
    print(f"  - Input: {file_info['extracted_files'][0]['num_pages']} page PDF")
    print(f"  - Output: {len(chunks)} chunks (1 per page)")
    print(f"  - Each chunk represents a logical unit for AI processing")
    print()


def example_csi_divisions():
    """Example of CSI divisions"""
    print("=" * 70)
    print("Example 5: CSI Division Organization")
    print("=" * 70)
    print()
    
    from src.utils.csi_divisions import get_all_divisions
    
    divisions = get_all_divisions()
    
    print("Sample CSI MasterFormat Divisions:")
    sample_divisions = ['03', '05', '09', '22', '26', '31']
    
    for div in sample_divisions:
        info = divisions[div]
        print(f"\nDivision {div}: {info['name']}")
        print(f"  {info['description']}")
    print()


def main():
    """Run all examples"""
    print("\n")
    print("*" * 70)
    print("BID-ZONE PLATFORM EXAMPLES")
    print("*" * 70)
    print("\n")
    
    example_basic_usage()
    example_file_ingestion()
    example_agent_framework()
    example_document_chunking()
    example_csi_divisions()
    
    print("=" * 70)
    print("Examples Complete")
    print("=" * 70)
    print()
    print("To process a real project, use:")
    print("  python main.py --project 'My Project' --file plans.pdf")
    print()


if __name__ == '__main__':
    main()
