"""
FORMATION INTELLIGENCE PLATFORM
CLU-02 — Council of Metanoia

Supreme governing body. Holds theological review authority, constitutional
governance, operational oversight, amendment power, member accountability,
and external relationship management.

Authority: DOC-01.1, DOC-01.2
Submodules: 02.1 through 02.6
"""

from .governing_authority_module import GoverningAuthorityModule
from .theological_review_engine import TheologicalReviewEngine
from .council_operations_manager import CouncilOperationsManager
from .amendment_ruling_registry import AmendmentRulingRegistry
from .member_accountability_module import MemberAccountabilityModule
from .external_relations_interface import ExternalRelationsInterface


class CouncilOfMetanoia:
    """
    CLU-02 cluster controller. Initializes all six submodules.
    This cluster governs all other clusters — initialized first at platform level.
    """

    def __init__(self, config, logger):
        self.governing_authority = GoverningAuthorityModule(config, logger)
        self.theological_review = TheologicalReviewEngine(config, logger)
        self.operations_manager = CouncilOperationsManager(config, logger)
        self.ruling_registry = AmendmentRulingRegistry(config, logger)
        self.member_accountability = MemberAccountabilityModule(config, logger)
        self.external_relations = ExternalRelationsInterface(config, logger)

        # TODO: Wire IC signals:
        # IC-07 consumer: theological_review (receives from all clusters)
        # IC-08 producer: governing_authority (propagates to all clusters)
        # IC-13 consumer: governing_authority (receives hub health escalations)
