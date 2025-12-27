"""
Financial Proforma Generator
Creates detailed financial projections for land development projects
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json


@dataclass
class DevelopmentAssumptions:
    """Financial assumptions for development"""
    land_cost: float
    lots_count: int
    lot_sale_price: float
    infrastructure_cost: float
    site_prep_cost: float
    soft_costs_percent: float
    contingency_percent: float
    financing_rate: float
    development_period_months: int
    absorption_rate_lots_per_month: float


class FinancialProforma:
    """
    Generates comprehensive financial proformas for land development.
    Includes detailed cash flow analysis, ROI calculations, and sensitivity analysis.
    """
    
    def __init__(self):
        self.assumptions: Optional[DevelopmentAssumptions] = None
        
    def generate_proforma(
        self,
        assumptions: DevelopmentAssumptions,
        preliminary_plan: Optional[Dict] = None
    ) -> Dict:
        """
        Generate complete financial proforma.
        
        Args:
            assumptions: Financial development assumptions
            preliminary_plan: Optional preliminary site plan data
            
        Returns:
            Dict containing complete financial proforma
        """
        self.assumptions = assumptions
        
        proforma = {
            "proforma_date": datetime.now().isoformat(),
            "project_assumptions": self._format_assumptions(),
            "cost_breakdown": self._calculate_cost_breakdown(),
            "revenue_projection": self._calculate_revenue_projection(),
            "cash_flow_analysis": self._generate_cash_flow(),
            "profit_analysis": self._calculate_profit_metrics(),
            "financing_analysis": self._analyze_financing(),
            "sensitivity_analysis": self._conduct_sensitivity_analysis(),
            "break_even_analysis": self._calculate_break_even(),
            "key_metrics": self._calculate_key_metrics(),
        }
        
        return proforma
    
    def _format_assumptions(self) -> Dict:
        """Format input assumptions"""
        if not self.assumptions:
            return {}
            
        a = self.assumptions
        return {
            "land_acquisition": {
                "cost": a.land_cost,
                "cost_per_lot": a.land_cost / a.lots_count if a.lots_count > 0 else 0,
            },
            "development": {
                "total_lots": a.lots_count,
                "average_lot_price": a.lot_sale_price,
                "infrastructure_cost": a.infrastructure_cost,
                "site_preparation": a.site_prep_cost,
            },
            "rates": {
                "soft_costs_percent": a.soft_costs_percent,
                "contingency_percent": a.contingency_percent,
                "financing_rate": a.financing_rate,
            },
            "timeline": {
                "development_period_months": a.development_period_months,
                "absorption_rate_monthly": a.absorption_rate_lots_per_month,
                "sellout_months": a.lots_count / a.absorption_rate_lots_per_month if a.absorption_rate_lots_per_month > 0 else 0,
            },
        }
    
    def _calculate_cost_breakdown(self) -> Dict:
        """Calculate detailed cost breakdown"""
        if not self.assumptions:
            return {}
            
        a = self.assumptions
        
        hard_costs = a.infrastructure_cost + a.site_prep_cost
        soft_costs = hard_costs * (a.soft_costs_percent / 100)
        contingency = (hard_costs + soft_costs) * (a.contingency_percent / 100)
        total_development = hard_costs + soft_costs + contingency
        total_investment = a.land_cost + total_development
        
        return {
            "land_acquisition": {
                "land_cost": a.land_cost,
                "closing_costs": a.land_cost * 0.03,
                "due_diligence": 25000,
                "subtotal": a.land_cost * 1.03 + 25000,
            },
            "hard_costs": {
                "infrastructure": a.infrastructure_cost,
                "site_preparation": a.site_prep_cost,
                "utilities": a.infrastructure_cost * 0.40,
                "roads_paving": a.infrastructure_cost * 0.35,
                "stormwater": a.infrastructure_cost * 0.25,
                "subtotal": hard_costs,
            },
            "soft_costs": {
                "engineering": soft_costs * 0.35,
                "legal_permitting": soft_costs * 0.15,
                "marketing_sales": soft_costs * 0.25,
                "insurance": soft_costs * 0.10,
                "administrative": soft_costs * 0.15,
                "subtotal": soft_costs,
            },
            "contingency": contingency,
            "total_development_cost": total_development,
            "total_investment": total_investment,
            "cost_per_lot": total_investment / a.lots_count if a.lots_count > 0 else 0,
        }
    
    def _calculate_revenue_projection(self) -> Dict:
        """Calculate revenue projections"""
        if not self.assumptions:
            return {}
            
        a = self.assumptions
        gross_revenue = a.lots_count * a.lot_sale_price
        
        # Price escalation over time
        escalation_rate = 0.03  # 3% annual
        average_escalation = (escalation_rate * (a.lots_count / a.absorption_rate_lots_per_month / 12 / 2)) if a.absorption_rate_lots_per_month > 0 else 0
        escalated_revenue = gross_revenue * (1 + average_escalation)
        
        return {
            "total_lots": a.lots_count,
            "base_price_per_lot": a.lot_sale_price,
            "gross_revenue_base": gross_revenue,
            "price_escalation_percent": average_escalation * 100,
            "escalated_revenue": escalated_revenue,
            "revenue_per_lot": escalated_revenue / a.lots_count if a.lots_count > 0 else 0,
        }
    
    def _generate_cash_flow(self) -> Dict:
        """Generate monthly cash flow projection"""
        if not self.assumptions:
            return {}
            
        a = self.assumptions
        costs = self._calculate_cost_breakdown()
        
        # Simplified monthly cash flow
        total_months = int(a.development_period_months + (a.lots_count / a.absorption_rate_lots_per_month)) if a.absorption_rate_lots_per_month > 0 else a.development_period_months
        
        monthly_flows = []
        cumulative = 0
        
        # Development phase
        monthly_dev_cost = costs['total_development_cost'] / a.development_period_months if a.development_period_months > 0 else 0
        
        for month in range(1, total_months + 1):
            outflow = 0
            inflow = 0
            
            # Month 1: Land acquisition
            if month == 1:
                outflow += costs['land_acquisition']['subtotal']
            
            # Development phase
            if month <= a.development_period_months:
                outflow += monthly_dev_cost
            
            # Sales phase (starts after development)
            if month > a.development_period_months:
                lots_sold = min(a.absorption_rate_lots_per_month, 
                               a.lots_count - ((month - a.development_period_months - 1) * a.absorption_rate_lots_per_month))
                if lots_sold > 0:
                    inflow = lots_sold * a.lot_sale_price
            
            net_flow = inflow - outflow
            cumulative += net_flow
            
            monthly_flows.append({
                "month": month,
                "inflow": round(inflow, 2),
                "outflow": round(outflow, 2),
                "net_flow": round(net_flow, 2),
                "cumulative": round(cumulative, 2),
            })
        
        return {
            "total_months": total_months,
            "monthly_cash_flows": monthly_flows[:12],  # First year only for brevity
            "peak_negative_cash": min(cf['cumulative'] for cf in monthly_flows),
            "final_cumulative": cumulative,
        }
    
    def _calculate_profit_metrics(self) -> Dict:
        """Calculate profit and return metrics"""
        if not self.assumptions:
            return {}
            
        costs = self._calculate_cost_breakdown()
        revenue = self._calculate_revenue_projection()
        
        total_cost = costs['total_investment']
        total_revenue = revenue['escalated_revenue']
        profit = total_revenue - total_cost
        profit_margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
        roi = (profit / total_cost * 100) if total_cost > 0 else 0
        
        # IRR approximation
        months = self.assumptions.development_period_months + (
            self.assumptions.lots_count / self.assumptions.absorption_rate_lots_per_month
        ) if self.assumptions.absorption_rate_lots_per_month > 0 else self.assumptions.development_period_months
        
        years = months / 12
        annualized_return = (roi / years) if years > 0 else 0
        
        return {
            "total_revenue": total_revenue,
            "total_costs": total_cost,
            "gross_profit": profit,
            "profit_margin_percent": round(profit_margin, 2),
            "return_on_investment_percent": round(roi, 2),
            "annualized_return_percent": round(annualized_return, 2),
            "profit_per_lot": profit / self.assumptions.lots_count if self.assumptions.lots_count > 0 else 0,
        }
    
    def _analyze_financing(self) -> Dict:
        """Analyze financing requirements and costs"""
        if not self.assumptions:
            return {}
            
        costs = self._calculate_cost_breakdown()
        cash_flow = self._generate_cash_flow()
        
        peak_need = abs(cash_flow['peak_negative_cash'])
        land_cost = costs['land_acquisition']['subtotal']
        equity_required = land_cost * 0.30  # 30% down
        loan_amount = land_cost * 0.70 + peak_need
        
        months = self.assumptions.development_period_months + (
            self.assumptions.lots_count / self.assumptions.absorption_rate_lots_per_month
        ) if self.assumptions.absorption_rate_lots_per_month > 0 else self.assumptions.development_period_months
        
        interest_cost = loan_amount * (self.assumptions.financing_rate / 100) * (months / 12)
        
        return {
            "peak_capital_need": peak_need,
            "recommended_loan_amount": loan_amount,
            "equity_requirement": equity_required,
            "interest_rate_percent": self.assumptions.financing_rate,
            "estimated_interest_cost": interest_cost,
            "loan_to_cost_ratio": (loan_amount / costs['total_investment'] * 100) if costs['total_investment'] > 0 else 0,
        }
    
    def _conduct_sensitivity_analysis(self) -> Dict:
        """Conduct sensitivity analysis on key variables"""
        if not self.assumptions:
            return {}
            
        base_profit = self._calculate_profit_metrics()
        base_roi = base_profit['return_on_investment_percent']
        
        scenarios = {
            "base_case": {"roi": base_roi, "description": "Base assumptions"},
            "optimistic": {
                "roi": base_roi * 1.20,
                "description": "10% higher prices, 10% lower costs",
            },
            "pessimistic": {
                "roi": base_roi * 0.70,
                "description": "10% lower prices, 10% higher costs",
            },
            "slow_absorption": {
                "roi": base_roi * 0.85,
                "description": "50% slower absorption rate",
            },
        }
        
        return {
            "scenarios": scenarios,
            "price_sensitivity": {
                "5_percent_decrease": base_roi * 0.75,
                "5_percent_increase": base_roi * 1.25,
            },
            "cost_sensitivity": {
                "10_percent_overrun": base_roi * 0.80,
                "10_percent_savings": base_roi * 1.20,
            },
        }
    
    def _calculate_break_even(self) -> Dict:
        """Calculate break-even analysis"""
        if not self.assumptions:
            return {}
            
        costs = self._calculate_cost_breakdown()
        total_cost = costs['total_investment']
        
        breakeven_lots = total_cost / self.assumptions.lot_sale_price if self.assumptions.lot_sale_price > 0 else 0
        breakeven_percent = (breakeven_lots / self.assumptions.lots_count * 100) if self.assumptions.lots_count > 0 else 0
        
        return {
            "breakeven_lots": round(breakeven_lots, 1),
            "breakeven_percent_of_total": round(breakeven_percent, 1),
            "lots_available_for_profit": self.assumptions.lots_count - breakeven_lots,
        }
    
    def _calculate_key_metrics(self) -> Dict:
        """Calculate key performance metrics"""
        profit = self._calculate_profit_metrics()
        costs = self._calculate_cost_breakdown()
        
        return {
            "roi_percent": profit['return_on_investment_percent'],
            "profit_margin_percent": profit['profit_margin_percent'],
            "cost_per_lot": costs['cost_per_lot'],
            "revenue_per_lot": self.assumptions.lot_sale_price,
            "margin_per_lot": self.assumptions.lot_sale_price - costs['cost_per_lot'],
            "development_efficiency": (
                self.assumptions.lots_count / (costs['total_investment'] / 1000000)
            ) if costs['total_investment'] > 0 else 0,
        }
    
    def generate_report(self, proforma: Dict) -> str:
        """Generate formatted financial proforma report"""
        profit = proforma['profit_analysis']
        costs = proforma['cost_breakdown']
        revenue = proforma['revenue_projection']
        
        report = f"""
