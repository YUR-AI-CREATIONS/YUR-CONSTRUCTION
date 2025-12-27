"""
BID-ZONE Main Application

Command-line interface for the construction estimating platform
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.interfaces.franklin_os import FranklinOS


def main():
    """Main entry point for BID-ZONE CLI"""
    parser = argparse.ArgumentParser(
        description='BID-ZONE: Enterprise Construction Estimating Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Process a single PDF:
    python main.py --project "Office Building" --file plans.pdf
  
  Process a ZIP archive:
    python main.py --project "Warehouse" --file complete_plans.zip
  
  Process without consolidating duplicates:
    python main.py --project "Renovation" --file plans.pdf --no-consolidate
        """
    )
    
    parser.add_argument(
        '--project',
        type=str,
        required=True,
        help='Name of the construction project'
    )
    
    parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to construction plan file (PDF, ZIP, DWG, or image)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='outputs',
        help='Output directory for Excel estimates (default: outputs)'
    )
    
    parser.add_argument(
        '--no-consolidate',
        action='store_true',
        help='Do not consolidate duplicate items'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {args.file}")
        return 1
    
    # Initialize Franklin OS
    print("=" * 70)
    print("BID-ZONE: Enterprise Construction Estimating Platform")
    print("=" * 70)
    print()
    
    config = {
        'output_folder': args.output,
        'upload_folder': 'uploads'
    }
    
    franklin = FranklinOS(config=config)
    
    # Process project
    try:
        result = franklin.process_project(
            project_name=args.project,
            file_path=str(file_path),
            consolidate_duplicates=not args.no_consolidate
        )
        
        print()
        print("=" * 70)
        print("PROCESSING COMPLETE")
        print("=" * 70)
        print()
        print(f"Project: {result['name']}")
        print(f"Status: {result['status']}")
        print(f"Excel File: {result['excel_file']}")
        print()
        print("Summary:")
        print(f"  Total Cost: ${result['summary']['total_cost']:,.2f}")
        print(f"  Line Items: {result['summary']['item_count']}")
        print(f"  CSI Divisions: {result['summary']['divisions']}")
        print(f"  Verification Confidence: {result['summary']['verification_confidence']:.1%}")
        print()
        
        if args.verbose:
            print("Stage Details:")
            for stage_name, stage_info in result['stages'].items():
                print(f"  {stage_name}: {stage_info}")
            print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("ERROR")
        print("=" * 70)
        print(f"An error occurred: {str(e)}")
        
        if args.verbose:
            import traceback
            print()
            print("Traceback:")
            traceback.print_exc()
        
        return 1


if __name__ == '__main__':
    sys.exit(main())
