"""
Simple test script for BID-ZONE

This script tests the core functionality without requiring actual files.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.interfaces.franklin_os import FranklinOS
from src.core.chunking import DocumentChunk
from src.agents.agent_framework import AgentFramework
from src.core.oracle import OracleVerifier
from src.core.nucleus import NucleusAggregator
from src.utils.csi_divisions import get_all_divisions, get_division_name


def test_csi_divisions():
    """Test CSI division utilities"""
    print("Testing CSI Divisions...")
    
    divisions = get_all_divisions()
    assert len(divisions) > 0, "Should have CSI divisions"
    assert '03' in divisions, "Should have division 03 (Concrete)"
    
    name = get_division_name('03')
    assert name == 'Concrete', f"Division 03 should be 'Concrete', got '{name}'"
    
    print("  ✓ CSI divisions working correctly")


def test_agent_framework():
    """Test agent framework"""
    print("Testing Agent Framework...")
    
    framework = AgentFramework()
    assert len(framework.agents) > 0, "Should have agents"
    
    # Test agent retrieval
    structural_agent = framework.get_agent('structural')
    assert structural_agent is not None, "Should get structural agent"
    assert structural_agent.specialty == 'Structural Engineering'
    
    # Test processing with mock chunk
    mock_chunk = DocumentChunk(
        chunk_id='test_001',
        content={'type': 'test'},
        metadata={'test': True}
    )
    
    result = structural_agent.process_chunk(mock_chunk)
    assert result['agent_id'] == structural_agent.agent_id
    assert 'data' in result
    assert 'items' in result['data']
    
    print("  ✓ Agent framework working correctly")


def test_oracle_verifier():
    """Test Oracle verification"""
    print("Testing Oracle Verifier...")
    
    oracle = OracleVerifier()
    
    # Create a mock agent result
    mock_result = {
        'agent_id': 'test-001',
        'chunk_id': 'chunk_001',
        'data': {
            'csi_division': '03',
            'items': [
                {
                    'description': 'Concrete Foundation',
                    'quantity': 100,
                    'unit': 'CY',
                    'unit_price': 150.00,
                    'total': 15000.00
                }
            ]
        }
    }
    
    verification = oracle.verify_result(mock_result)
    assert 'verified' in verification
    assert 'confidence_score' in verification
    assert verification['confidence_score'] > 0
    
    print("  ✓ Oracle verifier working correctly")


def test_nucleus_aggregator():
    """Test Nucleus aggregation"""
    print("Testing Nucleus Aggregator...")
    
    nucleus = NucleusAggregator()
    
    # Create mock agent results
    mock_results = [
        {
            'agent_id': 'structural-001',
            'specialty': 'Structural',
            'data': {
                'csi_division': '03',
                'items': [
                    {
                        'description': 'Concrete',
                        'quantity': 100,
                        'unit': 'CY',
                        'unit_price': 150.00,
                        'total': 15000.00
                    }
                ],
                'scope': 'Foundation work'
            }
        },
        {
            'agent_id': 'mep-001',
            'specialty': 'MEP',
            'data': {
                'csi_division': '22',
                'items': [
                    {
                        'description': 'Plumbing',
                        'quantity': 1,
                        'unit': 'LS',
                        'unit_price': 10000.00,
                        'total': 10000.00
                    }
                ],
                'scope': 'Plumbing systems'
            }
        }
    ]
    
    aggregated = nucleus.aggregate(mock_results)
    assert 'divisions' in aggregated
    assert 'total_cost' in aggregated
    assert aggregated['total_cost'] == 25000.00
    assert len(aggregated['divisions']) == 2
    
    print("  ✓ Nucleus aggregator working correctly")


def test_franklin_os():
    """Test Franklin OS initialization"""
    print("Testing Franklin OS...")
    
    franklin = FranklinOS()
    
    # Test system status
    status = franklin.get_system_status()
    assert status['system_status'] == 'operational'
    assert 'agents_available' in status
    
    # Test agent statistics
    agent_stats = franklin.get_agent_statistics()
    assert len(agent_stats) > 0
    
    print("  ✓ Franklin OS working correctly")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("BID-ZONE SYSTEM TESTS")
    print("=" * 70 + "\n")
    
    try:
        test_csi_divisions()
        test_agent_framework()
        test_oracle_verifier()
        test_nucleus_aggregator()
        test_franklin_os()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED ✓")
        print("=" * 70 + "\n")
        
        print("The BID-ZONE platform is ready to use!")
        print("\nNext steps:")
        print("  1. Set up your .env file with API keys")
        print("  2. Run: python main.py --project 'Test' --file your_plan.pdf")
        print()
        
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}\n")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
