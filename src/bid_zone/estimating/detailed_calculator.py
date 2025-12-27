"""
Detailed Construction Calculator
Handles all construction-specific calculations with industry-standard formulas
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class PavingCalculation:
    """Paving calculation results"""
    area_sf: float
    area_sy: float
    thickness_inches: float
    concrete_psi: int
    rebar_spec: str
    rebar_spacing: str
    concrete_volume_cy: float
    rebar_tonnage: float
    subgrade_treatment: str
    unit_cost_per_sy: float
    total_cost: float
    crew_days: float


@dataclass
class UtilityCalculation:
    """Utility line calculation results"""
    line_type: str
    diameter: str
    length_lf: float
    bedding_required: bool
    bedding_volume_cy: float
    excavation_volume_cy: float
    backfill_volume_cy: float
    crew_days: float
    daily_production_lf: float
    crew_cost_per_day: float
    total_cost: float


@dataclass
class EarthworkCalculation:
    """Earthwork calculation results"""
    cut_volume_cy: float
    fill_volume_cy: float
    net_cut_fill_cy: float
    swell_factor: float
    shrinkage_factor: float
    adjusted_cut_cy: float
    adjusted_fill_cy: float
    import_export_cy: float
    unit_cost_per_cy: float
    total_cost: float


@dataclass
class ConcreteCalculation:
    """Concrete calculation results"""
    element_type: str
    volume_cy: float
    area_sf: float
    thickness_inches: float
    psi_strength: int
    rebar_required: bool
    rebar_tonnage: float
    finish_type: str
    finishers_required: int
    pour_days: float
    batch_plant_type: str  # portable or truck
    daily_capacity_cy: float
    unit_cost_per_cy: float
    total_cost: float


class DetailedCalculator:
    """
    Performs detailed construction calculations with industry-standard formulas
    """
    
    def __init__(self):
        # Standard unit costs (can be overridden)
        self.concrete_cost_per_cy = 170.0  # $170/CY for 3000 PSI
        self.rebar_cost_per_ton = 950.0
        self.excavation_cost_per_cy = 15.0
        self.utility_crew_cost_per_day = 2500.0
        
        # Productivity rates
        self.finisher_production_sf_per_day = 300.0
        self.finisher_cost_per_day = 200.0
        self.utility_crew_production_lf_per_day = 700.0  # 600-800 LF average
        self.portable_batch_plant_capacity_cy_per_day = 1850.0  # 1700-2000
        self.truck_delivery_capacity_cy_per_day = 1000.0
        
        # Material properties
        self.concrete_density_pcf = 150.0
        self.rebar_spacing_map = {
            "16_oc": 16,
            "18_oc": 18,
            "12_oc": 12,
            "24_oc": 24,
        }
    
    def calculate_paving(
        self,
        area_sf: float,
        thickness_inches: float = 6.0,
        psi_strength: int = 3000,
        rebar_size: str = "#3",
        rebar_spacing: str = "16_oc",
        subgrade_treatment: str = "lime_stabilized"
    ) -> PavingCalculation:
        """
        Calculate detailed paving quantities and costs.
        
        Args:
            area_sf: Paving area in square feet
            thickness_inches: Slab thickness in inches
            psi_strength: Concrete PSI strength
            rebar_size: Rebar size (e.g., "#3", "#4")
            rebar_spacing: Rebar spacing (e.g., "16_oc" for 16" on center)
            subgrade_treatment: Subgrade treatment type
            
        Returns:
            PavingCalculation with all details
        """
        # Convert SF to SY
        area_sy = area_sf / 9.0
        
        # Calculate concrete volume
        # Volume = Area (SF) × Thickness (IN) / 12 / 27 = CY
        concrete_volume_cy = (area_sf * thickness_inches) / 12.0 / 27.0
        
        # Calculate rebar tonnage
        # Estimate: #3 rebar at 16" OC ≈ 0.015 tons/SY
        # Adjust based on spacing
        spacing_inches = self.rebar_spacing_map.get(rebar_spacing, 16)
        base_tonnage_per_sy = 0.015  # for 16" OC
        spacing_factor = 16.0 / spacing_inches
        rebar_tonnage = area_sy * base_tonnage_per_sy * spacing_factor
        
        # Adjust for rebar size
        if rebar_size == "#4":
            rebar_tonnage *= 1.5
        elif rebar_size == "#5":
            rebar_tonnage *= 2.0
        
        # Calculate costs
        concrete_cost = concrete_volume_cy * self.concrete_cost_per_cy
        rebar_cost = rebar_tonnage * self.rebar_cost_per_ton
        
        # Subgrade treatment cost
        subgrade_cost = 0
        if subgrade_treatment == "lime_stabilized":
            subgrade_cost = area_sy * 8.0  # $8/SY for lime stabilization
        
        # Forming and finishing
        forming_cost = area_sf * 0.50  # $0.50/SF for forming
        finishing_cost = area_sf * 1.50  # $1.50/SF for finishing
        
        total_cost = concrete_cost + rebar_cost + subgrade_cost + forming_cost + finishing_cost
        unit_cost_per_sy = total_cost / area_sy
        
        # Calculate crew days
        finishers_needed = max(1, int(area_sf / self.finisher_production_sf_per_day))
        crew_days = area_sf / self.finisher_production_sf_per_day / finishers_needed
        
        return PavingCalculation(
            area_sf=area_sf,
            area_sy=area_sy,
            thickness_inches=thickness_inches,
            concrete_psi=psi_strength,
            rebar_spec=f"{rebar_size} @ {rebar_spacing.replace('_', ' ')}",
            rebar_spacing=rebar_spacing,
            concrete_volume_cy=concrete_volume_cy,
            rebar_tonnage=rebar_tonnage,
            subgrade_treatment=subgrade_treatment,
            unit_cost_per_sy=unit_cost_per_sy,
            total_cost=total_cost,
            crew_days=crew_days
        )
    
    def calculate_utility_line(
        self,
        line_type: str,
        diameter: str,
        length_lf: float,
        depth_ft: float = 5.0,
        bedding_required: bool = True
    ) -> UtilityCalculation:
        """
        Calculate detailed utility line quantities and costs.
        
        Args:
            line_type: Type of utility (water, sewer, storm)
            diameter: Pipe diameter (e.g., "8\"")
            length_lf: Length in linear feet
            depth_ft: Average depth in feet
            bedding_required: Whether bedding is required
            
        Returns:
            UtilityCalculation with all details
        """
        # Parse diameter
        diameter_inches = float(diameter.replace('"', '').replace('in', ''))
        
        # Calculate trench volume for excavation
        # Typical trench width = diameter + 24" (12" each side)
        trench_width_ft = (diameter_inches + 24) / 12.0
        excavation_volume_cy = (length_lf * trench_width_ft * depth_ft) / 27.0
        
        # Calculate bedding volume if required
        bedding_volume_cy = 0
        if bedding_required:
            # Bedding: 6" under pipe
            bedding_volume_cy = (length_lf * trench_width_ft * 0.5) / 27.0
        
        # Calculate backfill volume
        # Pipe volume to subtract
        pipe_radius_ft = (diameter_inches / 12.0) / 2.0
        pipe_volume_cy = (length_lf * math.pi * pipe_radius_ft ** 2) / 27.0
        backfill_volume_cy = excavation_volume_cy - pipe_volume_cy - bedding_volume_cy
        
        # Calculate crew days
        crew_days = length_lf / self.utility_crew_production_lf_per_day
        
        # Calculate costs
        excavation_cost = excavation_volume_cy * self.excavation_cost_per_cy
        
        # Pipe cost (varies by type and diameter)
        pipe_cost_per_lf = {
            "water": {8: 45.0, 10: 55.0, 12: 65.0},
            "sewer": {8: 49.0, 10: 59.0, 12: 70.0},
            "storm": {15: 75.0, 18: 90.0, 24: 120.0}
        }
        
        diameter_int = int(diameter_inches)
        base_pipe_cost = pipe_cost_per_lf.get(line_type, {}).get(diameter_int, 50.0)
        pipe_cost = length_lf * base_pipe_cost
        
        # Bedding cost
        bedding_cost = bedding_volume_cy * 35.0  # $35/CY for bedding material
        
        # Backfill cost
        backfill_cost = backfill_volume_cy * 12.0  # $12/CY for backfill
        
        # Labor cost
        labor_cost = crew_days * self.utility_crew_cost_per_day
        
        total_cost = excavation_cost + pipe_cost + bedding_cost + backfill_cost + labor_cost
        
        return UtilityCalculation(
            line_type=line_type,
            diameter=diameter,
            length_lf=length_lf,
            bedding_required=bedding_required,
            bedding_volume_cy=bedding_volume_cy,
            excavation_volume_cy=excavation_volume_cy,
            backfill_volume_cy=backfill_volume_cy,
            crew_days=crew_days,
            daily_production_lf=self.utility_crew_production_lf_per_day,
            crew_cost_per_day=self.utility_crew_cost_per_day,
            total_cost=total_cost
        )
    
    def calculate_earthwork(
        self,
        cut_volume_cy: float,
        fill_volume_cy: float,
        soil_type: str = "silty_clay",
        region: str = "texas"
    ) -> EarthworkCalculation:
        """
        Calculate detailed earthwork with swell and shrinkage factors.
        
        Args:
            cut_volume_cy: Cut volume in cubic yards
            fill_volume_cy: Fill volume in cubic yards
            soil_type: Soil type for swell/shrinkage factors
            region: Region for geological considerations
            
        Returns:
            EarthworkCalculation with all details
        """
        # Swell and shrinkage factors by soil type
        soil_factors = {
            "silty_clay": {"swell": 1.25, "shrinkage": 0.90},
            "sandy_clay": {"swell": 1.20, "shrinkage": 0.92},
            "sand": {"swell": 1.12, "shrinkage": 0.95},
            "rock": {"swell": 1.50, "shrinkage": 1.00},
            "clay": {"swell": 1.30, "shrinkage": 0.88}
        }
        
        factors = soil_factors.get(soil_type, {"swell": 1.25, "shrinkage": 0.90})
        swell_factor = factors["swell"]
        shrinkage_factor = factors["shrinkage"]
        
        # Apply swell to cut (increases volume when removed)
        adjusted_cut_cy = cut_volume_cy * swell_factor
        
        # Apply shrinkage to fill (decreases volume when compacted)
        adjusted_fill_cy = fill_volume_cy / shrinkage_factor
        
        # Net import/export
        net_cut_fill_cy = cut_volume_cy - fill_volume_cy
        import_export_cy = adjusted_cut_cy - adjusted_fill_cy
        
        # Calculate costs
        cut_cost = cut_volume_cy * self.excavation_cost_per_cy
        fill_cost = fill_volume_cy * self.excavation_cost_per_cy
        
        # Import/export cost
        import_export_cost = 0
        if import_export_cy > 0:
            # Export (haul away)
            import_export_cost = abs(import_export_cy) * 8.0  # $8/CY haul
        else:
            # Import (bring in)
            import_export_cost = abs(import_export_cy) * 15.0  # $15/CY import
        
        total_cost = cut_cost + fill_cost + import_export_cost
        unit_cost_per_cy = total_cost / (cut_volume_cy + fill_volume_cy) if (cut_volume_cy + fill_volume_cy) > 0 else 0
        
        return EarthworkCalculation(
            cut_volume_cy=cut_volume_cy,
            fill_volume_cy=fill_volume_cy,
            net_cut_fill_cy=net_cut_fill_cy,
            swell_factor=swell_factor,
            shrinkage_factor=shrinkage_factor,
            adjusted_cut_cy=adjusted_cut_cy,
            adjusted_fill_cy=adjusted_fill_cy,
            import_export_cy=import_export_cy,
            unit_cost_per_cy=unit_cost_per_cy,
            total_cost=total_cost
        )
    
    def calculate_concrete_pour(
        self,
        element_type: str,
        volume_cy: float,
        area_sf: Optional[float] = None,
        thickness_inches: Optional[float] = None,
        psi_strength: int = 3000,
        batch_plant_type: str = "truck",
        rebar_required: bool = True
    ) -> ConcreteCalculation:
        """
        Calculate detailed concrete pour with productivity and scheduling.
        
        Args:
            element_type: Type (sidewalk, driveway, slab, footing)
            volume_cy: Concrete volume in cubic yards
            area_sf: Area in square feet (optional)
            thickness_inches: Thickness in inches (optional)
            psi_strength: PSI strength
            batch_plant_type: "truck" or "portable"
            rebar_required: Whether rebar is required
            
        Returns:
            ConcreteCalculation with all details
        """
        # Calculate area if not provided
        if area_sf is None and thickness_inches:
            area_sf = (volume_cy * 27 * 12) / thickness_inches
        elif area_sf is None:
            area_sf = 0
        
        # Calculate thickness if not provided
        if thickness_inches is None and area_sf > 0:
            thickness_inches = (volume_cy * 27 * 12) / area_sf
        elif thickness_inches is None:
            thickness_inches = 6.0  # default
        
        # Determine daily capacity
        if batch_plant_type == "portable":
            daily_capacity_cy = self.portable_batch_plant_capacity_cy_per_day
        else:
            daily_capacity_cy = self.truck_delivery_capacity_cy_per_day
        
        # Calculate pour days
        pour_days = volume_cy / daily_capacity_cy
        if pour_days < 0.5:
            pour_days = 0.5  # minimum half day
        
        # Calculate finishers required
        finishers_required = max(1, int(area_sf / self.finisher_production_sf_per_day)) if area_sf > 0 else 1
        
        # Calculate rebar tonnage if required
        rebar_tonnage = 0
        if rebar_required:
            # Estimate based on element type
            rebar_per_cy = {
                "footing": 0.10,  # 200 lbs/CY
                "slab": 0.08,     # 160 lbs/CY
                "sidewalk": 0.05, # 100 lbs/CY
                "driveway": 0.06, # 120 lbs/CY
            }
            rebar_tons_per_cy = rebar_per_cy.get(element_type, 0.08)
            rebar_tonnage = volume_cy * rebar_tons_per_cy
        
        # Calculate costs
        concrete_cost = volume_cy * self.concrete_cost_per_cy
        rebar_cost = rebar_tonnage * self.rebar_cost_per_ton if rebar_required else 0
        finishing_cost = area_sf * 1.50 if area_sf > 0 else 0
        forming_cost = area_sf * 0.50 if area_sf > 0 else 0
        
        total_cost = concrete_cost + rebar_cost + finishing_cost + forming_cost
        unit_cost_per_cy = total_cost / volume_cy if volume_cy > 0 else 0
        
        # Determine finish type
        finish_map = {
            "sidewalk": "Broom Finish",
            "driveway": "Broom Finish",
            "slab": "Steel Trowel",
            "footing": "Rough Screeded"
        }
        finish_type = finish_map.get(element_type, "Steel Trowel")
        
        return ConcreteCalculation(
            element_type=element_type,
            volume_cy=volume_cy,
            area_sf=area_sf,
            thickness_inches=thickness_inches,
            psi_strength=psi_strength,
            rebar_required=rebar_required,
            rebar_tonnage=rebar_tonnage,
            finish_type=finish_type,
            finishers_required=finishers_required,
            pour_days=pour_days,
            batch_plant_type=batch_plant_type,
            daily_capacity_cy=daily_capacity_cy,
            unit_cost_per_cy=unit_cost_per_cy,
            total_cost=total_cost
        )
    
    def calculate_weather_adjusted_schedule(
        self,
        base_duration_days: float,
        start_month: int,
        work_type: str = "general"
    ) -> Dict:
        """
        Adjust schedule for weather impacts.
        
        Args:
            base_duration_days: Base duration in days
            start_month: Starting month (1-12)
            work_type: Type of work
            
        Returns:
            Dict with adjusted schedule
        """
        # Weather productivity factors by month (for Texas/Southern US)
        # January and February are cold and rainy
        productivity_by_month = {
            1: 0.70,   # January - cold, rainy
            2: 0.70,   # February - cold, rainy
            3: 0.85,   # March - improving
            4: 0.95,   # April - good
            5: 0.95,   # May - good
            6: 0.90,   # June - hot
            7: 0.85,   # July - very hot
            8: 0.85,   # August - very hot
            9: 0.90,   # September - warm
            10: 0.95,  # October - excellent
            11: 0.95,  # November - excellent
            12: 0.85,  # December - cold
        }
        
        # Get productivity factor
        productivity = productivity_by_month.get(start_month, 0.90)
        
        # Adjust for work type
        if work_type == "concrete":
            # Concrete more affected by cold
            if start_month in [1, 2, 12]:
                productivity *= 0.90
        elif work_type == "earthwork":
            # Earthwork more affected by rain
            if start_month in [1, 2, 3]:
                productivity *= 0.85
        
        # Calculate adjusted duration
        adjusted_duration_days = base_duration_days / productivity
        lost_days = adjusted_duration_days - base_duration_days
        
        return {
            "base_duration_days": base_duration_days,
            "adjusted_duration_days": adjusted_duration_days,
            "productivity_factor": productivity,
            "lost_days": lost_days,
            "start_month": start_month,
            "weather_notes": self._get_weather_notes(start_month)
        }
    
    def _get_weather_notes(self, month: int) -> str:
        """Get weather notes for month"""
        notes = {
            1: "Cold and rainy conditions expected. Limited concrete pouring. High erosion risk.",
            2: "Cold and rainy conditions expected. Limited concrete pouring. High erosion risk.",
            3: "Improving weather but still wet conditions possible.",
            4: "Good working conditions expected.",
            5: "Excellent working conditions.",
            6: "Hot weather - concrete curing precautions required.",
            7: "Very hot weather - limit concrete pours to early morning.",
            8: "Very hot weather - limit concrete pours to early morning.",
            9: "Good working conditions.",
            10: "Excellent working conditions - optimal construction season.",
            11: "Excellent working conditions - optimal construction season.",
            12: "Cooling weather - concrete curing may require protection.",
        }
        return notes.get(month, "Normal working conditions expected.")
