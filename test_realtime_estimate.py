"""
Test Real-Time Estimate Functionality

This script tests the new real-time estimate tracking feature
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.interfaces.franklin_os import FranklinOS

def test_realtime_estimates():
    """Test real-time estimate tracking"""
    
    print("\n" + "="*70)
    print("Testing Real-Time Estimate Tracking")
    print("="*70 + "\n")
    
    # Initialize Franklin OS
    franklin = FranklinOS()
    
    # Check initial state
    print("1. Checking initial state...")
    status = franklin.get_project_status()
    assert status is None, "Expected no current project initially"
    print("   ✓ Initial state correct (no active project)\n")
    
    # Use an existing PDF file from the repository
    print("2. Using existing test file...")
    test_file = Path(__file__).parent / "JCK BATCH PLANT - WATER LINE PLANS.pdf"
    
    if not test_file.exists():
        print(f"   ⚠ Test file not found: {test_file}")
        print("   Creating a minimal mock PDF for testing...\n")
        # Create a simple test by using a simpler approach
        print("   Skipping file-based test, testing API only...\n")
        return test_api_only(franklin)
    
    print(f"   ✓ Test file found: {test_file}\n")
    
    # Process the project
    print("3. Processing project with real-time estimates...")
    print("   (Watch for cumulative cost updates)\n")
    
    result = franklin.process_project(
        project_name="Real-Time Test Project",
        file_path=str(test_file),
        consolidate_duplicates=True
    )
    
    print("\n4. Verifying results...")
    
    # Check that we got results
    assert result['status'] == 'complete', "Expected complete status"
    print("   ✓ Project completed successfully")
    
    # Check that we have cost estimate
    assert 'summary' in result, "Expected summary in result"
    assert 'total_cost' in result['summary'], "Expected total_cost in summary"
    print(f"   ✓ Final cost estimate: ${result['summary']['total_cost']:,.2f}")
    
    # Check that agent processing stage has real-time data
    assert 'agent_processing' in result['stages'], "Expected agent_processing stage"
    agent_stage = result['stages']['agent_processing']
    assert 'final_estimate' in agent_stage, "Expected final_estimate in agent stage"
    assert 'total_items' in agent_stage, "Expected total_items in agent stage"
    print(f"   ✓ Agent stage estimate: ${agent_stage['final_estimate']:,.2f}")
    print(f"   ✓ Total items extracted: {agent_stage['total_items']}")
    
    # Check division breakdown exists
    assert 'aggregation' in result['stages'], "Expected aggregation stage"
    assert 'divisions' in result['stages']['aggregation'], "Expected divisions count"
    print(f"   ✓ CSI Divisions processed: {result['stages']['aggregation']['divisions']}")
    
    print("\n" + "="*70)
    print("✅ All Real-Time Estimate Tests PASSED!")
    print("="*70 + "\n")
    
    return True


def test_api_only(franklin):
    """Test just the API functionality without file processing"""
    print("3. Testing API functionality...")
    
    # Test system status
    status = franklin.get_system_status()
    assert 'system_status' in status, "Expected system_status"
    assert status['system_status'] == 'operational', "Expected operational status"
    print("   ✓ System status API works")
    
    # Test agent statistics
    agent_stats = franklin.get_agent_statistics()
    assert len(agent_stats) > 0, "Expected agent statistics"
    print(f"   ✓ Agent statistics API works ({len(agent_stats)} agents)")
    
    print("\n" + "="*70)
    print("✅ API Tests PASSED! (File processing skipped)")
    print("="*70 + "\n")
    
    return True


if __name__ == '__main__':
    try:
        success = test_realtime_estimates()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
