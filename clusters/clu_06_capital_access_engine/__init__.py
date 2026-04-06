"""CLU-06 — Capital Access Engine. Funding and capital development. Authority: DOC-01.4"""
from .funding_stream_manager import FundingStreamManager
from .grant_donor_pipeline import GrantDonorPipeline
from .kingdom_economics_module import KingdomEconomicsModule
from .sufficiency_standard_enforcer import SufficiencyStandardEnforcer
from .capital_reporting_interface import CapitalReportingInterface
from .deployment_funding_logic import DeploymentFundingLogic

class CapitalAccessEngine:
    def __init__(self, config, logger):
        self.stream_manager = FundingStreamManager(config, logger)
        self.grant_pipeline = GrantDonorPipeline(config, logger)
        self.kingdom_economics = KingdomEconomicsModule(config, logger)
        self.sufficiency_enforcer = SufficiencyStandardEnforcer(config, logger)
        self.capital_reporting = CapitalReportingInterface(config, logger)
        self.deployment_funding = DeploymentFundingLogic(config, logger)
        # IC-09 consumer: stream_manager, grant_pipeline (from CLU-03.1)
        # IC-10 consumer: deployment_funding (from CLU-03.5)
        # IC-14 producer: deployment_funding → CLU-04.1
