"""
Cut/Fill Analyzer
Analyzes existing vs proposed elevations and generates 3D cut/fill models
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class ElevationPoint:
    """Point with elevation data"""
    x: float
    y: float
    existing_elevation: float
    proposed_elevation: float
    
    @property
    def cut_fill(self) -> float:
        """Positive = cut, Negative = fill"""
        return self.existing_elevation - self.proposed_elevation


@dataclass
class SoilProperties:
    """Soil properties from geotech report"""
    soil_type: str
    swell_factor: float  # Volume increase when excavated
    shrinkage_factor: float  # Volume decrease when compacted
    compaction_requirement: float  # % of maximum dry density
    is_rock: bool = False


class CutFillAnalyzer:
    """
    Analyzes cut and fill quantities for earthwork.
    Generates 3D models showing cut/fill areas with quantities.
    Applies swell and shrinkage factors from geotech report.
    """
    
    def __init__(self):
        self.elevation_points: List[ElevationPoint] = []
        self.soil_properties: Optional[SoilProperties] = None
        self.grid_spacing: float = 10.0  # feet
        
    def load_existing_elevations(
        self,
        survey_data: List[Tuple[float, float, float]]
    ):
        """
        Load existing elevation data from survey.
        
        Args:
            survey_data: List of (x, y, elevation) tuples
        """
        for x, y, elev in survey_data:
            # Find if point already exists
            existing_point = None
            for point in self.elevation_points:
                if abs(point.x - x) < 0.01 and abs(point.y - y) < 0.01:
                    existing_point = point
                    break
            
            if existing_point:
                existing_point.existing_elevation = elev
            else:
                self.elevation_points.append(
                    ElevationPoint(x, y, elev, elev)  # proposed = existing initially
                )
    
    def load_proposed_elevations(
        self,
        grading_plan: List[Tuple[float, float, float]]
    ):
        """
        Load proposed elevation data from grading plan.
        
        Args:
            grading_plan: List of (x, y, elevation) tuples
        """
        for x, y, elev in grading_plan:
            # Find existing point
            point_found = False
            for point in self.elevation_points:
                if abs(point.x - x) < 0.01 and abs(point.y - y) < 0.01:
                    point.proposed_elevation = elev
                    point_found = True
                    break
            
            if not point_found:
                # Add new point with estimated existing elevation
                self.elevation_points.append(
                    ElevationPoint(x, y, elev, elev)
                )
    
    def analyze_cut_fill(self) -> Dict:
        """
        Analyze cut and fill quantities.
        
        Returns:
            Dict with cut/fill analysis results
        """
        cut_points = []
        fill_points = []
        balanced_points = []
        
        total_cut_cy = 0
        total_fill_cy = 0
        
        for point in self.elevation_points:
            diff = point.cut_fill
            
            # Calculate volume for this point (approximation using grid spacing)
            area_sf = self.grid_spacing ** 2
            volume_cf = abs(diff) * area_sf
            volume_cy = volume_cf / 27  # Convert to cubic yards
            
            if diff > 0.1:  # Cut (existing higher than proposed)
                cut_points.append(point)
                total_cut_cy += volume_cy
            elif diff < -0.1:  # Fill (existing lower than proposed)
                fill_points.append(point)
                total_fill_cy += volume_cy
            else:  # Balanced
                balanced_points.append(point)
        
        # Apply swell and shrinkage factors
        cut_loose_cy = total_cut_cy
        fill_compacted_cy = total_fill_cy
        
        if self.soil_properties:
            cut_loose_cy = total_cut_cy * (1 + self.soil_properties.swell_factor)
            fill_compacted_cy = total_fill_cy / (1 - self.soil_properties.shrinkage_factor)
        
        # Calculate import/export
        net_balance = cut_loose_cy - fill_compacted_cy
        
        result = {
            "total_points": len(self.elevation_points),
            "cut_points": len(cut_points),
            "fill_points": len(fill_points),
            "balanced_points": len(balanced_points),
            "cut_volume": {
                "in_place_cy": round(total_cut_cy, 2),
                "loose_cy": round(cut_loose_cy, 2),
                "description": "Volume after excavation (includes swell)",
            },
            "fill_volume": {
                "in_place_cy": round(total_fill_cy, 2),
                "compacted_cy": round(fill_compacted_cy, 2),
                "description": "Volume needed before compaction",
            },
            "net_balance": {
                "volume_cy": round(net_balance, 2),
                "type": "export" if net_balance > 0 else "import",
                "description": "Excess material to export" if net_balance > 0 else "Material to import",
            },
            "swell_factor": self.soil_properties.swell_factor if self.soil_properties else 0.25,
            "shrinkage_factor": self.soil_properties.shrinkage_factor if self.soil_properties else 0.10,
        }
        
        return result
    
    def identify_rock_excavation(self, geotech_report_data: Dict) -> Dict:
        """
        Identify areas requiring rock excavation based on geotech report.
        
        Args:
            geotech_report_data: Geotech report with boring data
            
        Returns:
            Dict with rock excavation analysis
        """
        rock_zones = []
        total_rock_cy = 0
        
        # Parse boring data
        borings = geotech_report_data.get("borings", [])
        
        for boring in borings:
            location = boring.get("location", (0, 0))
            depth_to_rock = boring.get("depth_to_rock", None)
            
            if depth_to_rock is not None and depth_to_rock < 10:  # Rock within 10 feet
                # Find nearby elevation points
                for point in self.elevation_points:
                    distance = ((point.x - location[0])**2 + (point.y - location[1])**2)**0.5
                    
                    if distance < 50:  # Within 50 feet of boring
                        # Check if proposed elevation requires cutting into rock
                        if point.cut_fill > depth_to_rock:
                            rock_depth = point.cut_fill - depth_to_rock
                            area_sf = self.grid_spacing ** 2
                            rock_volume_cy = (rock_depth * area_sf) / 27
                            
                            rock_zones.append({
                                "location": (point.x, point.y),
                                "boring_ref": boring.get("id", "Unknown"),
                                "rock_depth_ft": round(rock_depth, 2),
                                "rock_volume_cy": round(rock_volume_cy, 2),
                            })
                            
                            total_rock_cy += rock_volume_cy
        
        return {
            "rock_excavation_required": len(rock_zones) > 0,
            "total_rock_volume_cy": round(total_rock_cy, 2),
            "rock_zones": rock_zones,
            "estimated_cost_per_cy": 85.0,  # Typical rock excavation cost
            "total_estimated_cost": round(total_rock_cy * 85.0, 2),
            "recommendations": [
                "Pre-blast if allowed by jurisdiction",
                "Consider ripping vs blasting based on rock hardness",
                "Factor in rock disposal or crushing for reuse",
                "Add contingency for unknown rock conditions",
            ],
        }
    
    def generate_3d_model(self) -> Dict:
        """
        Generate 3D model data for cut/fill visualization.
        
        Returns:
            Dict with 3D model data
        """
        vertices = []
        faces_cut = []
        faces_fill = []
        
        # Create 3D surface from elevation points
        for point in self.elevation_points:
            # Existing surface vertex
            vertices.append({
                "x": point.x,
                "y": point.y,
                "z": point.existing_elevation,
                "type": "existing",
            })
            
            # Proposed surface vertex
            vertices.append({
                "x": point.x,
                "y": point.y,
                "z": point.proposed_elevation,
                "type": "proposed",
            })
        
        # Generate faces (simplified - actual would create proper mesh)
        # Color code: red = cut, blue = fill, green = balanced
        for i, point in enumerate(self.elevation_points):
            if point.cut_fill > 0.1:
                color = [255, 0, 0]  # Red for cut
            elif point.cut_fill < -0.1:
                color = [0, 0, 255]  # Blue for fill
            else:
                color = [0, 255, 0]  # Green for balanced
            
            # Store face data (would create actual triangulated mesh in production)
            # This is placeholder structure
        
        model = {
            "vertices": vertices,
            "cut_areas": len([p for p in self.elevation_points if p.cut_fill > 0.1]),
            "fill_areas": len([p for p in self.elevation_points if p.cut_fill < -0.1]),
            "color_legend": {
                "red": "Cut areas",
                "blue": "Fill areas",
                "green": "Balanced areas",
            },
        }
        
        return model
    
    def generate_cross_sections(
        self,
        section_lines: List[List[Tuple[float, float]]]
    ) -> List[Dict]:
        """
        Generate cross-section profiles.
        
        Args:
            section_lines: List of section line coordinate pairs
            
        Returns:
            List of cross-section data
        """
        sections = []
        
        for i, line in enumerate(section_lines):
            section_data = {
                "section_id": f"Section {i + 1}",
                "start": line[0],
                "end": line[1],
                "profiles": {
                    "existing": [],
                    "proposed": [],
                },
                "statistics": {},
            }
            
            # Sample points along section line
            num_samples = 20
            for j in range(num_samples + 1):
                t = j / num_samples
                x = line[0][0] + t * (line[1][0] - line[0][0])
                y = line[0][1] + t * (line[1][1] - line[0][1])
                
                # Find nearest elevation point
                nearest_point = min(
                    self.elevation_points,
                    key=lambda p: ((p.x - x)**2 + (p.y - y)**2)**0.5
                )
                
                distance = ((j / num_samples) * 
                           ((line[1][0] - line[0][0])**2 + (line[1][1] - line[0][1])**2)**0.5)
                
                section_data["profiles"]["existing"].append({
                    "station": round(distance, 2),
                    "elevation": round(nearest_point.existing_elevation, 2),
                })
                
                section_data["profiles"]["proposed"].append({
                    "station": round(distance, 2),
                    "elevation": round(nearest_point.proposed_elevation, 2),
                })
            
            sections.append(section_data)
        
        return sections
    
    def export_to_format(self, filename: str, format_type: str = "json") -> str:
        """
        Export cut/fill analysis to file.
        
        Args:
            filename: Output filename
            format_type: Export format (json, csv, etc.)
            
        Returns:
            Success message
        """
        analysis = self.analyze_cut_fill()
        model = self.generate_3d_model()
        
        data = {
            "analysis": analysis,
            "model": model,
            "elevation_points": [
                {
                    "x": p.x,
                    "y": p.y,
                    "existing": p.existing_elevation,
                    "proposed": p.proposed_elevation,
                    "cut_fill": p.cut_fill,
                }
                for p in self.elevation_points
            ],
        }
        
        if format_type == "json":
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        
        return f"Cut/fill analysis exported to {filename}"
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate formatted cut/fill report"""
        report = """
CUT/FILL ANALYSIS REPORT
========================

SUMMARY:
"""
        report += f"Total Survey Points: {analysis['total_points']}\n"
        report += f"Cut Areas: {analysis['cut_points']} points\n"
        report += f"Fill Areas: {analysis['fill_points']} points\n"
        report += f"Balanced Areas: {analysis['balanced_points']} points\n\n"
        
        report += "QUANTITIES:\n"
        report += f"Cut Volume (In-Place): {analysis['cut_volume']['in_place_cy']:,.0f} CY\n"
        report += f"Cut Volume (Loose): {analysis['cut_volume']['loose_cy']:,.0f} CY\n"
        report += f"Fill Volume (Compacted): {analysis['fill_volume']['compacted_cy']:,.0f} CY\n\n"
        
        report += "NET BALANCE:\n"
        net = analysis['net_balance']
        report += f"Type: {net['type'].upper()}\n"
        report += f"Volume: {abs(net['volume_cy']):,.0f} CY\n"
        report += f"{net['description']}\n\n"
        
        report += "FACTORS APPLIED:\n"
        report += f"Swell Factor: {analysis['swell_factor']:.2%}\n"
        report += f"Shrinkage Factor: {analysis['shrinkage_factor']:.2%}\n"
        
        return report
