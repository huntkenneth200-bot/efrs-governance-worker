"""
FORMATION INTELLIGENCE PLATFORM
OBJ-07 — Milestone Completion Record (re-export)

MilestoneCompletionRecord is defined in formation_pathway.py (co-located with
OBJ-06 FormationPathwayAssignment per their ownership relationship).
This module re-exports it to satisfy the models package import contract.
"""
from .formation_pathway import MilestoneCompletionRecord

__all__ = ["MilestoneCompletionRecord"]
