"""
FORMATION INTELLIGENCE PLATFORM
CLU-01 — Restoration OS

Core formation operating system. Governs all individual fracture assessment,
stage progression, milestone tracking, blockage detection, pathway routing,
and restoration record management.

Authority: DOC-01.6, DOC-03.2, DOC-03.3
Submodules: 01.1 through 01.6
"""

from .fracture_assessment_engine import FractureAssessmentEngine
from .stage_progression_logic import StageProgressionLogic
from .milestone_tracking_system import MilestoneTrackingSystem
from .blockage_detection_module import BlockageDetectionModule
from .formation_pathway_router import FormationPathwayRouter
from .restoration_record_keeper import RestorationRecordKeeper


class RestorationOS:
    """
    CLU-01 cluster controller. Initializes all six submodules and
    registers their inter-submodule interface wiring.
    """

    def __init__(self, config, logger):
        self.fracture_engine = FractureAssessmentEngine(config, logger)
        self.stage_logic = StageProgressionLogic(config, logger)
        self.milestone_tracker = MilestoneTrackingSystem(config, logger)
        self.blockage_detector = BlockageDetectionModule(config, logger)
        self.pathway_router = FormationPathwayRouter(config, logger)
        self.record_keeper = RestorationRecordKeeper(config, logger)

        # TODO: Wire intra-cluster IC signals:
        # IC-01: fracture_engine → stage_logic, pathway_router
        # IC-02: fracture_engine → pathway_router
        # IC-03: milestone_tracker → stage_logic
        # IC-04: blockage_detector → stage_logic
        # IC-05: pathway_router → CLU-04 (external — wired at platform level)
        # IC-06: record_keeper → CLU-02.1, CLU-06.5 (external — wired at platform level)
