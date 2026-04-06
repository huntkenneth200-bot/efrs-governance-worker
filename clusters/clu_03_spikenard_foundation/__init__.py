"""CLU-03 — Spikenard Foundation. Financial and stewardship governance. Authority: DOC-01.4"""
from .capital_source_integrity_filter import CapitalSourceIntegrityFilter
from .generative_giving_engine import GenerativeGivingEngine
from .stewardship_formation_module import StewardshipFormationModule
from .financial_integrity_reporting import FinancialIntegrityReporting
from .fund_allocation_logic import FundAllocationLogic
from .donor_relations_interface import DonorRelationsInterface

class SpikenardFoundation:
    def __init__(self, config, logger):
        self.integrity_filter = CapitalSourceIntegrityFilter(config, logger)
        self.giving_engine = GenerativeGivingEngine(config, logger)
        self.stewardship_formation = StewardshipFormationModule(config, logger)
        self.financial_reporting = FinancialIntegrityReporting(config, logger)
        self.fund_allocation = FundAllocationLogic(config, logger)
        self.donor_relations = DonorRelationsInterface(config, logger)
        # IC-09 producer: integrity_filter → giving_engine, CLU-06.1
        # IC-10 producer: fund_allocation → CLU-06.6
