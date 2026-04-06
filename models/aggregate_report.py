"""
FORMATION INTELLIGENCE PLATFORM
OBJ-12 — Aggregate Formation Report (re-export)

AggregateFormationReport is defined in formation_pathway.py.
This module re-exports it to satisfy the models package import contract.
"""
from .formation_pathway import AggregateFormationReport

__all__ = ["AggregateFormationReport"]
