"""
FORMATION INTELLIGENCE PLATFORM
OBJ-13 — Theological Review Record (re-export)

TheologicalReviewRecord is defined in formation_pathway.py.
This module re-exports it to satisfy the models package import contract.
"""
from .formation_pathway import TheologicalReviewRecord

__all__ = ["TheologicalReviewRecord"]
