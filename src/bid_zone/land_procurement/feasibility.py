"""
Feasibility Study for Land Development
Analyzes project viability and financial feasibility
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta


@dataclass
class ProjectParameters:
    """Parameters for feasibility analysis"""
    total_acres: float
    developable_acres: float
    average_lot_size: float
    estimated_lot_price: float
    acquisition_cost: float
    development_cost_per_lot: float
    timeline_months: int


class FeasibilityStudy:
    """
    Conducts comprehensive feasibility studies for land development.
    Evaluates financial viability, regulatory constraints, and risk factors.
    """
    
    def __init__(self):
        self.parameters: Optional[ProjectParameters] = None
        
    def conduct_study(
        self,
        project_params: ProjectParameters,
        zoning: str,
        utilities_available: bool = False
    ) -> Dict:
        """
        Conduct comprehensive feasibility study.
        
        Args:
            project_params: Project parameters and financial assumptions
            zoning: Current zoning designation
            utilities_available: Whether utilities are available on site
            
        Returns:
            Dict containing feasibility analysis results
        """
        self.parameters = project_params
        
        study = {
            "study_date": datetime.now().isoformat(),
            "project_parameters": self._summarize_parameters(),
            "regulatory_analysis": self._analyze_regulatory(zoning),
            "infrastructure_analysis": self._analyze_infrastructure(utilities_available),
            "financial_feasibility": self._analyze_financial(),
            "schedule_analysis": self._analyze_schedule(),
            "risk_assessment": self._assess_risks(),
            "feasibility_rating": self._calculate_feasibility_rating(),
            "go_no_go_recommendation": self._generate_recommendation(),
        }
        
        return study
    
    def _summarize_parameters(self) -> Dict:
        """Summarize project parameters"""
        if not self.parameters:
            return {}
            
        p = self.parameters
        potential_lots = int(p.developable_acres / p.average_lot_size)
        
        return {
            "total_acres": p.total_acres,
            "developable_acres": p.developable_acres,
            "average_lot_size": p.average_lot_size,
            "potential_lots": potential_lots,
            "estimated_lot_price": p.estimated_lot_price,
            "acquisition_cost": p.acquisition_cost,
            "development_cost_per_lot": p.development_cost_per_lot,
            "timeline_months": p.timeline_months,
        }
    
    def _analyze_regulatory(self, zoning: str) -> Dict:
        """Analyze regulatory constraints"""
        return {
            "current_zoning": zoning,
            "zoning_compatible": True,
            "rezoning_required": False,
            "environmental_permits_needed": [
                "Stormwater Management",
                "Erosion Control",
                "Wetland Delineation",
            ],
            "estimated_approval_time_months": 6,
            "regulatory_risk": "Low to Moderate",
        }
    
    def _analyze_infrastructure(self, utilities_available: bool) -> Dict:
        """Analyze infrastructure requirements"""
        return {
            "utilities_available": utilities_available,
            "required_improvements": {
                "roads": "Internal road network required",
                "water": "Extension from main required" if not utilities_available else "Available",
                "sewer": "Connection to municipal system" if not utilities_available else "Available",
                "electric": "Overhead extension required",
                "gas": "Main line available",
                "stormwater": "Detention pond and system required",
            },
            "estimated_infrastructure_cost": 1200000 if not utilities_available else 800000,
            "off_site_improvements": "Traffic signal contribution may be required",
        }
    
    def _analyze_financial(self) -> Dict:
        """Analyze financial feasibility"""
        if not self.parameters:
            return {}
            
        p = self.parameters
        potential_lots = int(p.developable_acres / p.average_lot_size)
        gross_revenue = potential_lots * p.estimated_lot_price
        total_development_cost = potential_lots * p.development_cost_per_lot
        total_cost = p.acquisition_cost + total_development_cost
        profit = gross_revenue - total_cost
        profit_margin = (profit / gross_revenue * 100) if gross_revenue > 0 else 0
        roi = (profit / total_cost * 100) if total_cost > 0 else 0
        
        return {
            "potential_lots": potential_lots,
            "gross_revenue": gross_revenue,
            "acquisition_cost": p.acquisition_cost,
            "development_cost": total_development_cost,
            "total_investment": total_cost,
            "estimated_profit": profit,
            "profit_margin_percent": round(profit_margin, 2),
            "roi_percent": round(roi, 2),
            "breakeven_lots": int(total_cost / p.estimated_lot_price) if p.estimated_lot_price > 0 else 0,
        }
    
    def _analyze_schedule(self) -> Dict:
        """Analyze project schedule"""
        if not self.parameters:
            return {}
            
        start_date = datetime.now()
        
        milestones = [
            {"phase": "Due Diligence", "duration_months": 3},
            {"phase": "Permitting", "duration_months": 6},
            {"phase": "Infrastructure", "duration_months": 8},
            {"phase": "Lot Development", "duration_months": 6},
            {"phase": "Sales/Marketing", "duration_months": self.parameters.timeline_months},
        ]
        
        current_date = start_date
        schedule = []
        
        for milestone in milestones:
            end_date = current_date + timedelta(days=milestone["duration_months"] * 30)
            schedule.append({
                "phase": milestone["phase"],
                "start": current_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "duration_months": milestone["duration_months"],
            })
            current_date = end_date
            
        return {
            "project_start": start_date.strftime("%Y-%m-%d"),
            "estimated_completion": current_date.strftime("%Y-%m-%d"),
            "total_duration_months": sum(m["duration_months"] for m in milestones),
            "milestones": schedule,
        }
    
    def _assess_risks(self) -> Dict:
        """Assess project risks"""
        return {
            "market_risk": {
                "level": "Moderate",
                "factors": [
                    "Interest rate fluctuations",
                    "Builder demand changes",
                    "Economic downturn",
                ],
            },
            "regulatory_risk": {
                "level": "Low",
                "factors": [
                    "Permit delays",
                    "Zoning changes",
                    "Environmental issues",
                ],
            },
            "construction_risk": {
                "level": "Moderate",
                "factors": [
                    "Weather delays",
                    "Material cost escalation",
                    "Labor availability",
                ],
            },
            "financial_risk": {
                "level": "Low to Moderate",
                "factors": [
                    "Cost overruns",
                    "Slower absorption",
                    "Price competition",
                ],
            },
            "overall_risk_rating": "Moderate",
        }
    
    def _calculate_feasibility_rating(self) -> str:
        """Calculate overall feasibility rating"""
        financial = self._analyze_financial()
        
        if not financial:
            return "Insufficient Data"
            
        roi = financial.get("roi_percent", 0)
        profit_margin = financial.get("profit_margin_percent", 0)
        
        if roi >= 25 and profit_margin >= 20:
            return "Highly Feasible"
        elif roi >= 15 and profit_margin >= 15:
            return "Feasible"
        elif roi >= 10 and profit_margin >= 10:
            return "Marginally Feasible"
        else:
            return "Not Feasible"
    
    def _generate_recommendation(self) -> str:
        """Generate go/no-go recommendation"""
        rating = self._calculate_feasibility_rating()
        
        if rating in ["Highly Feasible", "Feasible"]:
            return "GO - Proceed with acquisition"
        elif rating == "Marginally Feasible":
            return "CONDITIONAL - Renegotiate terms or optimize design"
        else:
            return "NO-GO - Seek alternative opportunities"
    
    def generate_report(self, study: Dict) -> str:
        """Generate formatted feasibility study report"""
        report = f"""
FEASIBILITY STUDY REPORT
========================
Date: {study['study_date']}

PROJECT PARAMETERS:
"""
        params = study['project_parameters']
        for key, value in params.items():
            report += f"  {key.replace('_', ' ').title()}: {value}\n"
        
        report += f"""
FINANCIAL ANALYSIS:
"""
        financial = study['financial_feasibility']
        for key, value in financial.items():
            report += f"  {key.replace('_', ' ').title()}: {value}\n"
        
        report += f"""
FEASIBILITY RATING: {study['feasibility_rating']}
RECOMMENDATION: {study['go_no_go_recommendation']}

OVERALL RISK: {study['risk_assessment']['overall_risk_rating']}
"""
        return report
