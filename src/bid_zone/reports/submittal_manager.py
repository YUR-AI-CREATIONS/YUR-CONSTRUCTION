"""
Submittal Manager
Manages construction submittals and shop drawings
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class SubmittalStatus(Enum):
    """Submittal status"""
    NOT_STARTED = "Not Started"
    IN_PREPARATION = "In Preparation"
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    APPROVED_AS_NOTED = "Approved as Noted"
    REJECTED = "Rejected - Resubmit"
    REVISE_AND_RESUBMIT = "Revise and Resubmit"


@dataclass
class Submittal:
    """Submittal item"""
    number: str
    title: str
    type: str  # Product Data, Shop Drawings, Samples, etc.
    specification_section: str
    required_date: datetime
    submitted_date: Optional[datetime]
    status: SubmittalStatus
    reviewer: str
    priority: str  # High, Medium, Low


class SubmittalManager:
    """
    Manages construction submittals and shop drawings.
    Generates submittal schedules and tracks status.
    """
    
    def __init__(self, project_name: str = "Untitled Project"):
        self.project_name = project_name
        self.submittals: List[Submittal] = []
        
    def generate_submittal_schedule(
        self,
        project_specs: Dict,
        project_schedule: Dict
    ) -> List[Submittal]:
        """
        Generate submittal schedule based on project specifications.
        
        Args:
            project_specs: Project specifications data
            project_schedule: Project schedule with milestones
            
        Returns:
            List of required submittals
        """
        # Clear existing
        self.submittals = []
        
        # Generate submittals for each major category
        self._generate_concrete_submittals(project_schedule)
        self._generate_rebar_submittals(project_schedule)
        self._generate_structural_steel_submittals(project_schedule)
        self._generate_earthwork_submittals(project_schedule)
        self._generate_utility_submittals(project_schedule)
        
        # Sort by required date
        self.submittals.sort(key=lambda x: x.required_date)
        
        return self.submittals
    
    def _generate_concrete_submittals(self, schedule: Dict):
        """Generate concrete-related submittals"""
        base_date = datetime.now()
        
        submittals = [
            Submittal(
                number="03-001",
                title="Concrete Mix Designs",
                type="Product Data",
                specification_section="03300",
                required_date=base_date + timedelta(days=30),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="High",
            ),
            Submittal(
                number="03-002",
                title="Admixture Product Data",
                type="Product Data",
                specification_section="03300",
                required_date=base_date + timedelta(days=35),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="Medium",
            ),
        ]
        
        self.submittals.extend(submittals)
    
    def _generate_rebar_submittals(self, schedule: Dict):
        """Generate rebar-related submittals"""
        base_date = datetime.now()
        
        submittals = [
            Submittal(
                number="03-100",
                title="Reinforcing Steel Shop Drawings",
                type="Shop Drawings",
                specification_section="03200",
                required_date=base_date + timedelta(days=45),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="High",
            ),
            Submittal(
                number="03-101",
                title="Rebar Mill Certificates",
                type="Product Data",
                specification_section="03200",
                required_date=base_date + timedelta(days=40),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="High",
            ),
        ]
        
        self.submittals.extend(submittals)
    
    def _generate_structural_steel_submittals(self, schedule: Dict):
        """Generate structural steel submittals"""
        base_date = datetime.now()
        
        submittals = [
            Submittal(
                number="05-001",
                title="Structural Steel Shop Drawings",
                type="Shop Drawings",
                specification_section="05120",
                required_date=base_date + timedelta(days=60),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="High",
            ),
            Submittal(
                number="05-002",
                title="Steel Mill Certificates",
                type="Product Data",
                specification_section="05120",
                required_date=base_date + timedelta(days=55),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="Medium",
            ),
            Submittal(
                number="05-003",
                title="Welding Procedures (WPS)",
                type="Shop Drawings",
                specification_section="05120",
                required_date=base_date + timedelta(days=50),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Structural Engineer",
                priority="High",
            ),
        ]
        
        self.submittals.extend(submittals)
    
    def _generate_earthwork_submittals(self, schedule: Dict):
        """Generate earthwork-related submittals"""
        base_date = datetime.now()
        
        submittals = [
            Submittal(
                number="31-001",
                title="Erosion Control Plan",
                type="Shop Drawings",
                specification_section="31200",
                required_date=base_date + timedelta(days=15),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Civil Engineer",
                priority="High",
            ),
            Submittal(
                number="31-002",
                title="Compaction Test Procedure",
                type="Product Data",
                specification_section="31200",
                required_date=base_date + timedelta(days=20),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Geotechnical Engineer",
                priority="High",
            ),
            Submittal(
                number="31-003",
                title="Fill Material Source and Testing",
                type="Product Data",
                specification_section="31200",
                required_date=base_date + timedelta(days=25),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Geotechnical Engineer",
                priority="Medium",
            ),
        ]
        
        self.submittals.extend(submittals)
    
    def _generate_utility_submittals(self, schedule: Dict):
        """Generate utility-related submittals"""
        base_date = datetime.now()
        
        submittals = [
            Submittal(
                number="33-001",
                title="Water Pipe Shop Drawings",
                type="Shop Drawings",
                specification_section="33100",
                required_date=base_date + timedelta(days=40),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Civil Engineer",
                priority="High",
            ),
            Submittal(
                number="33-002",
                title="Sewer Pipe Shop Drawings",
                type="Shop Drawings",
                specification_section="33300",
                required_date=base_date + timedelta(days=40),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Civil Engineer",
                priority="High",
            ),
            Submittal(
                number="33-003",
                title="Storm Drain Shop Drawings",
                type="Shop Drawings",
                specification_section="33400",
                required_date=base_date + timedelta(days=45),
                submitted_date=None,
                status=SubmittalStatus.NOT_STARTED,
                reviewer="Civil Engineer",
                priority="High",
            ),
        ]
        
        self.submittals.extend(submittals)
    
    def generate_shop_drawings_requirements(
        self,
        work_type: str
    ) -> Dict:
        """
        Generate shop drawing requirements for specific work types.
        
        Args:
            work_type: Type of work (rebar, steel, earthwork, etc.)
            
        Returns:
            Dict with shop drawing requirements
        """
        requirements = {
            "rebar": {
                "title": "Reinforcing Steel Shop Drawings",
                "required_items": [
                    "Bar schedules and bending diagrams",
                    "Placement drawings showing bar location",
                    "Lap splice and development length details",
                    "Mill certificates for rebar",
                    "Compliance with ASTM A615 Grade 60",
                ],
                "scale": "As noted, typically 1/4\" = 1'-0\"",
                "format": "PDF and CAD files",
                "copies_required": 5,
                "review_time_days": 14,
            },
            "structural_steel": {
                "title": "Structural Steel Shop Drawings",
                "required_items": [
                    "Erection drawings",
                    "Connection details",
                    "Member sizes and grades",
                    "Bolt and weld schedules",
                    "Mill certificates",
                    "Welding procedures (WPS)",
                ],
                "scale": "As noted, typically 1/4\" = 1'-0\"",
                "format": "PDF and CAD files",
                "copies_required": 5,
                "review_time_days": 21,
            },
            "earthwork": {
                "title": "Earthwork Shop Drawings",
                "required_items": [
                    "Erosion control details",
                    "Grading plan with limits of work",
                    "Cut/fill calculations",
                    "Haul routes",
                    "Compaction test locations",
                    "SWPPP documentation",
                ],
                "scale": "1\" = 20' or 1\" = 40'",
                "format": "PDF",
                "copies_required": 4,
                "review_time_days": 10,
            },
        }
        
        return requirements.get(work_type, {})
    
    def update_submittal_status(
        self,
        submittal_number: str,
        new_status: SubmittalStatus,
        comments: Optional[str] = None
    ) -> bool:
        """
        Update submittal status.
        
        Args:
            submittal_number: Submittal number to update
            new_status: New status
            comments: Optional comments
            
        Returns:
            True if updated successfully
        """
        for submittal in self.submittals:
            if submittal.number == submittal_number:
                submittal.status = new_status
                
                if new_status == SubmittalStatus.SUBMITTED:
                    submittal.submitted_date = datetime.now()
                
                return True
        
        return False
    
    def get_overdue_submittals(self) -> List[Submittal]:
        """Get list of overdue submittals"""
        today = datetime.now()
        
        overdue = [
            s for s in self.submittals
            if s.required_date < today and s.status not in [
                SubmittalStatus.APPROVED,
                SubmittalStatus.APPROVED_AS_NOTED
            ]
        ]
        
        return overdue
    
    def generate_submittal_log(self) -> str:
        """Generate submittal log report"""
        report = f"""
