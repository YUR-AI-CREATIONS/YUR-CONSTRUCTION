"""
Risk Analyzer
Identifies and quantifies risks based on missing or incomplete plan information
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """Risk severity levels"""
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"
    CRITICAL = "Critical"


@dataclass
class RiskItem:
    """Individual risk item"""
    category: str
    description: str
    level: RiskLevel
    impact: str
    mitigation: str
    cost_impact_range: tuple  # (min, max)


class RiskAnalyzer:
    """
    Analyzes construction plans for risks and missing information.
    Generates comprehensive risk summaries and mitigation strategies.
    """
    
    def __init__(self):
        self.identified_risks: List[RiskItem] = []
        
    def analyze_plans(self, plan_data: Dict) -> Dict:
        """
        Analyze construction plans for risks and missing items.
        
        Args:
            plan_data: Processed plan data from document processor
            
        Returns:
            Dict containing risk analysis results
        """
        analysis = {
            "analysis_date": "2024-12-27",
            "completeness_score": self._calculate_completeness(plan_data),
            "risks_by_category": self._categorize_risks(),
            "missing_items": self._identify_missing_items(plan_data),
            "risk_summary": self._generate_risk_summary(),
            "recommendations": self._generate_recommendations(),
            "cost_impact": self._calculate_cost_impact(),
        }
        
        return analysis
    
    def _calculate_completeness(self, plan_data: Dict) -> float:
        """
        Calculate plan completeness score (0-100).
        
        Args:
            plan_data: Plan data to analyze
            
        Returns:
            Completeness percentage
        """
        required_elements = [
            "site_plan",
            "grading_plan",
            "utility_plan",
            "detail_sheets",
            "specifications",
            "geotechnical_report",
            "environmental_report",
            "material_schedules",
            "quantity_takeoffs",
        ]
        
        # Check which elements are present
        present_count = 0
        
        # Simplified checking logic
        if plan_data.get("documents"):
            present_count = len(plan_data["documents"])
        
        completeness = (present_count / len(required_elements)) * 100
        return min(completeness, 100)  # Cap at 100%
    
    def _identify_missing_items(self, plan_data: Dict) -> List[Dict]:
        """
        Identify missing or incomplete plan items.
        
        Args:
            plan_data: Plan data to analyze
            
        Returns:
            List of missing items
        """
        missing = []
        
        # Check for required plan elements
        required_items = {
            "Geotechnical Report": {
                "category": "Site Investigation",
                "risk_level": RiskLevel.HIGH,
                "reason": "Required for earthwork quantities and foundation design",
            },
            "Environmental Phase I": {
                "category": "Environmental",
                "risk_level": RiskLevel.HIGH,
                "reason": "Required for site clearance and risk assessment",
            },
            "Utility Coordination": {
                "category": "Utilities",
                "risk_level": RiskLevel.MODERATE,
                "reason": "Conflicts may cause delays and cost overruns",
            },
            "Traffic Impact Study": {
                "category": "Regulatory",
                "risk_level": RiskLevel.MODERATE,
                "reason": "May be required by jurisdiction",
            },
            "Erosion Control Plan": {
                "category": "Environmental",
                "risk_level": RiskLevel.MODERATE,
                "reason": "Required for permit and compliance",
            },
            "Storm Water Calculations": {
                "category": "Design",
                "risk_level": RiskLevel.MODERATE,
                "reason": "Required for proper sizing of drainage system",
            },
        }
        
        # Simulate checking (in production, would actually parse plan_data)
        for item, details in required_items.items():
            # Add to missing list (in production, check if actually present)
            missing.append({
                "item": item,
                "category": details["category"],
                "risk_level": details["risk_level"].value,
                "reason": details["reason"],
            })
        
        return missing
    
    def _categorize_risks(self) -> Dict[str, List[RiskItem]]:
        """
        Categorize identified risks.
        
        Returns:
            Dict of risks organized by category
        """
        # Identify common construction risks
        self._identify_design_risks()
        self._identify_construction_risks()
        self._identify_schedule_risks()
        self._identify_cost_risks()
        
        categories = {}
        for risk in self.identified_risks:
            if risk.category not in categories:
                categories[risk.category] = []
            categories[risk.category].append(risk)
        
        return categories
    
    def _identify_design_risks(self):
        """Identify design-related risks"""
        risks = [
            RiskItem(
                category="Design",
                description="Incomplete geotechnical data",
                level=RiskLevel.HIGH,
                impact="Unknown soil conditions may affect earthwork costs",
                mitigation="Obtain complete geotechnical report with borings",
                cost_impact_range=(50000, 200000),
            ),
            RiskItem(
                category="Design",
                description="Missing structural calculations",
                level=RiskLevel.MODERATE,
                impact="Retaining walls may be under-designed",
                mitigation="Engineer to provide stamped structural calculations",
                cost_impact_range=(10000, 50000),
            ),
        ]
        self.identified_risks.extend(risks)
    
    def _identify_construction_risks(self):
        """Identify construction-related risks"""
        risks = [
            RiskItem(
                category="Construction",
                description="Utility conflicts not fully coordinated",
                level=RiskLevel.MODERATE,
                impact="Potential delays and redesign during construction",
                mitigation="Complete utility coordination and obtain clearances",
                cost_impact_range=(25000, 100000),
            ),
            RiskItem(
                category="Construction",
                description="Rock excavation not quantified",
                level=RiskLevel.HIGH,
                impact="Actual rock excavation may exceed budget",
                mitigation="Review geotechnical report and add rock allowance",
                cost_impact_range=(100000, 500000),
            ),
        ]
        self.identified_risks.extend(risks)
    
    def _identify_schedule_risks(self):
        """Identify schedule-related risks"""
        risks = [
            RiskItem(
                category="Schedule",
                description="Permit approval timeline uncertain",
                level=RiskLevel.MODERATE,
                impact="Project start may be delayed",
                mitigation="Engage with jurisdiction early, track permit progress",
                cost_impact_range=(20000, 80000),
            ),
        ]
        self.identified_risks.extend(risks)
    
    def _identify_cost_risks(self):
        """Identify cost-related risks"""
        risks = [
            RiskItem(
                category="Cost",
                description="Material cost escalation",
                level=RiskLevel.MODERATE,
                impact="Prices may increase before procurement",
                mitigation="Lock in pricing early, include escalation contingency",
                cost_impact_range=(30000, 150000),
            ),
        ]
        self.identified_risks.extend(risks)
    
    def _generate_risk_summary(self) -> Dict:
        """
        Generate summary of risk analysis.
        
        Returns:
            Risk summary dict
        """
        risk_counts = {
            "Critical": 0,
            "High": 0,
            "Moderate": 0,
            "Low": 0,
        }
        
        for risk in self.identified_risks:
            risk_counts[risk.level.value] += 1
        
        overall_risk = "Moderate"
        if risk_counts["Critical"] > 0 or risk_counts["High"] >= 3:
            overall_risk = "High"
        elif risk_counts["High"] == 0 and risk_counts["Moderate"] <= 2:
            overall_risk = "Low"
        
        return {
            "total_risks_identified": len(self.identified_risks),
            "risk_counts": risk_counts,
            "overall_risk_level": overall_risk,
            "highest_risk_items": [
                risk.description 
                for risk in self.identified_risks 
                if risk.level == RiskLevel.HIGH or risk.level == RiskLevel.CRITICAL
            ],
        }
    
    def _generate_recommendations(self) -> List[str]:
        """
        Generate risk mitigation recommendations.
        
        Returns:
            List of recommendations
        """
        recommendations = [
            "Obtain complete geotechnical report with adequate borings",
            "Complete utility coordination with all providers",
            "Add 15-20% contingency for identified risks",
            "Engage early with permitting authorities",
            "Consider design-build approach for high-risk items",
            "Obtain environmental clearances before starting work",
            "Lock in material pricing for long-lead items",
            "Develop detailed CPM schedule with float analysis",
        ]
        
        # Add specific recommendations based on identified risks
        for risk in self.identified_risks:
            if risk.level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                if risk.mitigation not in recommendations:
                    recommendations.append(risk.mitigation)
        
        return recommendations
    
    def _calculate_cost_impact(self) -> Dict:
        """
        Calculate potential cost impact of identified risks.
        
        Returns:
            Cost impact analysis
        """
        min_impact = sum(risk.cost_impact_range[0] for risk in self.identified_risks)
        max_impact = sum(risk.cost_impact_range[1] for risk in self.identified_risks)
        expected_impact = (min_impact + max_impact) / 2
        
        return {
            "minimum_impact": min_impact,
            "maximum_impact": max_impact,
            "expected_impact": expected_impact,
            "recommended_contingency_percent": 20.0,
            "by_category": self._calculate_category_impacts(),
        }
    
    def _calculate_category_impacts(self) -> Dict:
        """Calculate cost impacts by category"""
        category_impacts = {}
        
        for risk in self.identified_risks:
            if risk.category not in category_impacts:
                category_impacts[risk.category] = {
                    "min": 0,
                    "max": 0,
                }
            
            category_impacts[risk.category]["min"] += risk.cost_impact_range[0]
            category_impacts[risk.category]["max"] += risk.cost_impact_range[1]
        
        return category_impacts
    
    def generate_report(self, analysis: Dict) -> str:
        """
        Generate formatted risk analysis report.
        
        Args:
            analysis: Risk analysis data
            
        Returns:
            Formatted report string
        """
        report = """
