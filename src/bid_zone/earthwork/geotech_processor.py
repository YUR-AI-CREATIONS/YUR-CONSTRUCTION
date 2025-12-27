"""
Geotech Report Processor
Processes geotechnical reports and extracts soil properties and recommendations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Boring:
    """Geotechnical boring data"""
    id: str
    location: tuple  # (x, y) coordinates
    elevation: float
    depth: float
    soil_layers: List[Dict]
    groundwater_depth: Optional[float]
    rock_depth: Optional[float]


@dataclass
class SoilLayer:
    """Soil layer information"""
    depth_from: float
    depth_to: float
    soil_type: str
    description: str
    uscs_classification: str
    blows_per_foot: Optional[int]  # SPT N-value
    moisture_content: Optional[float]
    is_rock: bool = False


class GeotechProcessor:
    """
    Processes geotechnical reports and extracts key information.
    Provides soil properties, bearing capacities, and excavation recommendations.
    """
    
    def __init__(self):
        self.borings: List[Boring] = []
        self.soil_properties: Dict[str, Dict] = {}
        self.recommendations: Dict[str, List[str]] = {}
        
    def process_report(self, report_data: Dict) -> Dict:
        """
        Process complete geotechnical report.
        
        Args:
            report_data: Parsed geotech report data
            
        Returns:
            Dict with processed information
        """
        # Extract boring data
        self._parse_borings(report_data.get("borings", []))
        
        # Analyze soil conditions
        soil_analysis = self._analyze_soil_conditions()
        
        # Determine excavation factors
        excavation_factors = self._determine_excavation_factors()
        
        # Extract bearing capacity
        bearing_capacity = self._extract_bearing_capacity(report_data)
        
        # Extract recommendations
        recommendations = self._extract_recommendations(report_data)
        
        result = {
            "project_info": report_data.get("project_info", {}),
            "boring_count": len(self.borings),
            "borings": [self._boring_to_dict(b) for b in self.borings],
            "soil_analysis": soil_analysis,
            "excavation_factors": excavation_factors,
            "bearing_capacity": bearing_capacity,
            "recommendations": recommendations,
            "rock_excavation": self._analyze_rock_conditions(),
        }
        
        return result
    
    def _parse_borings(self, boring_data: List[Dict]):
        """Parse boring data from report"""
        for data in boring_data:
            layers = []
            for layer_data in data.get("layers", []):
                layer = SoilLayer(
                    depth_from=layer_data.get("depth_from", 0),
                    depth_to=layer_data.get("depth_to", 0),
                    soil_type=layer_data.get("soil_type", "Unknown"),
                    description=layer_data.get("description", ""),
                    uscs_classification=layer_data.get("uscs", ""),
                    blows_per_foot=layer_data.get("n_value"),
                    moisture_content=layer_data.get("moisture"),
                    is_rock=layer_data.get("is_rock", False),
                )
                layers.append(layer.__dict__)
            
            boring = Boring(
                id=data.get("id", "Unknown"),
                location=tuple(data.get("location", (0, 0))),
                elevation=data.get("elevation", 0),
                depth=data.get("depth", 0),
                soil_layers=layers,
                groundwater_depth=data.get("groundwater_depth"),
                rock_depth=data.get("rock_depth"),
            )
            
            self.borings.append(boring)
    
    def _analyze_soil_conditions(self) -> Dict:
        """Analyze overall soil conditions"""
        if not self.borings:
            return self._get_default_soil_analysis()
        
        # Analyze predominant soil types
        soil_type_counts = {}
        total_layers = 0
        
        for boring in self.borings:
            for layer in boring.soil_layers:
                soil_type = layer.get("soil_type", "Unknown")
                soil_type_counts[soil_type] = soil_type_counts.get(soil_type, 0) + 1
                total_layers += 1
        
        predominant_soil = max(soil_type_counts.items(), key=lambda x: x[1])[0] if soil_type_counts else "Unknown"
        
        # Check for groundwater
        groundwater_present = any(b.groundwater_depth is not None for b in self.borings)
        avg_groundwater_depth = None
        if groundwater_present:
            depths = [b.groundwater_depth for b in self.borings if b.groundwater_depth is not None]
            avg_groundwater_depth = sum(depths) / len(depths) if depths else None
        
        # Check for rock
        rock_present = any(b.rock_depth is not None for b in self.borings)
        
        return {
            "predominant_soil_type": predominant_soil,
            "soil_types_found": list(soil_type_counts.keys()),
            "groundwater_present": groundwater_present,
            "average_groundwater_depth": avg_groundwater_depth,
            "rock_present": rock_present,
            "total_borings": len(self.borings),
            "soil_variability": "High" if len(soil_type_counts) > 3 else "Moderate" if len(soil_type_counts) > 1 else "Low",
        }
    
    def _get_default_soil_analysis(self) -> Dict:
        """Return default soil analysis when no boring data"""
        return {
            "predominant_soil_type": "Silty Clay",
            "soil_types_found": ["Silty Clay", "Sandy Clay"],
            "groundwater_present": False,
            "average_groundwater_depth": None,
            "rock_present": False,
            "total_borings": 0,
            "soil_variability": "Unknown",
            "note": "Using assumed soil conditions - geotech report recommended",
        }
    
    def _determine_excavation_factors(self) -> Dict:
        """
        Determine swell and shrinkage factors for excavation.
        Based on soil type and conditions.
        """
        soil_analysis = self._analyze_soil_conditions()
        predominant_soil = soil_analysis["predominant_soil_type"]
        
        # Standard excavation factors by soil type
        factor_table = {
            "Clay": {"swell": 0.30, "shrinkage": 0.10, "compaction": 0.95},
            "Silty Clay": {"swell": 0.25, "shrinkage": 0.08, "compaction": 0.95},
            "Sandy Clay": {"swell": 0.22, "shrinkage": 0.07, "compaction": 0.95},
            "Sand": {"swell": 0.15, "shrinkage": 0.05, "compaction": 0.95},
            "Silty Sand": {"swell": 0.18, "shrinkage": 0.06, "compaction": 0.95},
            "Gravel": {"swell": 0.12, "shrinkage": 0.04, "compaction": 0.95},
            "Rock": {"swell": 0.50, "shrinkage": 0.00, "compaction": 1.00},
        }
        
        # Get factors for predominant soil, default to silty clay
        factors = factor_table.get(predominant_soil, factor_table["Silty Clay"])
        
        return {
            "soil_type": predominant_soil,
            "swell_factor": factors["swell"],
            "swell_factor_percent": factors["swell"] * 100,
            "shrinkage_factor": factors["shrinkage"],
            "shrinkage_factor_percent": factors["shrinkage"] * 100,
            "compaction_requirement": factors["compaction"],
            "compaction_percent": factors["compaction"] * 100,
            "notes": [
                f"Swell: Cut material increases {factors['swell'] * 100:.0f}% when excavated",
                f"Shrinkage: Fill material decreases {factors['shrinkage'] * 100:.0f}% when compacted",
                f"Compaction required: {factors['compaction'] * 100:.0f}% of maximum dry density",
            ],
        }
    
    def _extract_bearing_capacity(self, report_data: Dict) -> Dict:
        """Extract bearing capacity recommendations"""
        # Try to extract from report data
        if "bearing_capacity" in report_data:
            return report_data["bearing_capacity"]
        
        # Default values based on typical conditions
        return {
            "allowable_bearing_pressure_psf": 2500,
            "foundation_type": "Shallow spread footings",
            "minimum_embedment_depth": 18,  # inches
            "recommendations": [
                "Footings should bear on undisturbed natural soil",
                "Remove all loose or disturbed material from footing excavations",
                "Proof-roll subgrade and verify with geotechnical engineer",
            ],
        }
    
    def _extract_recommendations(self, report_data: Dict) -> Dict:
        """Extract design and construction recommendations"""
        return {
            "site_preparation": [
                "Strip and remove topsoil (typically 6-12 inches)",
                "Remove vegetation and organic materials",
                "Proof-roll exposed subgrade with loaded truck",
                "Repair soft or yielding areas as directed by geotechnical engineer",
            ],
            "earthwork": [
                "Place fill in maximum 8-inch loose lifts",
                "Compact each lift to 95% of maximum dry density",
                "Maintain moisture content within 2% of optimum",
                "Test compaction at frequency of 1 per 2,500 SF per lift",
            ],
            "excavation": [
                "Slope excavations per OSHA requirements",
                "Protect excavations from surface water infiltration",
                "Shore or brace vertical cuts as required",
                "Monitor excavations for groundwater seepage",
            ],
            "drainage": [
                "Provide positive drainage away from structures",
                "Install perimeter drains at footing elevations",
                "Grade site to drain surface water away from buildings",
                "Prevent ponding of water on site",
            ],
        }
    
    def _analyze_rock_conditions(self) -> Dict:
        """Analyze rock excavation requirements"""
        rock_present = False
        rock_zones = []
        total_rock_volume_estimate = 0
        
        for boring in self.borings:
            if boring.rock_depth is not None and boring.rock_depth < boring.depth:
                rock_present = True
                rock_thickness = boring.depth - boring.rock_depth
                
                rock_zones.append({
                    "boring_id": boring.id,
                    "location": boring.location,
                    "depth_to_rock": boring.rock_depth,
                    "rock_thickness": rock_thickness,
                })
        
        if rock_present:
            return {
                "rock_present": True,
                "rock_zones": rock_zones,
                "excavation_method": "Ripping or blasting may be required",
                "estimated_cost_multiplier": 4.0,  # Rock is ~4x normal excavation cost
                "recommendations": [
                    "Engage blasting contractor for rock removal",
                    "Consider rock crushing for reuse as base material",
                    "Obtain blasting permits if required",
                    "Conduct pre-blast survey of nearby structures",
                    "Monitor vibrations during rock removal",
                ],
            }
        else:
            return {
                "rock_present": False,
                "excavation_method": "Standard excavation equipment adequate",
                "estimated_cost_multiplier": 1.0,
            }
    
    def _boring_to_dict(self, boring: Boring) -> Dict:
        """Convert boring object to dictionary"""
        return {
            "id": boring.id,
            "location": boring.location,
            "elevation": boring.elevation,
            "depth": boring.depth,
            "groundwater_depth": boring.groundwater_depth,
            "rock_depth": boring.rock_depth,
            "layer_count": len(boring.soil_layers),
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate formatted geotechnical report summary"""
        report = """
GEOTECHNICAL REPORT SUMMARY
===========================

"""
        
        soil = analysis["soil_analysis"]
        report += f"Total Borings: {soil['total_borings']}\n"
        report += f"Predominant Soil: {soil['predominant_soil_type']}\n"
        report += f"Soil Variability: {soil['soil_variability']}\n"
        report += f"Groundwater Present: {'Yes' if soil['groundwater_present'] else 'No'}\n"
        
        if soil['average_groundwater_depth']:
            report += f"Average Groundwater Depth: {soil['average_groundwater_depth']:.1f} ft\n"
        
        report += f"\nROCK CONDITIONS:\n"
        rock = analysis["rock_excavation"]
        report += f"Rock Present: {'Yes' if rock['rock_present'] else 'No'}\n"
        report += f"Excavation Method: {rock['excavation_method']}\n"
        
        report += f"\nEXCAVATION FACTORS:\n"
        factors = analysis["excavation_factors"]
        report += f"Swell Factor: {factors['swell_factor_percent']:.0f}%\n"
        report += f"Shrinkage Factor: {factors['shrinkage_factor_percent']:.0f}%\n"
        report += f"Compaction Requirement: {factors['compaction_percent']:.0f}%\n"
        
        report += f"\nBEARING CAPACITY:\n"
        bearing = analysis["bearing_capacity"]
        report += f"Allowable Bearing Pressure: {bearing['allowable_bearing_pressure_psf']} psf\n"
        report += f"Foundation Type: {bearing['foundation_type']}\n"
        
        return report
