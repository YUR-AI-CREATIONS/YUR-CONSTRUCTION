"""
Report Generator
Generates professional reports and packages for estimates and analyses
"""

from typing import Dict, List, Optional
from datetime import datetime
import json


class ReportGenerator:
    """
    Generates comprehensive professional reports.
    Creates nicely formatted packages with itemized breakdowns by divisions.
    """
    
    def __init__(self, project_name: str = "Untitled Project"):
        self.project_name = project_name
        self.report_date = datetime.now()
        
    def generate_comprehensive_estimate_report(
        self,
        estimate_data: Dict,
        risk_analysis: Dict,
        project_details: Dict
    ) -> str:
        """
        Generate comprehensive estimate report with all sections.
        
        Args:
            estimate_data: Estimate data from AIEstimator
            risk_analysis: Risk analysis from RiskAnalyzer
            project_details: Project information
            
        Returns:
            Formatted report string
        """
        report = self._generate_cover_page(project_details)
        report += self._generate_executive_summary(estimate_data, risk_analysis)
        report += self._generate_estimate_by_division(estimate_data)
        report += self._generate_risk_summary(risk_analysis)
        report += self._generate_assumptions_and_exclusions()
        
        return report
    
    def _generate_cover_page(self, project_details: Dict) -> str:
        """Generate report cover page"""
        return f"""
{'=' * 80}
                    CONSTRUCTION ESTIMATE REPORT
{'=' * 80}

Project:        {project_details.get('name', self.project_name)}
Location:       {project_details.get('location', 'N/A')}
Owner:          {project_details.get('owner', 'N/A')}
Prepared By:    BID-ZONE Construction Estimating Software
Date:           {self.report_date.strftime('%B %d, %Y')}
Estimate #:     {project_details.get('estimate_number', 'EST-001')}

{'=' * 80}


"""
    
    def _generate_executive_summary(
        self,
        estimate_data: Dict,
        risk_analysis: Dict
    ) -> str:
        """Generate executive summary section"""
        totals = estimate_data.get("totals", {})
        grand_total = totals.get("grand_total", 0)
        
        return f"""
EXECUTIVE SUMMARY
=================

Total Estimated Cost:        ${grand_total:,.2f}

Project Scope:
This estimate covers all work shown on the construction documents including:
- Site work and earthwork
- Utilities installation
- Infrastructure improvements
- All materials, labor, and equipment

Risk Assessment:
Overall Risk Level:          {risk_analysis.get('risk_summary', {}).get('overall_risk_level', 'N/A')}
Identified Risks:            {risk_analysis.get('risk_summary', {}).get('total_risks_identified', 0)}
Recommended Contingency:     {risk_analysis.get('cost_impact', {}).get('recommended_contingency_percent', 15)}%

Schedule:
Estimated Duration:          18-24 months
Critical Path Items:         Permitting, Utilities, Paving


"""
    
    def _generate_estimate_by_division(self, estimate_data: Dict) -> str:
        """Generate detailed estimate breakdown by CSI division"""
        by_division = estimate_data.get("by_division", {})
        
        report = """
DETAILED ESTIMATE BY DIVISION
==============================

"""
        
        for division, items in sorted(by_division.items()):
            division_total = sum(item.get("total_price", 0) for item in items)
            
            report += f"\n{division}\n"
            report += "-" * 80 + "\n"
            report += f"{'Item':50} {'Qty':>12} {'Unit':>8} {'Unit $':>12} {'Total':>15}\n"
            report += "-" * 80 + "\n"
            
            for item in items:
                desc = item.get("description", "")[:48]
                qty = item.get("quantity", 0)
                unit = item.get("unit", "")
                unit_price = item.get("unit_price", 0)
                total = item.get("total_price", 0)
                
                report += f"{desc:50} {qty:12,.2f} {unit:>8} ${unit_price:11,.2f} ${total:14,.2f}\n"
            
            report += "-" * 80 + "\n"
            report += f"{'Division Subtotal:':50} {'':21} ${division_total:14,.2f}\n"
            report += "\n"
        
        grand_total = estimate_data.get("totals", {}).get("grand_total", 0)
        report += "=" * 80 + "\n"
        report += f"{'TOTAL ESTIMATED COST:':71} ${grand_total:14,.2f}\n"
        report += "=" * 80 + "\n\n"
        
        return report
    
    def _generate_risk_summary(self, risk_analysis: Dict) -> str:
        """Generate risk analysis summary section"""
        summary = risk_analysis.get("risk_summary", {})
        missing = risk_analysis.get("missing_items", [])
        
        report = """
RISK ANALYSIS
=============

Risk Level Summary:
"""
        
        for level, count in summary.get("risk_counts", {}).items():
            report += f"  {level:15} {count:3} items\n"
        
        report += f"\nOverall Risk Level: {summary.get('overall_risk_level', 'N/A')}\n\n"
        
        if missing:
            report += "Missing or Incomplete Items:\n"
            for item in missing[:10]:  # Show first 10
                report += f"  - {item.get('item', 'Unknown')} ({item.get('risk_level', 'N/A')})\n"
                report += f"    Reason: {item.get('reason', 'N/A')}\n"
        
        cost_impact = risk_analysis.get("cost_impact", {})
        report += f"\nEstimated Cost Impact:\n"
        report += f"  Expected: ${cost_impact.get('expected_impact', 0):,.0f}\n"
        report += f"  Range: ${cost_impact.get('minimum_impact', 0):,.0f} - "
        report += f"${cost_impact.get('maximum_impact', 0):,.0f}\n\n"
        
        return report
    
    def _generate_assumptions_and_exclusions(self) -> str:
        """Generate assumptions and exclusions section"""
        return """
ASSUMPTIONS AND EXCLUSIONS
==========================

Assumptions:
1. Quantities are based on plan takeoffs and may vary in field
2. Pricing is current as of estimate date
3. Normal working conditions and access
4. Work during normal business hours
5. No delays due to weather or permitting
6. Adequate utilities available at site
7. No contaminated materials or hazardous waste

Exclusions:
1. Building construction (if applicable)
2. Off-site improvements beyond project limits
3. Utility company connection fees
4. Permit fees and impact fees
5. Engineering and design fees
6. Testing and inspection services
7. Escalation beyond 6 months
8. Sales tax (unless otherwise noted)

Validity:
This estimate is valid for 60 days from estimate date.

Notes:
- All work per plans and specifications
- Contractor to verify all quantities in field
- Allowances included where quantities are unknown
- Contingency recommended for identified risks


"""
    
    def generate_land_development_proforma(
        self,
        proforma_data: Dict,
        market_analysis: Dict,
        feasibility: Dict
    ) -> str:
        """
        Generate comprehensive land development proforma report.
        
        Args:
            proforma_data: Financial proforma data
            market_analysis: Market analysis results
            feasibility: Feasibility study results
            
        Returns:
            Formatted proforma report
        """
        report = f"""
{'=' * 80}
                LAND DEVELOPMENT FINANCIAL PROFORMA
{'=' * 80}

Project:        {self.project_name}
Date:           {self.report_date.strftime('%B %d, %Y')}

{'=' * 80}


MARKET ANALYSIS SUMMARY
=======================

Market Strength:        {market_analysis.get('market_strength', 'N/A')}
Absorption Rate:        {market_analysis.get('absorption_rate', {}).get('lots_sold_per_month', 'N/A')} lots/month
Price Trend:            {market_analysis.get('price_trends', {}).get('12_month_trend', 'N/A')}


FINANCIAL SUMMARY
=================

Revenue Projection:
  Total Lots:           {proforma_data.get('project_assumptions', {}).get('development', {}).get('total_lots', 0)}
  Average Lot Price:    ${proforma_data.get('revenue_projection', {}).get('base_price_per_lot', 0):,.0f}
  Total Revenue:        ${proforma_data.get('revenue_projection', {}).get('escalated_revenue', 0):,.0f}

Cost Summary:
  Land Acquisition:     ${proforma_data.get('cost_breakdown', {}).get('land_acquisition', {}).get('subtotal', 0):,.0f}
  Hard Costs:           ${proforma_data.get('cost_breakdown', {}).get('hard_costs', {}).get('subtotal', 0):,.0f}
  Soft Costs:           ${proforma_data.get('cost_breakdown', {}).get('soft_costs', {}).get('subtotal', 0):,.0f}
  Contingency:          ${proforma_data.get('cost_breakdown', {}).get('contingency', 0):,.0f}
  Total Investment:     ${proforma_data.get('cost_breakdown', {}).get('total_investment', 0):,.0f}

Profitability:
  Gross Profit:         ${proforma_data.get('profit_analysis', {}).get('gross_profit', 0):,.0f}
  Profit Margin:        {proforma_data.get('profit_analysis', {}).get('profit_margin_percent', 0):.2f}%
  ROI:                  {proforma_data.get('profit_analysis', {}).get('return_on_investment_percent', 0):.2f}%
  Annualized Return:    {proforma_data.get('profit_analysis', {}).get('annualized_return_percent', 0):.2f}%

Feasibility:
  Rating:               {feasibility.get('feasibility_rating', 'N/A')}
  Recommendation:       {feasibility.get('go_no_go_recommendation', 'N/A')}
  Overall Risk:         {feasibility.get('risk_assessment', {}).get('overall_risk_rating', 'N/A')}


"""
        
        return report
    
    def export_to_pdf(self, report_content: str, filename: str) -> str:
        """
        Export report to PDF format (placeholder).
        
        Args:
            report_content: Report text content
            filename: Output filename
            
        Returns:
            Success message
        """
        # In production, would use reportlab or similar
        # For now, save as text file
        with open(filename.replace('.pdf', '.txt'), 'w') as f:
            f.write(report_content)
        
        return f"Report exported to {filename}"
    
    def export_to_excel(self, estimate_data: Dict, filename: str) -> str:
        """
        Export estimate to Excel format (placeholder).
        
        Args:
            estimate_data: Estimate data
            filename: Output filename
            
        Returns:
            Success message
        """
        # In production, would use openpyxl or xlsxwriter
        with open(filename.replace('.xlsx', '.json'), 'w') as f:
            json.dump(estimate_data, f, indent=2)
        
        return f"Estimate exported to {filename}"
    
    def generate_quick_summary(self, data: Dict, data_type: str) -> str:
        """
        Generate a quick one-page summary.
        
        Args:
            data: Data to summarize
            data_type: Type of data (estimate, proforma, analysis)
            
        Returns:
            Quick summary string
        """
        if data_type == "estimate":
            total = data.get("totals", {}).get("grand_total", 0)
            items = data.get("totals", {}).get("item_count", 0)
            
            return f"""
ESTIMATE QUICK SUMMARY
=====================
Total Cost: ${total:,.2f}
Line Items: {items}
Date: {self.report_date.strftime('%Y-%m-%d')}
"""
        
        elif data_type == "proforma":
            profit = data.get("profit_analysis", {}).get("gross_profit", 0)
            roi = data.get("profit_analysis", {}).get("return_on_investment_percent", 0)
            
            return f"""
PROFORMA QUICK SUMMARY
=====================
Estimated Profit: ${profit:,.2f}
ROI: {roi:.2f}%
Date: {self.report_date.strftime('%Y-%m-%d')}
"""
        
        return "Summary not available"
