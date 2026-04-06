"""
FORMATION INTELLIGENCE PLATFORM
OBJ-08 — Stage Progression Evaluation (re-export)

StageProgressionEvaluation is defined in formation_pathway.py.
This module re-exports it to satisfy the models package import contract.
"""
from .formation_pathway import StageProgressionEvaluation

__all__ = ["StageProgressionEvaluation"]
