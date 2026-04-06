"""
FORMATION INTELLIGENCE PLATFORM
Governance Layer

Root package for the Platform Governance Layer. Provides the enforcement,
adjudication, drift detection, routing, and override infrastructure that
operates above cluster-level logic to maintain constitutional fidelity
across the full platform lifecycle.

Package structure:
    councils/        — Governance-layer representation of CouncilOfMetanoia authority
    contracts/       — Governance Contracts GC-01 through GC-07
    adjudication/    — GovernanceAdjudicationEngine
    drift_detection/ — DriftDetectionService
    routing/         — GovernanceRoutingTable
    overrides/       — GovernanceOverrideManager

Authority: DOC-01.1 (Platform Governing Charter), DOC-01.2 (Constitutional Bylaws)
Version: 1.0
Status: INSTALLED — Logic implemented (STEP 15B). Not yet activated. Activation pending STEP 15C.

Registration note:
    This package is imported by FormationIntelligencePlatform.__init__() as
    `self.governance_layer = None` — present in the initialization sequence
    but not instantiated until STEP 15C (Governance Layer Activation).
    To activate: self.governance_layer = GovernanceLayer(config, logger, platform=self)
"""

from .governance_layer import GovernanceLayer
from .councils.council_of_metanoia import CouncilOfMetanoia as GovernanceCouncil
from .adjudication.governance_adjudication_engine import GovernanceAdjudicationEngine
from .drift_detection.drift_detection_service import DriftDetectionService
from .routing.governance_routing_table import GovernanceRoutingTable
from .overrides.governance_override_manager import GovernanceOverrideManager

__all__ = [
    "GovernanceLayer",
    "GovernanceCouncil",
    "GovernanceAdjudicationEngine",
    "DriftDetectionService",
    "GovernanceRoutingTable",
    "GovernanceOverrideManager",
]
