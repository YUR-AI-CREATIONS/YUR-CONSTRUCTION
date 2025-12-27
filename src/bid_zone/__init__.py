"""
BID-ZONE: Construction Estimating and Land Procurement Due Diligence Software
"""

__version__ = "1.0.0"
__author__ = "YUR AI CREATIONS"

from .land_procurement import (
    MarketAnalysis,
    FeasibilityStudy,
    EnvironmentalPhaseOne,
    FinancialProforma,
)
from .estimating import AIEstimator, DocumentProcessor, RiskAnalyzer
from .rendering import Renderer2D, Renderer3D, LandPlanner
from .earthwork import CutFillAnalyzer, GeotechProcessor
from .reports import ReportGenerator, SubmittalManager
