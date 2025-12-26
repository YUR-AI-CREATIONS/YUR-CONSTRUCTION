"""
Franklin OS Interface

Primary interface for the BID-ZONE estimating platform
"""

from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json

from ..core.ingestion import FileIngestionSystem
from ..core.chunking import DocumentChunker
from ..agents.agent_framework import AgentFramework
from ..core.oracle import OracleVerifier
from ..core.nucleus import NucleusAggregator
from ..core.excel_export import ExcelExporter


class FranklinOS:
    """
    Main interface for the BID-ZONE construction estimating platform
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Franklin OS
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize components
        self.ingestion = FileIngestionSystem(
            upload_folder=self.config.get('upload_folder', 'uploads'),
            output_folder=self.config.get('output_folder', 'outputs')
        )
        self.chunker = DocumentChunker()
        self.agent_framework = AgentFramework()
        self.oracle = OracleVerifier()
        self.nucleus = NucleusAggregator()
        self.exporter = ExcelExporter(
            output_folder=self.config.get('output_folder', 'outputs')
        )
        
        # Processing state
        self.current_project = None
        self.processing_history = []
        
    def process_project(self, 
                       project_name: str,
                       file_path: str,
                       consolidate_duplicates: bool = True) -> Dict[str, Any]:
        """
        Process a complete construction estimating project
        
        Args:
            project_name: Name of the project
            file_path: Path to the construction plan file(s)
            consolidate_duplicates: Whether to consolidate duplicate items
            
        Returns:
            Processing results with Excel file path
        """
        start_time = datetime.utcnow()
        
        # Create project tracking
        project = {
            'name': project_name,
            'start_time': start_time.isoformat(),
            'status': 'processing',
            'stages': {}
        }
        self.current_project = project
        
        try:
            # Stage 1: File Ingestion
            print(f"[Franklin OS] Stage 1: Ingesting file: {file_path}")
            file_info = self.ingestion.ingest_file(file_path)
            project['stages']['ingestion'] = {
                'status': 'complete',
                'file_type': file_info['file_type'],
                'extracted_files': len(file_info['extracted_files'])
            }
            
            # Stage 2: Document Chunking
            print(f"[Franklin OS] Stage 2: Chunking documents")
            chunks = self.chunker.chunk_document(file_info)
            project['stages']['chunking'] = {
                'status': 'complete',
                'chunks_created': len(chunks)
            }
            print(f"[Franklin OS] Created {len(chunks)} chunks")
            
            # Stage 3: AI Agent Processing
            print(f"[Franklin OS] Stage 3: Processing with AI agents")
            agent_results = self.agent_framework.process_chunks(chunks)
            project['stages']['agent_processing'] = {
                'status': 'complete',
                'results_count': len(agent_results),
                'agents_used': list(self.agent_framework.agents.keys())
            }
            print(f"[Franklin OS] Agents processed {len(agent_results)} results")
            
            # Stage 4: Oracle Verification
            print(f"[Franklin OS] Stage 4: Oracle verification")
            verification = self.oracle.verify_batch(agent_results)
            project['stages']['verification'] = {
                'status': verification['status'],
                'verified_count': verification['verified_count'],
                'failed_count': verification['failed_count'],
                'confidence': verification['average_confidence']
            }
            print(f"[Franklin OS] Verification: {verification['status']} "
                  f"(confidence: {verification['average_confidence']:.2%})")
            
            # Stage 5: Nucleus Aggregation
            print(f"[Franklin OS] Stage 5: Aggregating results")
            aggregated = self.nucleus.aggregate(agent_results)
            
            if consolidate_duplicates:
                aggregated = self.nucleus.consolidate_duplicates(aggregated)
            
            project['stages']['aggregation'] = {
                'status': 'complete',
                'total_cost': aggregated['total_cost'],
                'item_count': aggregated['item_count'],
                'divisions': len(aggregated['divisions'])
            }
            print(f"[Franklin OS] Aggregated: ${aggregated['total_cost']:,.2f} "
                  f"({aggregated['item_count']} items)")
            
            # Stage 6: Excel Export
            print(f"[Franklin OS] Stage 6: Generating Excel estimate")
            metadata = {
                'project_name': project_name,
                'processing_time': (datetime.utcnow() - start_time).total_seconds(),
                'verification_status': verification['status'],
                'confidence_score': verification['average_confidence']
            }
            
            excel_path = self.exporter.create_estimate(
                project_name=project_name,
                agent_results=agent_results,
                metadata=metadata
            )
            
            project['stages']['export'] = {
                'status': 'complete',
                'excel_file': excel_path
            }
            print(f"[Franklin OS] Excel estimate created: {excel_path}")
            
            # Complete project
            project['status'] = 'complete'
            project['end_time'] = datetime.utcnow().isoformat()
            project['excel_file'] = excel_path
            project['summary'] = {
                'total_cost': aggregated['total_cost'],
                'item_count': aggregated['item_count'],
                'divisions': len(aggregated['divisions']),
                'verification_confidence': verification['average_confidence']
            }
            
            self.processing_history.append(project)
            
            print(f"[Franklin OS] Project complete!")
            
            return project
            
        except Exception as e:
            project['status'] = 'error'
            project['error'] = str(e)
            project['end_time'] = datetime.utcnow().isoformat()
            
            print(f"[Franklin OS] Error: {str(e)}")
            raise
    
    def get_project_status(self) -> Optional[Dict[str, Any]]:
        """Get current project status"""
        return self.current_project
    
    def get_processing_history(self) -> list:
        """Get history of all processed projects"""
        return self.processing_history
    
    def get_agent_statistics(self) -> Dict[str, Any]:
        """Get statistics about agent processing"""
        return self.agent_framework.get_agent_stats()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'current_project': self.current_project.get('name') if self.current_project else None,
            'projects_processed': len(self.processing_history),
            'agents_available': list(self.agent_framework.agents.keys()),
            'system_status': 'operational'
        }
