"""
Document Chunking System

Decomposes construction plans into structured chunks for AI processing
"""

from typing import List, Dict, Any
from pathlib import Path
import json


class DocumentChunk:
    """Represents a chunk of a construction document"""
    
    def __init__(self, chunk_id: str, content: Any, metadata: Dict[str, Any]):
        self.chunk_id = chunk_id
        self.content = content
        self.metadata = metadata
        self.processed = False
        self.results = None
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary"""
        return {
            'chunk_id': self.chunk_id,
            'content': str(self.content),
            'metadata': self.metadata,
            'processed': self.processed,
            'results': self.results
        }


class DocumentChunker:
    """
    Decomposes construction plans into structured chunks for processing
    """
    
    def __init__(self, chunk_size: int = 2000):
        self.chunk_size = chunk_size
        
    def chunk_document(self, file_info: Dict[str, Any]) -> List[DocumentChunk]:
        """
        Chunk a document based on its type
        
        Args:
            file_info: File information dictionary from ingestion
            
        Returns:
            List of DocumentChunk objects
        """
        file_type = file_info.get('file_type', '')
        file_path = file_info.get('original_file', '')
        
        if file_type == '.pdf':
            return self._chunk_pdf(file_info)
        elif file_type in ['.jpeg', '.jpg', '.png']:
            return self._chunk_image(file_info)
        elif file_type == '.dwg':
            return self._chunk_dwg(file_info)
        elif file_type == '.zip':
            return self._chunk_archive(file_info)
        else:
            return []
    
    def _chunk_pdf(self, file_info: Dict[str, Any]) -> List[DocumentChunk]:
        """Chunk PDF document by pages"""
        chunks = []
        extracted_files = file_info.get('extracted_files', [])
        
        for file_data in extracted_files:
            num_pages = file_data.get('num_pages', 1)
            
            for page_num in range(num_pages):
                chunk = DocumentChunk(
                    chunk_id=f"{Path(file_data['path']).stem}_page_{page_num+1}",
                    content={
                        'file_path': file_data['path'],
                        'page': page_num + 1,
                        'type': 'pdf_page'
                    },
                    metadata={
                        'source_file': file_data['path'],
                        'page_number': page_num + 1,
                        'total_pages': num_pages,
                        'document_type': 'construction_plan'
                    }
                )
                chunks.append(chunk)
                
        return chunks
    
    def _chunk_image(self, file_info: Dict[str, Any]) -> List[DocumentChunk]:
        """Chunk image file (single chunk per image)"""
        chunks = []
        extracted_files = file_info.get('extracted_files', [])
        
        for file_data in extracted_files:
            chunk = DocumentChunk(
                chunk_id=f"{Path(file_data['path']).stem}_image",
                content={
                    'file_path': file_data['path'],
                    'type': 'image',
                    'dimensions': file_data.get('dimensions', (0, 0))
                },
                metadata={
                    'source_file': file_data['path'],
                    'image_format': file_data.get('format', 'unknown'),
                    'document_type': 'construction_plan'
                }
            )
            chunks.append(chunk)
            
        return chunks
    
    def _chunk_dwg(self, file_info: Dict[str, Any]) -> List[DocumentChunk]:
        """Chunk DWG file by layers"""
        chunks = []
        extracted_files = file_info.get('extracted_files', [])
        
        for file_data in extracted_files:
            layers = file_data.get('layers', [])
            
            if layers:
                # Create chunks for each layer
                for layer in layers:
                    chunk = DocumentChunk(
                        chunk_id=f"{Path(file_data['path']).stem}_layer_{layer}",
                        content={
                            'file_path': file_data['path'],
                            'layer': layer,
                            'type': 'dwg_layer'
                        },
                        metadata={
                            'source_file': file_data['path'],
                            'layer_name': layer,
                            'document_type': 'cad_drawing'
                        }
                    )
                    chunks.append(chunk)
            else:
                # Single chunk for entire DWG if no layers
                chunk = DocumentChunk(
                    chunk_id=f"{Path(file_data['path']).stem}_dwg",
                    content={
                        'file_path': file_data['path'],
                        'type': 'dwg_complete'
                    },
                    metadata={
                        'source_file': file_data['path'],
                        'document_type': 'cad_drawing'
                    }
                )
                chunks.append(chunk)
                
        return chunks
    
    def _chunk_archive(self, file_info: Dict[str, Any]) -> List[DocumentChunk]:
        """Process files from archive"""
        chunks = []
        extracted_files = file_info.get('extracted_files', [])
        
        for file_data in extracted_files:
            # Create a sub-file-info for recursive processing
            sub_file_info = {
                'original_file': file_data['path'],
                'file_type': file_data['type'],
                'extracted_files': [file_data]
            }
            
            # Recursively chunk each file
            sub_chunks = self.chunk_document(sub_file_info)
            chunks.extend(sub_chunks)
            
        return chunks
