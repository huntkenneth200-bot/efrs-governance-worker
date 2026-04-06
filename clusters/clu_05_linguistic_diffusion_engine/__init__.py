"""CLU-05 — Linguistic Diffusion Engine. Language governance. Authority: DOC-01.5, DOC-03.1"""
from .semantic_authority_enforcer import SemanticAuthorityEnforcer
from .lexicon_management_system import LexiconManagementSystem
from .language_audit_module import LanguageAuditModule
from .formation_narrative_generator import FormationNarrativeGenerator
from .disqualified_language_filter import DisqualifiedLanguageFilter
from .external_communication_router import ExternalCommunicationRouter

class LinguisticDiffusionEngine:
    def __init__(self, config, logger):
        self.semantic_enforcer = SemanticAuthorityEnforcer(config, logger)
        self.lexicon_manager = LexiconManagementSystem(config, logger)
        self.language_auditor = LanguageAuditModule(config, logger)
        self.narrative_generator = FormationNarrativeGenerator(config, logger)
        self.disqualified_filter = DisqualifiedLanguageFilter(config, logger)
        self.external_router = ExternalCommunicationRouter(config, logger)
        # IC-11 producer: semantic_enforcer → all clusters
        # IC-12 producer: lexicon_manager → all clusters
