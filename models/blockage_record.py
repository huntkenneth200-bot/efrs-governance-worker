"""
FORMATION INTELLIGENCE PLATFORM
OBJ-09 — Blockage Record

Schema authority: DATA-SCHEMA-REGISTRY.md (DSR-01 / OBJ-09)
Owning cluster: CLU-01.4 — Blockage Detection Module
Interface: IC-04 (Blockage → Stage Hold)
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from .enumerations import (
    BlockageType, BlockageSeverity, BlockageHoldStatus, EscalationStatus
)


@dataclass
class BlockageRecord:
    """
    Records a detected formation blockage for one participant.
    While hold_status = Active, stage advancement is blocked (IC-04).

    Constraints:
    - hold_status may not be Resolved without resolution_documentation (VR-09-01)
    - escalation_required must be True when blockage_type = SPIRITUAL (VR-09-02)
    - escalation_required must be True when blockage_severity = CRITICAL (VR-09-03)
    - advancement_blocked must remain True while hold_status = Active — not manually overridden (VR-09-04)
    - Records are permanent — status changes only
    """

    # System-generated
    blockage_id: UUID = field(default_factory=uuid4)
    detection_date: date = field(default_factory=date.today)
    resolution_date: Optional[date] = None

    # Ownership
    participant_id: Optional[UUID] = None
    facilitator_id: Optional[UUID] = None   # Detecting facilitator

    # Classification
    blockage_type: Optional[BlockageType] = None
    blockage_severity: Optional[BlockageSeverity] = None
    detection_trigger: Optional[str] = None  # Milestone-stall / Time-in-stage / Facilitator-submitted / Assessment-flag

    # Hold state
    hold_status: BlockageHoldStatus = BlockageHoldStatus.ACTIVE
    advancement_blocked: bool = True        # Always True while Active — not manually overridden (VR-09-04)

    # Escalation — auto-set based on type and severity (VR-09-02, VR-09-03)
    escalation_required: bool = False
    escalation_status: EscalationStatus = EscalationStatus.NOT_ESCALATED
    escalation_target: Optional[str] = None  # Hub-leader / Council

    # Documentation
    recommended_response: Optional[str] = None     # Protocol reference from DOC-02.1
    facilitator_review_notes: Optional[str] = None
    resolution_documentation: Optional[str] = None  # Required before Resolved (VR-09-01)

    def validate(self) -> list[str]:
        """
        Run all VR-09 validation rules.
        TODO: Implement per VR-09-01 through VR-09-06.
        """
        # TODO: VR-09-01 — Resolved requires resolution_documentation
        # TODO: VR-09-02 — escalation_required = True when SPIRITUAL
        # TODO: VR-09-03 — escalation_required = True when CRITICAL
        # TODO: VR-09-04 — advancement_blocked = True while Active (reject override)
        # TODO: VR-09-05 — escalation_status updated when escalation_required = True
        # TODO: VR-09-06 — escalation_target set correctly per type/severity
        errors = []
        return errors

    def evaluate_escalation_requirement(self):
        """
        System evaluates whether escalation is required based on type and severity.
        Auto-sets escalation_required. Called on creation and on type/severity change.
        TODO: Implement COCC-03 logic.
        """
        # TODO: If blockage_type == SPIRITUAL: escalation_required = True; target = Council
        # TODO: If blockage_severity == CRITICAL: escalation_required = True; target = Hub-leader
        # TODO: Log escalation_required determination
        pass

    def trigger_escalation(self):
        """
        Initiates escalation to the defined target.
        Called when escalation_required = True and escalation_status = NOT_ESCALATED.
        TODO: Route to ESC-B (Hub Leader) or ESC-C (Council) per escalation_target.
        """
        # TODO: Create escalation notification record
        # TODO: Update escalation_status = PENDING
        # TODO: Log escalation trigger (error FP-011 if SPIRITUAL and missed)
        pass

    def resolve(self, documentation: str, facilitator_id: UUID) -> bool:
        """
        Attempt to resolve the blockage hold.
        Requires resolution_documentation — will not resolve without it (VR-09-01).
        TODO: Implement resolution gate.
        """
        # TODO: Validate documentation present
        # TODO: Set resolution_documentation; hold_status = RESOLVED; resolution_date = today
        # TODO: Set advancement_blocked = False
        # TODO: Emit IC-04 clear signal to CLU-01.2
        # TODO: Log resolution with facilitator_id
        pass
