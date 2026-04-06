"""
FORMATION INTELLIGENCE PLATFORM — GOVERNANCE LAYER
GovernanceLayer — Root Controller

Instantiates and wires all five governance services:
  1. CouncilOfMetanoia         — constitutional authority controller
  2. GovernanceAdjudicationEngine — judicial verdict engine
  3. DriftDetectionService     — deviation measurement and alert engine
  4. GovernanceRoutingTable    — governance signal dispatch registry
  5. GovernanceOverrideManager — exceptional override lifecycle manager

Inter-service dependency wiring (injection map):
  DriftDetectionService  ← GovernanceAdjudicationEngine  (alerts forwarded to adjudication)
  GovernanceAdjudicationEngine ← CouncilOfMetanoia       (verdicts forwarded to council)
  GovernanceAdjudicationEngine ← GovernanceRoutingTable  (verdicts routed via routing)
  CouncilOfMetanoia      ← GovernanceAdjudicationEngine  (contract enforcement routes to adj)
  CouncilOfMetanoia      ← GovernanceRoutingTable        (directives broadcast via routing)

Activation note:
  GovernanceLayer is NOT activated during STEP 15B. The platform holds
  `self.governance_layer = None` in main.py until STEP 15C.
  This controller is instantiated only in STEP 15C when the governance layer
  is wired into the FormationIntelligencePlatform and ICBus.

Authority: DOC-01.1 (Platform Governing Charter), DOC-01.2 (Constitutional Bylaws)
Version: 1.0
Status: TRUSTED — Cleared for Governance Layer Integration
"""

from __future__ import annotations
import datetime
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from config import PlatformConfig
    from logs.platform_logger import PlatformLogger

from .councils.council_of_metanoia import CouncilOfMetanoia
from .adjudication.governance_adjudication_engine import GovernanceAdjudicationEngine
from .drift_detection.drift_detection_service import DriftDetectionService
from .routing.governance_routing_table import GovernanceRoutingTable
from .overrides.governance_override_manager import GovernanceOverrideManager


class GovernanceLayer:
    """
    Root controller for the Formation Intelligence Platform Governance Layer.

    Instantiates all five governance services and wires cross-service references.
    Provides a single access point for the platform to interact with governance
    infrastructure.

    NOT ACTIVATED until STEP 15C. Until then, platform.governance_layer is None.

    STATUS: TRUSTED — Cleared for Governance Layer Integration
    """

    def __init__(self, config: "PlatformConfig", logger: "PlatformLogger",
                 platform: Optional[Any] = None):
        self.config = config
        self.logger = logger
        # Platform reference held for STEP 15C ICBus wiring
        self._platform = platform

        # ---------------------------------------------------------------
        # 1. Instantiate all five governance services
        # ---------------------------------------------------------------
        self.council = CouncilOfMetanoia(config, logger)
        self.adjudication = GovernanceAdjudicationEngine(config, logger)
        self.drift_detection = DriftDetectionService(config, logger)
        self.routing_table = GovernanceRoutingTable(config, logger)
        self.override_manager = GovernanceOverrideManager(config, logger)

        # ---------------------------------------------------------------
        # 2. Wire inter-service references
        #    Injection order chosen to avoid accessing a reference before
        #    the target object is fully initialized.
        # ---------------------------------------------------------------

        # DriftDetectionService → AdjudicationEngine
        #   Drift alerts above threshold are forwarded as violation signals.
        self.drift_detection.set_adjudication_engine(self.adjudication)

        # AdjudicationEngine → CouncilOfMetanoia
        #   Rendered verdicts are forwarded to the Council for directive issuance.
        self.adjudication.set_council(self.council)

        # AdjudicationEngine → GovernanceRoutingTable
        #   Verdicts are routed to target clusters via the routing table.
        self.adjudication.set_routing_table(self.routing_table)

        # CouncilOfMetanoia → AdjudicationEngine
        #   Contract enforcement requests are dispatched to the adjudication engine.
        self.council.set_adjudication_engine(self.adjudication)

        # CouncilOfMetanoia → GovernanceRoutingTable
        #   Platform-wide directives are broadcast via the routing table.
        self.council.set_routing_table(self.routing_table)

        logger.log(
            "GovernanceLayer initialized | services=5 | "
            "inter-service-wires=5 | status=NOT-ACTIVE (activation pending STEP 15C)"
        )

    # ------------------------------------------------------------------
    # Service accessors
    # ------------------------------------------------------------------

    @property
    def services(self) -> dict:
        """Return a dict of all five governance services by name."""
        return {
            "council":          self.council,
            "adjudication":     self.adjudication,
            "drift_detection":  self.drift_detection,
            "routing_table":    self.routing_table,
            "override_manager": self.override_manager,
        }

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    def health_check(self) -> dict:
        """
        Run a basic health check on all governance services.
        Validates routing table integrity and returns service readiness status.
        Returns health summary dict.
        """
        routing_validation = self.routing_table.validate_routing_table()

        # Verify all five injection wires are intact
        wire_status = {
            "drift→adjudication":  self.drift_detection._adjudication is self.adjudication,
            "adj→council":         self.adjudication._council is self.council,
            "adj→routing":         self.adjudication._routing_table is self.routing_table,
            "council→adjudication": self.council._adjudication is self.adjudication,
            "council→routing":     self.council._routing_table is self.routing_table,
        }
        wires_intact = all(wire_status.values())

        self.logger.log(
            f"GovernanceLayer.health_check | "
            f"routing_valid={routing_validation['valid']} | "
            f"active_routes={routing_validation['active_routes']} | "
            f"wires_intact={wires_intact}"
        )

        return {
            "status":             "READY" if (routing_validation["valid"] and wires_intact) else "DEGRADED",
            "routing_validation": routing_validation,
            "wire_status":        wire_status,
            "wires_intact":       wires_intact,
            "checked_at":         datetime.datetime.now(datetime.timezone.utc).isoformat(
                                      timespec="milliseconds").replace("+00:00", "Z"),
        }
