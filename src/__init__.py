"""
BID-ZONE: Enterprise Construction Estimating Platform

A comprehensive system for processing construction plans and generating
detailed cost estimates using AI-powered analysis.
"""

__version__ = "1.0.0"
__author__ = "YUR AI CREATIONS"

from .core.ingestion import FileIngestionSystem
from .core.chunking import DocumentChunker
from .core.oracle import OracleVerifier
from .core.nucleus import NucleusAggregator
from .agents.agent_framework import AgentFramework
from .interfaces.franklin_os import FranklinOS

__all__ = [
    'FileIngestionSystem',
    'DocumentChunker',
    'OracleVerifier',
    'NucleusAggregator',
    'AgentFramework',
    'FranklinOS'
]
