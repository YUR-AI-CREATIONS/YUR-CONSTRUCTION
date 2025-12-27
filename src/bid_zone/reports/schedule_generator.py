"""
Construction Schedule Generator
Generates industry-standard construction schedules with productivity rates and dependencies
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import math


class ActivityType(Enum):
    """Construction activity types"""
    MOBILIZATION = "Mobilization"
    EARTHWORK = "Earthwork"
    UTILITIES = "Utilities"
    CONCRETE = "Concrete"
    PAVING = "Paving"
    FINISHES = "Finishes"
    CLEANUP = "Cleanup"


@dataclass
class ScheduleActivity:
    """Schedule activity"""
    id: str
    name: str
    activity_type: ActivityType
    duration_days: float
    start_date: datetime
    end_date: datetime
    predecessors: List[str]
    crew_size: int
    daily_cost: float
    total_cost: float
    notes: str = ""


class ScheduleGenerator:
    """
    Generates construction schedules with proper sequencing,
    productivity rates, and weather adjustments.
    """
    
    def __init__(self, project_name: str = "Untitled Project"):
        self.project_name = project_name
        self.activities: List[ScheduleActivity] = []
        self.start_date: Optional[datetime] = None
        
        # Standard productivity rates
        self.productivity_rates = {
            "earthwork_cy_per_day": 500,
            "utility_lf_per_day": 700,
            "concrete_cy_per_day": 100,
            "paving_sy_per_day": 1500,
            "finisher_sf_per_day": 300,
        }
        
        # Weather adjustment factors
        self.weather_factors = {
            1: 0.70, 2: 0.70, 3: 0.85, 4: 0.95,
            5: 0.95, 6: 0.90, 7: 0.85, 8: 0.85,
            9: 0.90, 10: 0.95, 11: 0.95, 12: 0.85
        }
    
    def generate_schedule(
        self,
        project_data: Dict,
        start_date: Optional[datetime] = None
    ) -> List[ScheduleActivity]:
        """
        Generate comprehensive construction schedule.
        
        Args:
            project_data: Project quantities and scope
            start_date: Project start date
            
        Returns:
            List of schedule activities
        """
        self.start_date = start_date or datetime.now()
        self.activities = []
        
        current_date = self.start_date
        
        # 1. Mobilization
        mob_activity = self._create_mobilization_activity(current_date)
        self.activities.append(mob_activity)
        current_date = mob_activity.end_date
        
        # 2. Earthwork
        earthwork_data = project_data.get("earthwork", {})
        if earthwork_data:
            earthwork_activity = self._create_earthwork_activity(
                earthwork_data, current_date, [mob_activity.id]
            )
            self.activities.append(earthwork_activity)
            current_date = earthwork_activity.end_date
        
        # 3. Underground Utilities
        utilities_data = project_data.get("utilities", {})
        if utilities_data:
            utility_activities = self._create_utility_activities(
                utilities_data, current_date, [earthwork_activity.id] if earthwork_data else [mob_activity.id]
            )
            self.activities.extend(utility_activities)
            if utility_activities:
                current_date = utility_activities[-1].end_date
        
        # 4. Base preparation and paving
        paving_data = project_data.get("paving", {})
        if paving_data:
            paving_activities = self._create_paving_activities(
                paving_data, current_date, [a.id for a in utility_activities] if utilities_data else []
            )
            self.activities.extend(paving_activities)
            if paving_activities:
                current_date = paving_activities[-1].end_date
        
        # 5. Concrete work (sidewalks, driveways, etc.)
        concrete_data = project_data.get("concrete", {})
        if concrete_data:
            concrete_activities = self._create_concrete_activities(
                concrete_data, current_date, [a.id for a in paving_activities] if paving_data else []
            )
            self.activities.extend(concrete_activities)
            if concrete_activities:
                current_date = concrete_activities[-1].end_date
        
        # 6. Final grading and cleanup
        cleanup_activity = self._create_cleanup_activity(
            current_date, [self.activities[-1].id]
        )
        self.activities.append(cleanup_activity)
        
        return self.activities
    
    def _create_mobilization_activity(self, start_date: datetime) -> ScheduleActivity:
        """Create mobilization activity"""
        duration_days = 5.0
        end_date = start_date + timedelta(days=duration_days)
        
        return ScheduleActivity(
            id="MOB-001",
            name="Mobilization and Site Setup",
            activity_type=ActivityType.MOBILIZATION,
            duration_days=duration_days,
            start_date=start_date,
            end_date=end_date,
            predecessors=[],
            crew_size=5,
            daily_cost=2000.0,
            total_cost=2000.0 * duration_days,
            notes="Setup trailer, utilities, erosion control, fencing"
        )
    
    def _create_earthwork_activity(
        self,
        earthwork_data: Dict,
        start_date: datetime,
        predecessors: List[str]
    ) -> ScheduleActivity:
        """Create earthwork activity"""
        # Get quantities
        cut_cy = earthwork_data.get("cut_volume_cy", 0)
        fill_cy = earthwork_data.get("fill_volume_cy", 0)
        total_cy = cut_cy + fill_cy
        
        # Calculate duration
        base_duration = total_cy / self.productivity_rates["earthwork_cy_per_day"]
        
        # Apply weather factor
        weather_factor = self.weather_factors.get(start_date.month, 0.90)
        adjusted_duration = base_duration / weather_factor
        
        # Round up to whole days
        duration_days = math.ceil(adjusted_duration)
        end_date = self._add_working_days(start_date, duration_days)
        
        return ScheduleActivity(
            id="EW-001",
            name="Mass Grading and Earthwork",
            activity_type=ActivityType.EARTHWORK,
            duration_days=duration_days,
            start_date=start_date,
            end_date=end_date,
            predecessors=predecessors,
            crew_size=8,
            daily_cost=4500.0,
            total_cost=4500.0 * duration_days,
            notes=f"Cut: {cut_cy:,.0f} CY, Fill: {fill_cy:,.0f} CY. Weather factor: {weather_factor:.2f}"
        )
    
    def _create_utility_activities(
        self,
        utilities_data: Dict,
        start_date: datetime,
        predecessors: List[str]
    ) -> List[ScheduleActivity]:
        """Create utility installation activities"""
        activities = []
        current_date = start_date
        current_predecessors = predecessors.copy()
        
        # Water line
        if utilities_data.get("water_line_lf", 0) > 0:
            water_lf = utilities_data["water_line_lf"]
            duration = water_lf / self.productivity_rates["utility_lf_per_day"]
            duration_days = math.ceil(duration)
            end_date = self._add_working_days(current_date, duration_days)
            
            activity = ScheduleActivity(
                id="UT-001",
                name="Water Line Installation",
                activity_type=ActivityType.UTILITIES,
                duration_days=duration_days,
                start_date=current_date,
                end_date=end_date,
                predecessors=current_predecessors,
                crew_size=6,
                daily_cost=2500.0,
                total_cost=2500.0 * duration_days,
                notes=f"{water_lf:,.0f} LF water line. Crew production: 600-800 LF/day"
            )
            activities.append(activity)
            current_date = end_date
            current_predecessors = [activity.id]
        
        # Sewer line
        if utilities_data.get("sewer_line_lf", 0) > 0:
            sewer_lf = utilities_data["sewer_line_lf"]
            duration = sewer_lf / self.productivity_rates["utility_lf_per_day"]
            duration_days = math.ceil(duration)
            end_date = self._add_working_days(current_date, duration_days)
            
            activity = ScheduleActivity(
                id="UT-002",
                name="Sanitary Sewer Installation",
                activity_type=ActivityType.UTILITIES,
                duration_days=duration_days,
                start_date=current_date,
                end_date=end_date,
                predecessors=current_predecessors,
                crew_size=6,
                daily_cost=2500.0,
                total_cost=2500.0 * duration_days,
                notes=f"{sewer_lf:,.0f} LF sewer line. Crew production: 600-800 LF/day"
            )
            activities.append(activity)
            current_date = end_date
            current_predecessors = [activity.id]
        
        # Storm drain
        if utilities_data.get("storm_drain_lf", 0) > 0:
            storm_lf = utilities_data["storm_drain_lf"]
            duration = storm_lf / self.productivity_rates["utility_lf_per_day"]
            duration_days = math.ceil(duration)
            end_date = self._add_working_days(current_date, duration_days)
            
            activity = ScheduleActivity(
                id="UT-003",
                name="Storm Drain Installation",
                activity_type=ActivityType.UTILITIES,
                duration_days=duration_days,
                start_date=current_date,
                end_date=end_date,
                predecessors=current_predecessors,
                crew_size=6,
                daily_cost=2500.0,
                total_cost=2500.0 * duration_days,
                notes=f"{storm_lf:,.0f} LF storm drain. Crew production: 600-800 LF/day"
            )
            activities.append(activity)
        
        return activities
    
    def _create_paving_activities(
        self,
        paving_data: Dict,
        start_date: datetime,
        predecessors: List[str]
    ) -> List[ScheduleActivity]:
        """Create paving activities"""
        activities = []
        current_date = start_date
        current_predecessors = predecessors.copy()
        
        # Base preparation
        if paving_data.get("area_sy", 0) > 0:
            area_sy = paving_data["area_sy"]
            
            # Base prep (1-2 days per 1000 SY)
            base_duration = (area_sy / 1000.0) * 1.5
            base_days = math.ceil(base_duration)
            base_end = self._add_working_days(current_date, base_days)
            
            base_activity = ScheduleActivity(
                id="PV-001",
                name="Base Preparation and Compaction",
                activity_type=ActivityType.PAVING,
                duration_days=base_days,
                start_date=current_date,
                end_date=base_end,
                predecessors=current_predecessors,
                crew_size=6,
                daily_cost=3500.0,
                total_cost=3500.0 * base_days,
                notes=f"{area_sy:,.0f} SY base preparation. Includes lime stabilization."
            )
            activities.append(base_activity)
            current_date = base_end
            current_predecessors = [base_activity.id]
            
            # Paving
            paving_duration = area_sy / self.productivity_rates["paving_sy_per_day"]
            paving_days = math.ceil(paving_duration)
            paving_end = self._add_working_days(current_date, paving_days)
            
            thickness = paving_data.get("thickness_inches", 6)
            psi = paving_data.get("psi", 3000)
            
            paving_activity = ScheduleActivity(
                id="PV-002",
                name=f"Concrete Paving {thickness}\" @ {psi} PSI",
                activity_type=ActivityType.PAVING,
                duration_days=paving_days,
                start_date=current_date,
                end_date=paving_end,
                predecessors=current_predecessors,
                crew_size=8,
                daily_cost=5000.0,
                total_cost=5000.0 * paving_days,
                notes=f"{area_sy:,.0f} SY paving. Production: ~1500 SY/day. Weather dependent."
            )
            activities.append(paving_activity)
        
        return activities
    
    def _create_concrete_activities(
        self,
        concrete_data: Dict,
        start_date: datetime,
        predecessors: List[str]
    ) -> List[ScheduleActivity]:
        """Create concrete activities"""
        activities = []
        current_date = start_date
        current_predecessors = predecessors.copy()
        
        # Sidewalks
        if concrete_data.get("sidewalk_sf", 0) > 0:
            sidewalk_sf = concrete_data["sidewalk_sf"]
            duration = sidewalk_sf / self.productivity_rates["finisher_sf_per_day"]
            duration_days = math.ceil(duration)
            end_date = self._add_working_days(current_date, duration_days)
            
            activity = ScheduleActivity(
                id="CN-001",
                name="Sidewalk Installation",
                activity_type=ActivityType.CONCRETE,
                duration_days=duration_days,
                start_date=current_date,
                end_date=end_date,
                predecessors=current_predecessors,
                crew_size=4,
                daily_cost=1200.0,
                total_cost=1200.0 * duration_days,
                notes=f"{sidewalk_sf:,.0f} SF sidewalk. Finisher production: 300 SF/day/finisher"
            )
            activities.append(activity)
            current_date = end_date
            current_predecessors = [activity.id]
        
        # Driveways
        if concrete_data.get("driveway_sf", 0) > 0:
            driveway_sf = concrete_data["driveway_sf"]
            duration = driveway_sf / self.productivity_rates["finisher_sf_per_day"]
            duration_days = math.ceil(duration)
            end_date = self._add_working_days(current_date, duration_days)
            
            activity = ScheduleActivity(
                id="CN-002",
                name="Driveway Installation",
                activity_type=ActivityType.CONCRETE,
                duration_days=duration_days,
                start_date=current_date,
                end_date=end_date,
                predecessors=current_predecessors,
                crew_size=4,
                daily_cost=1200.0,
                total_cost=1200.0 * duration_days,
                notes=f"{driveway_sf:,.0f} SF driveways. Finisher production: 300 SF/day/finisher"
            )
            activities.append(activity)
        
        return activities
    
    def _create_cleanup_activity(
        self,
        start_date: datetime,
        predecessors: List[str]
    ) -> ScheduleActivity:
        """Create final cleanup activity"""
        duration_days = 3.0
        end_date = self._add_working_days(start_date, duration_days)
        
        return ScheduleActivity(
            id="CLN-001",
            name="Final Grading, Cleanup, and Punchlist",
            activity_type=ActivityType.CLEANUP,
            duration_days=duration_days,
            start_date=start_date,
            end_date=end_date,
            predecessors=predecessors,
            crew_size=4,
            daily_cost=1500.0,
            total_cost=1500.0 * duration_days,
            notes="Final grading, cleanup, demobilization, punchlist items"
        )
    
    def _add_working_days(self, start_date: datetime, days: float) -> datetime:
        """
        Add working days (skip weekends).
        
        Args:
            days: Number of working days to add (will be rounded up to nearest whole day)
        """
        current = start_date
        days_to_add = math.ceil(days)  # Round up fractional days
        days_added = 0
        
        while days_added < days_to_add:
            current += timedelta(days=1)
            # Skip weekends
            if current.weekday() < 5:  # Monday=0, Friday=4
                days_added += 1
        
        return current
    
    def generate_gantt_text(self) -> str:
        """Generate text-based Gantt chart"""
        if not self.activities:
            return "No schedule generated yet."
        
        report = f"""
