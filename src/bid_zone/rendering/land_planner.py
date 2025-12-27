"""
Land Planner
Generates multiple land development layout options based on zoning requirements
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class ZoningRequirements:
    """Zoning requirements for development"""
    designation: str  # e.g., "R-1", "R-2", "PUD"
    min_lot_size_sf: float
    min_lot_width: float
    min_lot_depth: float
    max_density_units_per_acre: float
    setback_front: float
    setback_rear: float
    setback_side: float
    max_lot_coverage_percent: float
    max_building_height: float


@dataclass
class LotLayout:
    """Individual lot definition"""
    lot_number: int
    area_sf: float
    width: float
    depth: float
    corners: List[Tuple[float, float]]
    frontage_road: str
    buildable_area_sf: float


class LandPlanner:
    """
    Generates multiple land development layout options based on zoning.
    Creates 4-5 different configurations optimized for different objectives.
    """
    
    def __init__(self):
        self.site_boundary: Optional[List[Tuple[float, float]]] = None
        self.site_area_acres: float = 0.0
        self.zoning: Optional[ZoningRequirements] = None
        self.generated_options: List[Dict] = []
        
    def analyze_site(
        self,
        boundary_points: List[Tuple[float, float]],
        zoning_designation: str,
        constraints: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze site and determine development potential.
        
        Args:
            boundary_points: Site boundary coordinates
            zoning_designation: Zoning code (e.g., "R-1")
            constraints: Optional site constraints (wetlands, easements, etc.)
            
        Returns:
            Site analysis results
        """
        self.site_boundary = boundary_points
        self.site_area_acres = self._calculate_area(boundary_points) / 43560  # Convert to acres
        self.zoning = self._get_zoning_requirements(zoning_designation)
        
        constraints = constraints or {}
        
        # Calculate developable area
        constrained_area_sf = sum(constraints.get("areas", {}).values())
        developable_area_sf = (self.site_area_acres * 43560) - constrained_area_sf
        developable_acres = developable_area_sf / 43560
        
        # Calculate maximum lots based on zoning
        max_lots_density = int(developable_acres * self.zoning.max_density_units_per_acre)
        max_lots_size = int(developable_area_sf / self.zoning.min_lot_size_sf)
        max_lots = min(max_lots_density, max_lots_size)
        
        analysis = {
            "site_area_acres": self.site_area_acres,
            "developable_acres": developable_acres,
            "zoning": zoning_designation,
            "zoning_requirements": {
                "min_lot_size_sf": self.zoning.min_lot_size_sf,
                "max_density": self.zoning.max_density_units_per_acre,
                "setbacks": {
                    "front": self.zoning.setback_front,
                    "rear": self.zoning.setback_rear,
                    "side": self.zoning.setback_side,
                },
            },
            "maximum_lots": max_lots,
            "constraints": constraints,
            "recommended_lot_count": int(max_lots * 0.85),  # 85% efficiency
        }
        
        return analysis
    
    def generate_layout_options(
        self,
        boundary_points: List[Tuple[float, float]],
        zoning_designation: str,
        target_lot_count: Optional[int] = None
    ) -> List[Dict]:
        """
        Generate 4-5 different layout options optimized for different goals.
        
        Args:
            boundary_points: Site boundary coordinates
            zoning_designation: Zoning code
            target_lot_count: Optional target number of lots
            
        Returns:
            List of layout options
        """
        analysis = self.analyze_site(boundary_points, zoning_designation)
        
        if target_lot_count is None:
            target_lot_count = analysis["recommended_lot_count"]
        
        options = []
        
        # Option 1: Maximum Density
        options.append(self._generate_max_density_layout(analysis))
        
        # Option 2: Premium Lots (larger lots, lower density)
        options.append(self._generate_premium_layout(analysis))
        
        # Option 3: Mixed Size Lots
        options.append(self._generate_mixed_layout(analysis))
        
        # Option 4: Cul-de-sac Design
        options.append(self._generate_culdesac_layout(analysis))
        
        # Option 5: Grid Pattern
        options.append(self._generate_grid_layout(analysis))
        
        self.generated_options = options
        return options
    
    def _generate_max_density_layout(self, analysis: Dict) -> Dict:
        """
        Generate maximum density layout option.
        Optimizes for maximum number of lots within zoning constraints.
        """
        max_lots = analysis["maximum_lots"]
        avg_lot_size = (analysis["developable_acres"] * 43560) / max_lots if max_lots > 0 else 0
        
        # Generate lot layout
        lots = self._create_lots_grid_pattern(
            max_lots,
            avg_lot_size,
            lot_width=self.zoning.min_lot_width,
        )
        
        return {
            "option_name": "Maximum Density",
            "description": "Optimized for maximum lot count within zoning limits",
            "lot_count": max_lots,
            "average_lot_size_sf": avg_lot_size,
            "total_road_length_lf": self._estimate_road_length(max_lots),
            "lots": lots,
            "pros": [
                "Maximizes revenue potential",
                "Efficient use of land",
                "Lower per-lot infrastructure cost",
            ],
            "cons": [
                "Minimum lot sizes",
                "Higher density may impact sales pace",
                "Less premium pricing opportunity",
            ],
            "estimated_development_cost": self._estimate_development_cost(max_lots),
            "projected_revenue": max_lots * 85000,  # Estimated price per lot
        }
    
    def _generate_premium_layout(self, analysis: Dict) -> Dict:
        """
        Generate premium large-lot layout option.
        Larger lots for premium pricing.
        """
        lot_count = int(analysis["maximum_lots"] * 0.65)  # 35% fewer lots
        avg_lot_size = (analysis["developable_acres"] * 43560) / lot_count if lot_count > 0 else 0
        
        lots = self._create_lots_grid_pattern(
            lot_count,
            avg_lot_size,
            lot_width=self.zoning.min_lot_width * 1.4,
        )
        
        return {
            "option_name": "Premium Large Lots",
            "description": "Larger lots targeting premium buyers",
            "lot_count": lot_count,
            "average_lot_size_sf": avg_lot_size,
            "total_road_length_lf": self._estimate_road_length(lot_count),
            "lots": lots,
            "pros": [
                "Premium pricing opportunity",
                "Attractive to high-end buyers",
                "Lower competition density",
                "Better landscaping potential",
            ],
            "cons": [
                "Fewer total lots",
                "Higher per-lot infrastructure cost",
                "Longer absorption period",
            ],
            "estimated_development_cost": self._estimate_development_cost(lot_count),
            "projected_revenue": lot_count * 115000,  # Premium pricing
        }
    
    def _generate_mixed_layout(self, analysis: Dict) -> Dict:
        """
        Generate mixed lot size layout.
        Variety of lot sizes for different market segments.
        """
        total_lots = analysis["recommended_lot_count"]
        
        # Mix of lot sizes
        small_lots = int(total_lots * 0.30)  # 30% small
        medium_lots = int(total_lots * 0.50)  # 50% medium
        large_lots = total_lots - small_lots - medium_lots  # 20% large
        
        lots = []
        lots.extend(self._create_lots_grid_pattern(small_lots, 8000, 60))
        lots.extend(self._create_lots_grid_pattern(medium_lots, 10000, 70))
        lots.extend(self._create_lots_grid_pattern(large_lots, 13000, 85))
        
        return {
            "option_name": "Mixed Lot Sizes",
            "description": "Variety of lot sizes for different buyer segments",
            "lot_count": total_lots,
            "lot_mix": {
                "small (8,000 SF)": small_lots,
                "medium (10,000 SF)": medium_lots,
                "large (13,000 SF)": large_lots,
            },
            "total_road_length_lf": self._estimate_road_length(total_lots),
            "lots": lots,
            "pros": [
                "Appeals to multiple buyer segments",
                "Diversified risk",
                "Flexible pricing strategy",
                "Faster overall absorption",
            ],
            "cons": [
                "More complex to market",
                "Varied infrastructure per lot type",
            ],
            "estimated_development_cost": self._estimate_development_cost(total_lots),
            "projected_revenue": (small_lots * 75000) + (medium_lots * 90000) + (large_lots * 110000),
        }
    
    def _generate_culdesac_layout(self, analysis: Dict) -> Dict:
        """
        Generate cul-de-sac based layout.
        Traditional suburban layout with cul-de-sacs.
        """
        lot_count = int(analysis["recommended_lot_count"] * 0.90)
        avg_lot_size = (analysis["developable_acres"] * 43560) / lot_count if lot_count > 0 else 0
        
        lots = self._create_lots_culdesac_pattern(lot_count, avg_lot_size)
        
        return {
            "option_name": "Cul-de-Sac Design",
            "description": "Traditional suburban layout with cul-de-sacs",
            "lot_count": lot_count,
            "average_lot_size_sf": avg_lot_size,
            "cul_de_sacs": int(lot_count / 15),  # Approximately 15 lots per cul-de-sac
            "total_road_length_lf": self._estimate_road_length(lot_count) * 1.15,  # Slightly more road
            "lots": lots,
            "pros": [
                "Low traffic on residential streets",
                "Safe for children",
                "Traditional neighborhood feel",
                "Good market acceptance",
            ],
            "cons": [
                "More road length per lot",
                "Higher infrastructure cost",
                "Emergency vehicle access considerations",
            ],
            "estimated_development_cost": self._estimate_development_cost(lot_count) * 1.1,
            "projected_revenue": lot_count * 92000,
        }
    
    def _generate_grid_layout(self, analysis: Dict) -> Dict:
        """
        Generate grid pattern layout.
        Efficient grid-based street network.
        """
        lot_count = int(analysis["recommended_lot_count"] * 0.95)
        avg_lot_size = (analysis["developable_acres"] * 43560) / lot_count if lot_count > 0 else 0
        
        lots = self._create_lots_grid_pattern(
            lot_count,
            avg_lot_size,
            lot_width=self.zoning.min_lot_width * 1.15,
        )
        
        return {
            "option_name": "Grid Pattern",
            "description": "Efficient grid-based street layout",
            "lot_count": lot_count,
            "average_lot_size_sf": avg_lot_size,
            "total_road_length_lf": self._estimate_road_length(lot_count),
            "lots": lots,
            "pros": [
                "Efficient land use",
                "Easy navigation",
                "Multiple access routes",
                "Lower road costs",
                "Good connectivity",
            ],
            "cons": [
                "Higher traffic on residential streets",
                "Less distinctive character",
            ],
            "estimated_development_cost": self._estimate_development_cost(lot_count) * 0.95,
            "projected_revenue": lot_count * 88000,
        }
    
    def _create_lots_grid_pattern(
        self,
        count: int,
        avg_size_sf: float,
        lot_width: float
    ) -> List[LotLayout]:
        """Create lots in grid pattern"""
        lots = []
        lot_depth = avg_size_sf / lot_width if lot_width > 0 else 100
        
        # Calculate buildable area (accounting for setbacks)
        buildable_width = lot_width - (2 * self.zoning.setback_side)
        buildable_depth = lot_depth - self.zoning.setback_front - self.zoning.setback_rear
        buildable_area = max(0, buildable_width * buildable_depth)
        
        # Simple grid placement (placeholder for actual layout algorithm)
        lots_per_row = int(math.sqrt(count))
        
        for i in range(count):
            row = i // lots_per_row
            col = i % lots_per_row
            
            x = col * lot_width
            y = row * lot_depth
            
            corners = [
                (x, y),
                (x + lot_width, y),
                (x + lot_width, y + lot_depth),
                (x, y + lot_depth),
            ]
            
            lot = LotLayout(
                lot_number=i + 1,
                area_sf=avg_size_sf,
                width=lot_width,
                depth=lot_depth,
                corners=corners,
                frontage_road=f"Street {row + 1}",
                buildable_area_sf=buildable_area,
            )
            lots.append(lot)
        
        return lots
    
    def _create_lots_culdesac_pattern(self, count: int, avg_size_sf: float) -> List[LotLayout]:
        """Create lots in cul-de-sac pattern"""
        # Simplified - in production would create actual cul-de-sac geometry
        return self._create_lots_grid_pattern(count, avg_size_sf, self.zoning.min_lot_width * 1.1)
    
    def _calculate_area(self, points: List[Tuple[float, float]]) -> float:
        """Calculate polygon area using shoelace formula"""
        n = len(points)
        if n < 3:
            return 0.0
        
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        
        return abs(area) / 2.0
    
    def _estimate_road_length(self, lot_count: int) -> float:
        """Estimate total road length needed"""
        # Rough estimate: ~50 LF of road frontage per lot
        return lot_count * 50
    
    def _estimate_development_cost(self, lot_count: int) -> float:
        """Estimate total development cost"""
        # Simplified cost estimation
        road_length = self._estimate_road_length(lot_count)
        
        costs = {
            "roads": road_length * 180,  # $180/LF
            "utilities": lot_count * 15000,  # $15K per lot
            "site_prep": lot_count * 8000,  # $8K per lot
            "engineering": lot_count * 3000,  # $3K per lot
        }
        
        return sum(costs.values())
    
    def _get_zoning_requirements(self, designation: str) -> ZoningRequirements:
        """Get zoning requirements for designation"""
        # Simplified zoning requirements (would be loaded from database)
        zoning_db = {
            "R-1": ZoningRequirements(
                designation="R-1 Single Family Residential",
                min_lot_size_sf=8000,
                min_lot_width=60,
                min_lot_depth=100,
                max_density_units_per_acre=5.0,
                setback_front=25,
                setback_rear=20,
                setback_side=5,
                max_lot_coverage_percent=35,
                max_building_height=35,
            ),
            "R-2": ZoningRequirements(
                designation="R-2 Single Family Residential",
                min_lot_size_sf=10000,
                min_lot_width=70,
                min_lot_depth=120,
                max_density_units_per_acre=4.0,
                setback_front=30,
                setback_rear=25,
                setback_side=7,
                max_lot_coverage_percent=30,
                max_building_height=35,
            ),
            "PUD": ZoningRequirements(
                designation="Planned Unit Development",
                min_lot_size_sf=6000,
                min_lot_width=50,
                min_lot_depth=100,
                max_density_units_per_acre=6.0,
                setback_front=20,
                setback_rear=15,
                setback_side=5,
                max_lot_coverage_percent=40,
                max_building_height=45,
            ),
        }
        
        return zoning_db.get(designation, zoning_db["R-1"])
    
    def generate_comparison_report(self) -> str:
        """Generate comparison report of all layout options"""
        if not self.generated_options:
            return "No layout options generated yet."
        
        report = """
LAND LAYOUT OPTIONS COMPARISON
==============================

"""
        
        for i, option in enumerate(self.generated_options, 1):
            report += f"\nOPTION {i}: {option['option_name']}\n"
            report += "=" * (9 + len(option['option_name'])) + "\n"
            report += f"Description: {option['description']}\n"
            report += f"Lot Count: {option['lot_count']}\n"
            
            if 'average_lot_size_sf' in option:
                report += f"Average Lot Size: {option['average_lot_size_sf']:,.0f} SF\n"
            
            report += f"Estimated Cost: ${option['estimated_development_cost']:,.0f}\n"
            report += f"Projected Revenue: ${option['projected_revenue']:,.0f}\n"
            profit = option['projected_revenue'] - option['estimated_development_cost']
            report += f"Estimated Profit: ${profit:,.0f}\n"
            
            report += "\nPros:\n"
            for pro in option['pros']:
                report += f"  + {pro}\n"
            
            report += "\nCons:\n"
            for con in option['cons']:
                report += f"  - {con}\n"
            
            report += "\n" + "-" * 60 + "\n"
        
        return report
