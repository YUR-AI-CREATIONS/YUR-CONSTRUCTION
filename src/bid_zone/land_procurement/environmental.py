"""
Environmental Phase One Assessment
Identifies potential environmental concerns for land development
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class SiteData:
    """Site information for environmental assessment"""
    address: str
    parcel_id: str
    total_acres: float
    current_use: str
    historical_uses: List[str]


class EnvironmentalPhaseOne:
    """
    Conducts Environmental Phase One assessments per ASTM E1527 standards.
    Identifies recognized environmental conditions (RECs).
    """
    
    def __init__(self):
        self.site_data: Optional[SiteData] = None
        
    def conduct_assessment(self, site_data: SiteData) -> Dict:
        """
        Conduct Environmental Phase One Assessment.
        
        Args:
            site_data: Site information and history
            
        Returns:
            Dict containing environmental assessment results
        """
        self.site_data = site_data
        
        assessment = {
            "assessment_date": datetime.now().isoformat(),
            "site_information": self._compile_site_info(),
            "records_review": self._conduct_records_review(),
            "site_reconnaissance": self._conduct_site_reconnaissance(),
            "historical_review": self._review_historical_use(),
            "regulatory_database_search": self._search_regulatory_databases(),
            "recognized_environmental_conditions": self._identify_recs(),
            "controlled_recognized_conditions": self._identify_crecs(),
            "historical_recognized_conditions": self._identify_hrecs(),
            "vapor_encroachment_screening": self._screen_vapor_encroachment(),
            "recommendations": self._generate_recommendations(),
            "phase_two_required": self._assess_phase_two_need(),
        }
        
        return assessment
    
    def _compile_site_info(self) -> Dict:
        """Compile basic site information"""
        if not self.site_data:
            return {}
            
        return {
            "address": self.site_data.address,
            "parcel_id": self.site_data.parcel_id,
            "total_acres": self.site_data.total_acres,
            "current_use": self.site_data.current_use,
            "historical_uses": self.site_data.historical_uses,
        }
    
    def _conduct_records_review(self) -> Dict:
        """Review environmental records"""
        return {
            "title_review_completed": True,
            "lien_search_completed": True,
            "environmental_liens_found": False,
            "activity_use_limitations": None,
            "deed_restrictions": None,
        }
    
    def _conduct_site_reconnaissance(self) -> Dict:
        """Conduct physical site inspection"""
        return {
            "inspection_date": datetime.now().strftime("%Y-%m-%d"),
            "site_observations": {
                "surface_staining": False,
                "stressed_vegetation": False,
                "drums_containers": False,
                "storage_tanks": {
                    "above_ground": False,
                    "underground": False,
                },
                "solid_waste": False,
                "wastewater_discharge": False,
            },
            "adjacent_property_observations": {
                "industrial_facilities": False,
                "gas_stations": True,
                "dry_cleaners": False,
                "auto_repair": False,
            },
            "terrain_observations": {
                "topography": "Gently sloping",
                "drainage": "Adequate",
                "wetlands_present": False,
                "water_bodies": False,
            },
        }
    
    def _review_historical_use(self) -> Dict:
        """Review historical site use"""
        return {
            "aerial_photos_reviewed": True,
            "years_reviewed": "1950-2024",
            "historical_findings": [
                {
                    "period": "1950-1980",
                    "use": "Agricultural - Row crops",
                    "concerns": None,
                },
                {
                    "period": "1980-2010",
                    "use": "Vacant land",
                    "concerns": None,
                },
                {
                    "period": "2010-Present",
                    "use": self.site_data.current_use if self.site_data else "Vacant",
                    "concerns": None,
                },
            ],
            "fire_insurance_maps_reviewed": True,
            "sanborn_maps_available": False,
        }
    
    def _search_regulatory_databases(self) -> Dict:
        """Search federal and state environmental databases"""
        return {
            "databases_searched": [
                "EPA NPL (National Priorities List)",
                "EPA CERCLIS",
                "EPA RCRA Info",
                "LUST (Leaking Underground Storage Tanks)",
                "State UST databases",
                "State waste sites",
                "Brownfield sites",
            ],
            "findings": {
                "site_listed": False,
                "adjacent_sites_listed": {
                    "count": 1,
                    "details": [
                        {
                            "name": "Former Gas Station",
                            "distance": "0.5 miles",
                            "database": "LUST",
                            "status": "Closed - No Further Action",
                        }
                    ],
                },
            },
            "search_radius_miles": 1.0,
        }
    
    def _identify_recs(self) -> List[Dict]:
        """Identify Recognized Environmental Conditions"""
        # No RECs identified in this example
        return []
    
    def _identify_crecs(self) -> List[Dict]:
        """Identify Controlled Recognized Environmental Conditions"""
        return []
    
    def _identify_hrecs(self) -> List[Dict]:
        """Identify Historical Recognized Environmental Conditions"""
        return []
    
    def _screen_vapor_encroachment(self) -> Dict:
        """Screen for vapor encroachment conditions"""
        return {
            "screening_performed": True,
            "tier_1_screening": "Complete",
            "vapor_concerns_identified": False,
            "recommendations": "No further vapor assessment needed",
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate environmental recommendations"""
        recs = self._identify_recs()
        
        if recs:
            return [
                "Phase Two Environmental Site Assessment recommended",
                "Address identified RECs before acquisition",
                "Consider environmental insurance",
                "Budget for potential remediation",
            ]
        else:
            return [
                "No RECs identified",
                "Site appears suitable for intended use",
                "Standard construction best practices recommended",
                "Maintain erosion and sediment control during development",
            ]
    
    def _assess_phase_two_need(self) -> bool:
        """Determine if Phase Two assessment is needed"""
        recs = self._identify_recs()
        crecs = self._identify_crecs()
        
        return len(recs) > 0 or len(crecs) > 0
    
    def generate_report(self, assessment: Dict) -> str:
        """Generate formatted Phase One ESA report"""
        report = f"""
ENVIRONMENTAL PHASE ONE ASSESSMENT
===================================
Date: {assessment['assessment_date']}

SITE INFORMATION:
Address: {assessment['site_information']['address']}
Parcel ID: {assessment['site_information']['parcel_id']}
Size: {assessment['site_information']['total_acres']} acres
Current Use: {assessment['site_information']['current_use']}

RECOGNIZED ENVIRONMENTAL CONDITIONS (RECs):
"""
        recs = assessment['recognized_environmental_conditions']
        if recs:
            for i, rec in enumerate(recs, 1):
                report += f"{i}. {rec.get('description', 'N/A')}\n"
        else:
            report += "None identified\n"
        
        report += f"""
PHASE TWO ASSESSMENT REQUIRED: {"Yes" if assessment['phase_two_required'] else "No"}

RECOMMENDATIONS:
"""
        for rec in assessment['recommendations']:
            report += f"- {rec}\n"
        
        return report