CONSTRUCTION SCHEDULE - GANTT CHART
====================================
Project: {self.project_name}
Start Date: {self.start_date.strftime('%Y-%m-%d') if self.start_date else 'N/A'}
Total Duration: {self._calculate_total_duration()} days

"""
        
        # Header
        report += f"{'ID':10} {'Activity':40} {'Duration':10} {'Start':12} {'End':12} {'Cost':15}\n"
        report += "=" * 99 + "\n"
        
        # Activities
        for activity in self.activities:
            report += f"{activity.id:10} "
            report += f"{activity.name[:38]:40} "
            report += f"{activity.duration_days:8.1f} d "
            report += f"{activity.start_date.strftime('%Y-%m-%d'):12} "
            report += f"{activity.end_date.strftime('%Y-%m-%d'):12} "
            report += f"${activity.total_cost:13,.0f}\n"
            
            if activity.notes:
                report += f"{'':10} Note: {activity.notes}\n"
        
        # Summary
        total_cost = sum(a.total_cost for a in self.activities)
        report += "=" * 99 + "\n"
        report += f"{'':62} Total: ${total_cost:13,.0f}\n"
        
        return report
    
    def generate_critical_path(self) -> List[ScheduleActivity]:
        """Identify critical path activities"""
        # Simplified: activities with no float
        critical = []
        
        for i, activity in enumerate(self.activities):
            if i == 0 or i == len(self.activities) - 1:
                # First and last are always critical
                critical.append(activity)
            elif activity.duration_days > 5:
                # Long duration activities are likely critical
                critical.append(activity)
        
        return critical
    
    def _calculate_total_duration(self) -> int:
        """Calculate total project duration"""
        if not self.activities:
            return 0
        
        start = self.activities[0].start_date
        end = self.activities[-1].end_date
        
        return (end - start).days
    
    def export_to_csv(self, filename: str) -> str:
        """Export schedule to CSV"""
        with open(filename, 'w') as f:
            f.write("ID,Activity,Type,Duration (days),Start Date,End Date,Predecessors,Crew Size,Daily Cost,Total Cost,Notes\n")
            
            for activity in self.activities:
                f.write(f"{activity.id},")
                f.write(f'"{activity.name}",')
                f.write(f"{activity.activity_type.value},")
                f.write(f"{activity.duration_days},")
                f.write(f"{activity.start_date.strftime('%Y-%m-%d')},")
                f.write(f"{activity.end_date.strftime('%Y-%m-%d')},")
                f.write(f'"{";".join(activity.predecessors)}",')
                f.write(f"{activity.crew_size},")
                f.write(f"{activity.daily_cost},")
                f.write(f"{activity.total_cost},")
                f.write(f'"{activity.notes}"\n')
        
        return f"Schedule exported to {filename}"


import math