SUBMITTAL LOG
=============
Project: {self.project_name}
Date: {datetime.now().strftime('%Y-%m-%d')}

Total Submittals: {len(self.submittals)}
Approved: {len([s for s in self.submittals if s.status == SubmittalStatus.APPROVED])}
Pending: {len([s for s in self.submittals if s.status in [SubmittalStatus.SUBMITTED, SubmittalStatus.UNDER_REVIEW]])}
Overdue: {len(self.get_overdue_submittals())}

"""
        
        report += f"\n{'No':8} {'Title':40} {'Type':15} {'Required':12} {'Status':20}\n"
        report += "-" * 95 + "\n"
        
        for submittal in self.submittals:
            report += f"{submittal.number:8} "
            report += f"{submittal.title[:38]:40} "
            report += f"{submittal.type[:13]:15} "
            report += f"{submittal.required_date.strftime('%Y-%m-%d'):12} "
            report += f"{submittal.status.value:20}\n"
        
        # Show overdue items
        overdue = self.get_overdue_submittals()
        if overdue:
            report += "\n\nOVERDUE SUBMITTALS:\n"
            report += "=" * 95 + "\n"
            
            for submittal in overdue:
                days_overdue = (datetime.now() - submittal.required_date).days
                report += f"{submittal.number}: {submittal.title} - {days_overdue} days overdue\n"
        
        return report
    
    def export_to_format(self, filename: str, format_type: str = "csv") -> str:
        """
        Export submittal log to file.
        
        Args:
            filename: Output filename
            format_type: Export format
            
        Returns:
            Success message
        """
        if format_type == "csv":
            with open(filename, 'w') as f:
                # Header
                f.write("Number,Title,Type,Spec Section,Required Date,Status,Reviewer,Priority\n")
                
                # Data
                for s in self.submittals:
                    f.write(f"{s.number},")
                    f.write(f'"{s.title}",')
                    f.write(f"{s.type},")
                    f.write(f"{s.specification_section},")
                    f.write(f"{s.required_date.strftime('%Y-%m-%d')},")
                    f.write(f"{s.status.value},")
                    f.write(f"{s.reviewer},")
                    f.write(f"{s.priority}\n")
        
        return f"Submittal log exported to {filename}"