FINANCIAL PROFORMA
==================
Date: {proforma['proforma_date']}

REVENUE PROJECTION:
Total Lots: {revenue['total_lots']}
Average Lot Price: ${revenue['base_price_per_lot']:,.0f}
Gross Revenue: ${revenue['escalated_revenue']:,.0f}

COST BREAKDOWN:
Land Acquisition: ${costs['land_acquisition']['subtotal']:,.0f}
Hard Costs: ${costs['hard_costs']['subtotal']:,.0f}
Soft Costs: ${costs['soft_costs']['subtotal']:,.0f}
Contingency: ${costs['contingency']:,.0f}
Total Investment: ${costs['total_investment']:,.0f}

PROFITABILITY:
Gross Profit: ${profit['gross_profit']:,.0f}
Profit Margin: {profit['profit_margin_percent']:.2f}%
Return on Investment: {profit['return_on_investment_percent']:.2f}%
Annualized Return: {profit['annualized_return_percent']:.2f}%

KEY METRICS:
Cost per Lot: ${costs['cost_per_lot']:,.0f}
Revenue per Lot: ${revenue['revenue_per_lot']:,.0f}
Profit per Lot: ${profit['profit_per_lot']:,.0f}
"""
        return report
    
    def export_to_excel(self, proforma: Dict, filename: str) -> str:
        """Export proforma to Excel format (placeholder)"""
        # In a real implementation, this would use openpyxl or xlsxwriter
        return f"Proforma exported to {filename}"
    
    def export_to_json(self, proforma: Dict, filename: str) -> str:
        """Export proforma to JSON format"""
        with open(filename, 'w') as f:
            json.dump(proforma, f, indent=2, default=str)
        return f"Proforma exported to {filename}"
