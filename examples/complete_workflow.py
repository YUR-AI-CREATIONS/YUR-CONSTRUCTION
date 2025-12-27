"""
Example usage of BID-ZONE Land Procurement and Construction Estimation System
"""

from bid_zone.land_procurement import (
    MarketAnalysis,
    FeasibilityStudy,
    EnvironmentalPhaseOne,
    FinancialProforma,
)
from bid_zone.land_procurement.feasibility import ProjectParameters
from bid_zone.land_procurement.environmental import SiteData
from bid_zone.land_procurement.financial import DevelopmentAssumptions

from bid_zone.estimating import AIEstimator, DocumentProcessor, RiskAnalyzer
from bid_zone.rendering import Renderer2D, Renderer3D, LandPlanner
from bid_zone.earthwork import CutFillAnalyzer, GeotechProcessor
from bid_zone.reports import ReportGenerator, SubmittalManager


def example_land_procurement_workflow():
    """
    Example: Complete land procurement due diligence workflow
    """
    print("=" * 80)
    print("LAND PROCUREMENT DUE DILIGENCE EXAMPLE")
    print("=" * 80)
    
    # 1. Market Analysis
    print("\n1. Conducting Market Analysis...")
    market = MarketAnalysis()
    analysis = market.analyze_market(
        location="123 Development Way, Anytown, USA",
        radius_miles=3.0,
        property_type="residential"
    )
    print(market.generate_report(analysis))
    
    # 2. Feasibility Study
    print("\n2. Conducting Feasibility Study...")
    feasibility = FeasibilityStudy()
    params = ProjectParameters(
        total_acres=50.0,
        developable_acres=42.0,
        average_lot_size=0.25,  # acres
        estimated_lot_price=90000,
        acquisition_cost=2500000,
        development_cost_per_lot=25000,
        timeline_months=24,
    )
    study = feasibility.conduct_study(params, zoning="R-1", utilities_available=False)
    print(feasibility.generate_report(study))
    
    # 3. Environmental Phase One
    print("\n3. Conducting Environmental Phase One Assessment...")
    environmental = EnvironmentalPhaseOne()
    site_data = SiteData(
        address="123 Development Way",
        parcel_id="12-345-678",
        total_acres=50.0,
        current_use="Vacant agricultural",
        historical_uses=["Agricultural", "Vacant"],
    )
    assessment = environmental.conduct_assessment(site_data)
    print(environmental.generate_report(assessment))
    
    # 4. Financial Proforma
    print("\n4. Generating Financial Proforma...")
    proforma_gen = FinancialProforma()
    assumptions = DevelopmentAssumptions(
        land_cost=2500000,
        lots_count=168,
        lot_sale_price=90000,
        infrastructure_cost=3000000,
        site_prep_cost=500000,
        soft_costs_percent=15.0,
        contingency_percent=10.0,
        financing_rate=7.5,
        development_period_months=18,
        absorption_rate_lots_per_month=4.5,
    )
    proforma = proforma_gen.generate_proforma(assumptions)
    print(proforma_gen.generate_report(proforma))


def example_land_planning_workflow():
    """
    Example: Generate multiple land layout options
    """
    print("\n" + "=" * 80)
    print("LAND PLANNING EXAMPLE")
    print("=" * 80)
    
    planner = LandPlanner()
    
    # Define site boundary
    boundary = [
        (0, 0),
        (2000, 0),
        (2000, 1000),
        (0, 1000),
    ]
    
    # Generate layout options
    print("\nGenerating layout options based on zoning...")
    options = planner.generate_layout_options(
        boundary_points=boundary,
        zoning_designation="R-1",
        target_lot_count=None  # Let it calculate optimal
    )
    
    print(f"\nGenerated {len(options)} layout options:")
    for i, option in enumerate(options, 1):
        print(f"\nOption {i}: {option['option_name']}")
        print(f"  Lots: {option['lot_count']}")
        print(f"  Estimated Cost: ${option['estimated_development_cost']:,.0f}")
        print(f"  Projected Revenue: ${option['projected_revenue']:,.0f}")
    
    # Generate comparison report
    print("\n" + planner.generate_comparison_report())


