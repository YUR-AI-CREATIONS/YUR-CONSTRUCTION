"""
File Ingestion System

Handles ingestion of large plan sets in multiple formats:
- ZIP archives
- DWG (AutoCAD) files
- JPEG images
- PDF documents
"""

import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2
from PIL import Image
import ezdxf


class FileIngestionSystem:
    """
    Manages file uploads and extraction of construction plans
    """
    
    def __init__(self, upload_folder: str = "uploads", output_folder: str = "outputs"):
        self.upload_folder = Path(upload_folder)
        self.output_folder = Path(output_folder)
        self.upload_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
        
        self.supported_formats = ['.zip', '.dwg', '.jpeg', '.jpg', '.pdf', '.png']
        
    def ingest_file(self, file_path: str) -> Dict[str, Any]:
        """
        Ingest a file and prepare it for processing
        
        Args:
            file_path: Path to the file to ingest
            
        Returns:
            Dictionary containing file metadata and extracted content paths
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        file_ext = file_path.suffix.lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}")
            
        result = {
            'original_file': str(file_path),
            'file_type': file_ext,
            'file_size': file_path.stat().st_size,
            'extracted_files': []
        }
        
        # Handle different file types
        if file_ext == '.zip':
            result['extracted_files'] = self._extract_zip(file_path)
        elif file_ext == '.dwg':
            result['extracted_files'] = self._process_dwg(file_path)
        elif file_ext in ['.jpeg', '.jpg', '.png']:
            result['extracted_files'] = self._process_image(file_path)
        elif file_ext == '.pdf':
            result['extracted_files'] = self._process_pdf(file_path)
            
        return result
    
    def _extract_zip(self, zip_path: Path) -> List[Dict[str, Any]]:
        """Extract ZIP archive and process contained files"""
        extract_dir = self.output_folder / zip_path.stem
        extract_dir.mkdir(exist_ok=True)
        
        extracted_files = []
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            
            for file_name in zip_ref.namelist():
                file_path = extract_dir / file_name
                if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                    extracted_files.append({
                        'path': str(file_path),
                        'type': file_path.suffix.lower(),
                        'size': file_path.stat().st_size
                    })
                    
        return extracted_files
    
    def _process_dwg(self, dwg_path: Path) -> List[Dict[str, Any]]:
        """Process AutoCAD DWG file"""
        try:
            doc = ezdxf.readfile(str(dwg_path))
            
            return [{
                'path': str(dwg_path),
                'type': '.dwg',
                'size': dwg_path.stat().st_size,
                'layers': [layer.dxf.name for layer in doc.layers],
                'entities_count': len(list(doc.modelspace()))
            }]
        except Exception as e:
            # If DWG can't be read, still return basic info
            return [{
                'path': str(dwg_path),
                'type': '.dwg',
                'size': dwg_path.stat().st_size,
                'error': str(e)
            }]
    
    def _process_image(self, image_path: Path) -> List[Dict[str, Any]]:
        """Process image file"""
        try:
            with Image.open(image_path) as img:
                return [{
                    'path': str(image_path),
                    'type': image_path.suffix.lower(),
                    'size': image_path.stat().st_size,
                    'dimensions': img.size,
                    'format': img.format
                }]
        except Exception as e:
            return [{
                'path': str(image_path),
                'type': image_path.suffix.lower(),
                'size': image_path.stat().st_size,
                'error': str(e)
            }]
    
    def _process_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """Process PDF document"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract text from first page for preview
                first_page_text = pdf_reader.pages[0].extract_text() if num_pages > 0 else ""
                
                return [{
                    'path': str(pdf_path),
                    'type': '.pdf',
                    'size': pdf_path.stat().st_size,
                    'num_pages': num_pages,
                    'preview': first_page_text[:500]
                }]
        except Exception as e:
            return [{
                'path': str(pdf_path),
                'type': '.pdf',
                'size': pdf_path.stat().st_size,
                'error': str(e)
            }]
