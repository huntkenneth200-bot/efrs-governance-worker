"""
FORMATION INTELLIGENCE PLATFORM
OBJ-10 — Hub Routing Record (re-export)

HubRoutingRecord is defined in formation_pathway.py.
This module re-exports it to satisfy the models package import contract.
"""
from .formation_pathway import HubRoutingRecord

__all__ = ["HubRoutingRecord"]
