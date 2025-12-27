"""
AI-Powered Estimator
Integrates OpenAI Vision, Google Vision, and Gemini Vision for document analysis
"""

from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import base64
import os


@dataclass
class EstimateItem:
    """Individual estimate line item"""
    division: str
    item_number: str
    description: str
    quantity: float
    unit: str
    unit_price: float
    total_price: float
    source: str  # e.g., "plan_sheet_3", "spec_section_03"


class AIEstimator:
    """
    AI-Powered construction estimator using multiple vision APIs.
    Reads and analyzes PDFs, scanned documents, and extracts quantity information.
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        google_api_key: Optional[str] = None,
        gemini_api_key: Optional[str] = None,
    ):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.google_api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        
        self.estimates: List[EstimateItem] = []
        
    def analyze_document(
        self,
        document_path: str,
        document_type: str = "construction_plans",
        use_api: str = "all"
    ) -> Dict:
        """
        Analyze construction documents using AI vision.
        
        Args:
            document_path: Path to PDF or image file
            document_type: Type of document (plans, specs, geotech, etc.)
            use_api: Which API to use ('openai', 'google', 'gemini', 'all')
            
        Returns:
            Dict containing extracted information and estimates
        """
        results = {
            "document_path": document_path,
            "document_type": document_type,
            "metadata": self._extract_metadata(document_path),
            "analysis_results": {},
        }
        
        # Use multiple APIs for cross-validation
        if use_api in ["openai", "all"]:
            results["analysis_results"]["openai"] = self._analyze_with_openai(document_path)
        
        if use_api in ["google", "all"]:
            results["analysis_results"]["google"] = self._analyze_with_google(document_path)
        
        if use_api in ["gemini", "all"]:
            results["analysis_results"]["gemini"] = self._analyze_with_gemini(document_path)
        
        # Consolidate results
        results["consolidated_data"] = self._consolidate_results(results["analysis_results"])
        results["estimate_items"] = self._create_estimate_items(results["consolidated_data"])
        
        return results
    
    def _extract_metadata(self, document_path: str) -> Dict:
        """Extract document metadata"""
        return {
            "filename": os.path.basename(document_path),
            "file_size": os.path.getsize(document_path) if os.path.exists(document_path) else 0,
            "file_type": os.path.splitext(document_path)[1],
            "extraction_method": "AI Vision APIs",
        }
    
    def _analyze_with_openai(self, document_path: str) -> Dict:
        """
        Analyze document using OpenAI Vision API.
        
        This is a placeholder for actual OpenAI Vision API integration.
        """
        # Placeholder response structure
        return {
            "api": "OpenAI Vision",
            "status": "success",
            "detected_elements": [
                {
                    "type": "dimension",
                    "value": "100 LF",
                    "context": "8\" PVC Sewer Line",
                    "confidence": 0.95,
                },
                {
                    "type": "quantity",
                    "value": "25 CY",
                    "context": "Concrete Footings",
                    "confidence": 0.92,
                },
                {
                    "type": "specification",
                    "value": "ASTM A615 Grade 60",
                    "context": "Rebar specifications",
                    "confidence": 0.98,
                },
            ],
            "plan_details": {
                "scale": "1:40",
                "sheet_number": "C-1.0",
                "revision": "Rev 2",
            },
        }
    
    def _analyze_with_google(self, document_path: str) -> Dict:
        """
        Analyze document using Google Vision API.
        
        This is a placeholder for actual Google Vision API integration.
        """
        return {
            "api": "Google Vision",
            "status": "success",
            "text_extraction": {
                "full_text": "Sample extracted text from plans...",
                "structured_data": [
                    {"category": "dimensions", "items": ["100 LF", "25 CY"]},
                    {"category": "materials", "items": ["8\" PVC", "Concrete 3000 PSI"]},
                ],
            },
            "object_detection": {
                "symbols": ["North arrow", "Scale bar", "Detail callout"],
                "lines_detected": 1250,
            },
        }
    
    def _analyze_with_gemini(self, document_path: str) -> Dict:
        """
        Analyze document using Gemini Vision API.
        
        This is a placeholder for actual Gemini Vision API integration.
        """
        return {
            "api": "Gemini Vision",
            "status": "success",
            "understanding": {
                "document_summary": "Civil engineering plan showing site utilities and grading",
                "key_components": [
                    "Water line routing",
                    "Sewer collection system",
                    "Storm drainage",
                    "Grading plan with contours",
                ],
            },
            "quantities_identified": [
                {"item": "8\" Water Line", "quantity": 985, "unit": "LF"},
                {"item": "8\" Sewer Line", "quantity": 1100, "unit": "LF"},
                {"item": "Manholes", "quantity": 12, "unit": "EA"},
            ],
        }
    
    def _consolidate_results(self, analysis_results: Dict) -> Dict:
        """
        Consolidate results from multiple AI APIs.
        Cross-validates and merges data from different sources.
        """
        consolidated = {
            "quantities": [],
            "materials": [],
            "specifications": [],
            "confidence_scores": {},
        }
        
        # Merge quantities from all APIs
        for api_name, results in analysis_results.items():
            if api_name == "openai" and "detected_elements" in results:
                for element in results["detected_elements"]:
                    if element["type"] == "quantity":
                        consolidated["quantities"].append({
                            "value": element["value"],
                            "context": element["context"],
                            "source": api_name,
                            "confidence": element["confidence"],
                        })
            
            if api_name == "gemini" and "quantities_identified" in results:
                for qty in results["quantities_identified"]:
                    consolidated["quantities"].append({
                        "value": f"{qty['quantity']} {qty['unit']}",
                        "context": qty["item"],
                        "source": api_name,
                        "confidence": 0.90,
                    })
        
        return consolidated
    
    def _create_estimate_items(self, consolidated_data: Dict) -> List[EstimateItem]:
        """
        Create structured estimate items from consolidated data.
        Organizes by CSI MasterFormat divisions.
        """
        items = []
        
        # Example items based on consolidated data
        division_map = {
            "Concrete": "03",
            "Utilities": "33",
            "Earthwork": "31",
            "Steel": "05",
        }
        
        # Parse quantities and create estimate items
        for qty_data in consolidated_data.get("quantities", []):
            # Determine division based on context
            context = qty_data.get("context", "")
            division = "01"  # Default
            division_name = "General"
            
            if "concrete" in context.lower():
                division = "03"
                division_name = "Concrete"
            elif "sewer" in context.lower() or "water" in context.lower():
                division = "33"
                division_name = "Utilities"
            elif "excavation" in context.lower() or "earthwork" in context.lower():
                division = "31"
                division_name = "Earthwork"
            elif "steel" in context.lower() or "rebar" in context.lower():
                division = "05"
                division_name = "Metals"
            
            # Parse quantity value
            value_str = qty_data.get("value", "0")
            parts = value_str.split()
            quantity = float(parts[0]) if parts else 0
            unit = parts[1] if len(parts) > 1 else "LS"
            
            # Estimate unit price (placeholder - would come from cost database)
            unit_price = self._estimate_unit_price(context, unit)
            
            item = EstimateItem(
                division=f"{division} - {division_name}",
                item_number=f"{division}-001",
                description=context,
                quantity=quantity,
                unit=unit,
                unit_price=unit_price,
                total_price=quantity * unit_price,
                source=qty_data.get("source", "unknown"),
            )
            
            items.append(item)
        
        self.estimates.extend(items)
        return items
    
    def _estimate_unit_price(self, description: str, unit: str) -> float:
        """
        Estimate unit price based on description and unit.
        In production, this would query a cost database.
        """
        # Simplified pricing logic
        price_map = {
            "CY": 150.0,  # Default per cubic yard
            "LF": 45.0,   # Default per linear foot
            "SF": 12.0,   # Default per square foot
            "EA": 500.0,  # Default per each
            "LS": 5000.0, # Default lump sum
        }
        
        base_price = price_map.get(unit, 100.0)
        
        # Adjust based on description
        if "concrete" in description.lower():
            return base_price * 1.2
        elif "steel" in description.lower():
            return base_price * 1.5
        elif "sewer" in description.lower():
            return base_price * 1.3
        
        return base_price
    
    def generate_estimate_by_division(self) -> Dict[str, List[EstimateItem]]:
        """
        Organize estimate items by CSI division.
        """
        by_division = {}
        
        for item in self.estimates:
            division = item.division
            if division not in by_division:
                by_division[division] = []
            by_division[division].append(item)
        
        return by_division
    
    def calculate_totals(self) -> Dict:
        """
        Calculate estimate totals and summary.
        """
        by_division = self.generate_estimate_by_division()
        
        division_totals = {}
        grand_total = 0
        
        for division, items in by_division.items():
            division_total = sum(item.total_price for item in items)
            division_totals[division] = {
                "item_count": len(items),
                "total": division_total,
            }
            grand_total += division_total
        
        return {
            "division_totals": division_totals,
            "grand_total": grand_total,
            "item_count": len(self.estimates),
        }
    
    def generate_report(self) -> str:
        """
        Generate professional estimate report.
        """
        totals = self.calculate_totals()
        by_division = self.generate_estimate_by_division()
        
        report = """
CONSTRUCTION ESTIMATE REPORT
============================

"""
        
        for division, items in sorted(by_division.items()):
            division_total = totals["division_totals"][division]["total"]
            report += f"\n{division}\n"
            report += "=" * len(division) + "\n\n"
            
            for item in items:
                report += f"{item.item_number} - {item.description}\n"
                report += f"  Quantity: {item.quantity:,.2f} {item.unit}\n"
                report += f"  Unit Price: ${item.unit_price:,.2f}\n"
                report += f"  Total: ${item.total_price:,.2f}\n"
                report += f"  Source: {item.source}\n\n"
            
            report += f"Division Total: ${division_total:,.2f}\n"
            report += "-" * 50 + "\n"
        
        report += f"\nGRAND TOTAL: ${totals['grand_total']:,.2f}\n"
        report += f"Total Items: {totals['item_count']}\n"
        
        return report
