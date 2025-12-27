"""
Oracle Verification Layer

Verifies outputs from AI agents for accuracy and completeness
"""

from typing import Dict, Any, List
from datetime import datetime


class OracleVerifier:
    """
    Verification layer that validates agent outputs
    """
    
    def __init__(self):
        self.verification_history = []
        
    def verify_result(self, agent_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a single agent result
        
        Args:
            agent_result: Result from an AI agent
            
        Returns:
            Verification result with status and issues
        """
        verification = {
            'timestamp': datetime.utcnow().isoformat(),
            'agent_id': agent_result.get('agent_id'),
            'chunk_id': agent_result.get('chunk_id'),
            'verified': True,
            'issues': [],
            'warnings': [],
            'confidence_score': 0.0
        }
        
        data = agent_result.get('data', {})
        items = data.get('items', [])
        
        # Check for required fields
        if not items:
            verification['issues'].append("No items extracted")
            verification['verified'] = False
        
        # Validate each item
        confidence_scores = []
        for idx, item in enumerate(items):
            item_issues = self._validate_item(item, idx)
            verification['issues'].extend(item_issues)
            
            # Calculate confidence for this item
            confidence = self._calculate_item_confidence(item)
            confidence_scores.append(confidence)
        
        # Overall confidence
        if confidence_scores:
            verification['confidence_score'] = sum(confidence_scores) / len(confidence_scores)
        
        # Check CSI division
        csi_division = data.get('csi_division')
        if not csi_division:
            verification['warnings'].append("No CSI division specified")
        
        # Mark as not verified if there are critical issues
        if len(verification['issues']) > 0:
            verification['verified'] = False
        
        # Store verification
        self.verification_history.append(verification)
        
        return verification
    
    def _validate_item(self, item: Dict[str, Any], index: int) -> List[str]:
        """Validate a single cost item"""
        issues = []
        
        # Required fields
        required_fields = ['description', 'quantity', 'unit', 'unit_price', 'total']
        for field in required_fields:
            if field not in item or item[field] is None:
                issues.append(f"Item {index + 1}: Missing required field '{field}'")
        
        # Validate numeric fields
        if 'quantity' in item and not isinstance(item['quantity'], (int, float)):
            issues.append(f"Item {index + 1}: Invalid quantity type")
        
        if 'unit_price' in item and not isinstance(item['unit_price'], (int, float)):
            issues.append(f"Item {index + 1}: Invalid unit_price type")
        
        if 'total' in item and not isinstance(item['total'], (int, float)):
            issues.append(f"Item {index + 1}: Invalid total type")
        
        # Validate calculations
        if all(k in item for k in ['quantity', 'unit_price', 'total']):
            expected_total = item['quantity'] * item['unit_price']
            actual_total = item['total']
            
            # Allow 1% tolerance for rounding (or 0.01 minimum for zero values)
            tolerance = max(abs(expected_total * 0.01), 0.01)
            if abs(expected_total - actual_total) > tolerance:
                issues.append(
                    f"Item {index + 1}: Total calculation mismatch "
                    f"(expected {expected_total:.2f}, got {actual_total:.2f})"
                )
        
        return issues
    
    def _calculate_item_confidence(self, item: Dict[str, Any]) -> float:
        """Calculate confidence score for an item"""
        score = 1.0
        
        # Reduce confidence for missing optional fields
        if 'description' not in item or not item['description']:
            score -= 0.2
        
        # Check if values are reasonable
        if 'quantity' in item and item['quantity'] <= 0:
            score -= 0.3
        
        if 'unit_price' in item and item['unit_price'] <= 0:
            score -= 0.3
        
        if 'total' in item and item['total'] <= 0:
            score -= 0.3
        
        return max(0.0, score)
    
    def verify_batch(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verify a batch of agent results
        
        Args:
            agent_results: List of results from AI agents
            
        Returns:
            Batch verification summary
        """
        verifications = []
        total_issues = 0
        total_warnings = 0
        verified_count = 0
        
        for result in agent_results:
            verification = self.verify_result(result)
            verifications.append(verification)
            
            total_issues += len(verification['issues'])
            total_warnings += len(verification['warnings'])
            if verification['verified']:
                verified_count += 1
        
        # Calculate overall confidence
        confidence_scores = [v['confidence_score'] for v in verifications]
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_results': len(agent_results),
            'verified_count': verified_count,
            'failed_count': len(agent_results) - verified_count,
            'total_issues': total_issues,
            'total_warnings': total_warnings,
            'average_confidence': avg_confidence,
            'verifications': verifications,
            'status': 'passed' if verified_count == len(agent_results) else 'failed'
        }
        
        return summary
    
    def get_verification_report(self) -> Dict[str, Any]:
        """Get summary report of all verifications"""
        return {
            'total_verifications': len(self.verification_history),
            'history': self.verification_history
        }
