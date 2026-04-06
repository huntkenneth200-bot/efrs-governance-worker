"""
FORMATION INTELLIGENCE PLATFORM
OBJ-15 — Ruling Propagation Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-15)
Owning cluster: CLU-02.1 — Governing Authority Module
Interface: IC-08 (Council Ruling Propagation)

Note: The RulingPropagationRecord dataclass is defined in council_ruling.py
(co-located with OBJ-14 CouncilRulingRecord per their 1:1 relationship).
This module re-exports it to satisfy the models package import contract.
"""

from .council_ruling import RulingPropagationRecord

__all__ = ["RulingPropagationRecord"]
