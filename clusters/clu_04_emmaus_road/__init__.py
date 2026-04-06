"""CLU-04 — Emmaus Road. Covenant community and hub operations. Authority: DOC-01.3, DOC-02.2"""
from .hub_formation_protocol import HubFormationProtocol
from .covenant_community_engine import CovenantCommunityEngine
from .household_rhythm_scheduler import HouseholdRhythmScheduler
from .hospitality_operations_module import HospitalityOperationsModule
from .local_church_interface import LocalChurchInterface
from .hub_health_assessment import HubHealthAssessmentModule

class EmmausRoad:
    def __init__(self, config, logger):
        self.hub_formation = HubFormationProtocol(config, logger)
        self.covenant_community = CovenantCommunityEngine(config, logger)
        self.rhythm_scheduler = HouseholdRhythmScheduler(config, logger)
        self.hospitality = HospitalityOperationsModule(config, logger)
        self.local_church = LocalChurchInterface(config, logger)
        self.hub_health = HubHealthAssessmentModule(config, logger)
        # IC-05 consumer: hub_formation, rhythm_scheduler (receives from CLU-01.5)
        # IC-13 producer: hub_health → CLU-02.1
        # IC-14 consumer: hub_formation (receives from CLU-06.6)
