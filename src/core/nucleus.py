"""
Nucleus Aggregation Engine

Aggregates and combines results from multiple AI agents
"""

from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict


class NucleusAggregator:
    """
    Aggregates results from multiple specialized agents
    """
    
    def __init__(self):
        self.aggregation_history = []
        
    def aggregate(self, agent_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregate results from multiple agents
        
        Args:
            agent_results: List of results from AI agents
            
        Returns:
            Aggregated results organized by CSI division
        """
        aggregation = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_results': len(agent_results),
            'divisions': {},
            'agents_used': set(),
            'total_cost': 0.0,
            'item_count': 0
        }
        
        # Group by CSI division
        division_data = defaultdict(lambda: {
            'items': [],
            'agents': set(),
            'scope_notes': [],
            'subtotal': 0.0
        })
        
        for result in agent_results:
            agent_id = result.get('agent_id')
            specialty = result.get('specialty')
            data = result.get('data', {})
            
            csi_division = data.get('csi_division', '99')
            items = data.get('items', [])
            scope = data.get('scope', '')
            notes = data.get('notes', '')
            
            # Track agent
            aggregation['agents_used'].add(agent_id)
            division_data[csi_division]['agents'].add(agent_id)
            
            # Add items
            for item in items:
                division_data[csi_division]['items'].append({
                    **item,
                    'agent_id': agent_id,
                    'specialty': specialty
                })
                division_data[csi_division]['subtotal'] += item.get('total', 0.0)
                aggregation['total_cost'] += item.get('total', 0.0)
                aggregation['item_count'] += 1
            
            # Add scope notes
            if scope:
                division_data[csi_division]['scope_notes'].append(scope)
            if notes:
                division_data[csi_division]['scope_notes'].append(notes)
        
        # Convert to serializable format
        for division, data in division_data.items():
            aggregation['divisions'][division] = {
                'items': data['items'],
                'agents': list(data['agents']),
                'scope_notes': list(set(data['scope_notes'])),  # Remove duplicates
                'subtotal': data['subtotal'],
                'item_count': len(data['items'])
            }
        
        aggregation['agents_used'] = list(aggregation['agents_used'])
        
        # Store aggregation
        self.aggregation_history.append({
            'timestamp': aggregation['timestamp'],
            'divisions_count': len(aggregation['divisions']),
            'total_cost': aggregation['total_cost'],
            'item_count': aggregation['item_count']
        })
        
        return aggregation
    
    def consolidate_duplicates(self, aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Consolidate duplicate items in aggregated data
        
        Args:
            aggregated_data: Aggregated results from aggregate()
            
        Returns:
            Consolidated data with duplicates merged
        """
        consolidated = {
            **aggregated_data,
            'consolidation_applied': True,
            'duplicates_merged': 0
        }
        
        # Process each division
        for division, data in consolidated['divisions'].items():
            items = data['items']
            
            # Group by description
            item_groups = defaultdict(list)
            for item in items:
                key = item.get('description', '').strip().lower()
                item_groups[key].append(item)
            
            # Consolidate items with same description
            consolidated_items = []
            for description_key, item_list in item_groups.items():
                if len(item_list) == 1:
                    consolidated_items.append(item_list[0])
                else:
                    # Merge multiple items
                    merged_item = self._merge_items(item_list)
                    consolidated_items.append(merged_item)
                    consolidated['duplicates_merged'] += len(item_list) - 1
            
            data['items'] = consolidated_items
            data['item_count'] = len(consolidated_items)
        
        return consolidated
    
    def _merge_items(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple similar items"""
        if not items:
            return {}
        
        # Use first item as base
        merged = items[0].copy()
        
        # Sum quantities and totals
        total_quantity = sum(item.get('quantity', 0) for item in items)
        total_cost = sum(item.get('total', 0) for item in items)
        
        # Average unit price (weighted by quantity)
        total_qty_price = sum(
            item.get('quantity', 0) * item.get('unit_price', 0) 
            for item in items
        )
        if total_quantity > 0:
            avg_unit_price = total_qty_price / total_quantity
        else:
            # If no quantity, log warning and use simple average of unit prices
            avg_unit_price = sum(item.get('unit_price', 0) for item in items) / len(items) if items else 0
        
        # Combine agent IDs
        agent_ids = [item.get('agent_id', '') for item in items]
        
        merged.update({
            'quantity': total_quantity,
            'unit_price': avg_unit_price,
            'total': total_cost,
            'agent_id': ', '.join(set(agent_ids)),
            'merged_from': len(items)
        })
        
        return merged
    
    def get_summary_statistics(self, aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary statistics from aggregated data
        
        Args:
            aggregated_data: Aggregated results
            
        Returns:
            Summary statistics
        """
        stats = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_cost': aggregated_data.get('total_cost', 0.0),
            'item_count': aggregated_data.get('item_count', 0),
            'division_count': len(aggregated_data.get('divisions', {})),
            'agents_used': len(aggregated_data.get('agents_used', [])),
            'cost_by_division': {},
            'items_by_division': {}
        }
        
        for division, data in aggregated_data.get('divisions', {}).items():
            stats['cost_by_division'][division] = data.get('subtotal', 0.0)
            stats['items_by_division'][division] = data.get('item_count', 0)
        
        return stats
    
    def get_aggregation_history(self) -> List[Dict[str, Any]]:
        """Get history of all aggregations"""
        return self.aggregation_history