def example_estimating_workflow():
    """
    Example: AI-powered estimating workflow
    """
    print("\n" + "=" * 80)
    print("AI-POWERED ESTIMATING EXAMPLE")
    print("=" * 80)
    
    # 1. Process documents
    print("\n1. Processing Construction Documents...")
    processor = DocumentProcessor()
    
    # Simulate processing a plan set
    # In production, this would actually read PDF files
    doc = processor.process_pdf("sample_plan.pdf")
    print(f"Processed: {doc.filename}")
    print(f"  Pages: {doc.pages}")
    print(f"  Tables detected: {len(doc.tables_detected)}")
    
    # 2. AI Estimating
    print("\n2. Running AI Vision Analysis...")
    estimator = AIEstimator()
    
    # Analyze document (using placeholder data)
    results = estimator.analyze_document(
        document_path="sample_plan.pdf",
        document_type="construction_plans",
        use_api="all"
    )
    
    print(f"Analysis complete using {len(results['analysis_results'])} AI APIs")
    print(f"Estimate items identified: {len(results['estimate_items'])}")
    
    # Generate estimate report
    print("\n" + estimator.generate_report())
    
    # 3. Risk Analysis
    print("\n3. Conducting Risk Analysis...")
    risk_analyzer = RiskAnalyzer()
    
    plan_data = {"documents": [doc]}
    risk_analysis = risk_analyzer.analyze_plans(plan_data)
    
    print(risk_analyzer.generate_report(risk_analysis))


def example_earthwork_workflow():
    """
    Example: Cut/fill analysis with geotech integration
    """
    print("\n" + "=" * 80)
    print("EARTHWORK & CUT/FILL ANALYSIS EXAMPLE")
    print("=" * 80)
    
    # 1. Process Geotech Report
    print("\n1. Processing Geotechnical Report...")
    geotech = GeotechProcessor()
    
    # Sample geotech data
    geotech_data = {
        "project_info": {"name": "Sample Development"},
        "borings": [
            {
                "id": "B-1",
                "location": (100, 100),
                "elevation": 850.0,
                "depth": 25.0,
                "layers": [
                    {
                        "depth_from": 0,
                        "depth_to": 3,
                        "soil_type": "Silty Clay",
                        "uscs": "CL",
                        "n_value": 8,
                    },
                    {
                        "depth_from": 3,
                        "depth_to": 25,
                        "soil_type": "Sandy Clay",
                        "uscs": "SC",
                        "n_value": 15,
                    },
                ],
                "groundwater_depth": None,
                "rock_depth": None,
            },
        ],
    }
    
    analysis = geotech.process_report(geotech_data)
    print(geotech.generate_report(analysis))
    
    # 2. Cut/Fill Analysis
    print("\n2. Analyzing Cut/Fill Quantities...")
    cutfill = CutFillAnalyzer()
    
    # Load elevations (sample data)
    existing = [(i * 10, j * 10, 850.0 + i * 0.1) for i in range(20) for j in range(20)]
    proposed = [(i * 10, j * 10, 850.0 + i * 0.05) for i in range(20) for j in range(20)]
    
    cutfill.load_existing_elevations(existing)
    cutfill.load_proposed_elevations(proposed)
    
    # Set soil properties from geotech
    from bid_zone.earthwork.cut_fill_analyzer import SoilProperties
    cutfill.soil_properties = SoilProperties(
        soil_type="Silty Clay",
        swell_factor=analysis["excavation_factors"]["swell_factor"],
        shrinkage_factor=analysis["excavation_factors"]["shrinkage_factor"],
        compaction_requirement=0.95,
    )
    
    cf_analysis = cutfill.analyze_cut_fill()
    print(cutfill.generate_report(cf_analysis))
    
    # Check for rock excavation
    rock_analysis = cutfill.identify_rock_excavation(geotech_data)
    if rock_analysis["rock_excavation_required"]:
        print(f"\nRock Excavation Required: {rock_analysis['total_rock_volume_cy']} CY")
        print(f"Estimated Cost: ${rock_analysis['total_estimated_cost']:,.0f}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "BID-ZONE COMPREHENSIVE DEMONSTRATION" + " " * 26 + "║")
    print("║" + " " * 10 + "Land Procurement & Construction Estimation System" + " " * 17 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        # Run all examples
        example_land_procurement_workflow()
        example_land_planning_workflow()
        example_estimating_workflow()
        example_earthwork_workflow()
        
        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()