RISK ANALYSIS REPORT
====================

"""
        
        report += f"Plan Completeness: {analysis['completeness_score']:.1f}%\n"
        report += f"Overall Risk Level: {analysis['risk_summary']['overall_risk_level']}\n"
        report += f"Total Risks Identified: {analysis['risk_summary']['total_risks_identified']}\n\n"
        
        report += "RISK BREAKDOWN:\n"
        for level, count in analysis['risk_summary']['risk_counts'].items():
            report += f"  {level}: {count}\n"
        
        report += "\n\nMISSING ITEMS:\n"
        for item in analysis['missing_items']:
            report += f"- {item['item']} ({item['risk_level']})\n"
            report += f"  Reason: {item['reason']}\n\n"
        
        report += "\nCOST IMPACT:\n"
        cost = analysis['cost_impact']
        report += f"Expected Cost Impact: ${cost['expected_impact']:,.0f}\n"
        report += f"Range: ${cost['minimum_impact']:,.0f} - ${cost['maximum_impact']:,.0f}\n"
        report += f"Recommended Contingency: {cost['recommended_contingency_percent']}%\n\n"
        
        report += "\nRECOMMENDATIONS:\n"
        for i, rec in enumerate(analysis['recommendations'], 1):
            report += f"{i}. {rec}\n"
        
        return report
