"""
FORMATION INTELLIGENCE PLATFORM
Interface Contract Bus (ICBus)

Central message bus wiring all 14 Interface Contracts (IC-01 through IC-14)
between cluster submodules. ICBus is the only layer permitted to call
cross-cluster receive methods. No cluster submodule may call another
cluster's submodule directly.

Architecture:
  - Each emit_ic_XX() method packages the payload (from ic_payloads.py)
    and dispatches to all registered consumers for that IC.
  - Broadcast ICs (IC-08, IC-11, IC-12) maintain a subscriber list and
    dispatch to all subscribers via a loop.
  - Point-to-point ICs call the single designated receive method directly.
  - Where a TRUSTED submodule has no explicit receive method, a stub from
    ic_integration_stubs.py is registered instead.

Authority: ICM-01
Version: 1.0
Status: WIRED — Step 10 IC Integration

Amendment: Any change to routing logic requires ICM-01 amendment under
Council ruling (DOC-01.2).
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Callable
from uuid import UUID
from datetime import date

from ic_payloads import (
    IC01Payload, IC02Payload, IC03Payload,
    IC04HoldPayload, IC04ClearPayload,
    IC05Payload, IC06GovernancePayload, IC06CapitalPayload,
    IC07Payload, IC08Payload, IC09Payload, IC10Payload,
    IC11Payload, IC12Payload, IC13Payload, IC14Payload,
)
from ic_integration_stubs import (
    ic_01_stage_progression_stub,
    ic_01_pathway_router_stub,
    ic_05_hospitality_stub,
    ic_06_capital_stub,
    build_ic08_subscribers,
    build_ic11_subscribers,
    build_ic12_subscribers,
)

if TYPE_CHECKING:
    from clusters.clu_01_restoration_os import RestorationOS
    from clusters.clu_02_council_of_metanoia import CouncilOfMetanoia
    from clusters.clu_03_spikenard_foundation import SpikenardFoundation
    from clusters.clu_04_emmaus_road import EmmausRoad
    from clusters.clu_05_linguistic_diffusion_engine import LinguisticDiffusionEngine
    from clusters.clu_06_capital_access_engine import CapitalAccessEngine


class ICBus:
    """
    Interface Contract Bus.

    Instantiated once by FormationIntelligencePlatform.__init__() after all
    six cluster instances are created. Holds references to every cluster and
    builds the broadcast subscriber lists for IC-08, IC-11, and IC-12.

    Usage:
        bus = ICBus(platform, logger)
        bus.emit_ic_01(payload)   # called by CLU-01.1 produce path
        ...

    STATUS: WIRED — Step 10 IC Integration
    """

    def __init__(self, platform, logger):
        self._platform = platform
        self._logger = logger

        # Broadcast subscriber registries
        self._ic08_subscribers: List[Callable[[IC08Payload], None]] = []
        self._ic11_subscribers: List[Callable[[IC11Payload], None]] = []
        self._ic12_subscribers: List[Callable[[IC12Payload], None]] = []

        self._register_ic08_subscribers()
        self._register_ic11_subscribers()
        self._register_ic12_subscribers()

    # ------------------------------------------------------------------
    # Subscriber registration (broadcast ICs)
    # ------------------------------------------------------------------

    def _register_ic08_subscribers(self) -> None:
        """
        IC-08: Council Ruling Propagation — broadcast to CLU-02.4 + all clusters.
        CLU-02.4 (ruling_registry) is wired directly. All other clusters receive
        stub handlers until cluster-level implementation is built.
        """
        # CLU-02.4 direct wire (TRUSTED receive method exists)
        self._ic08_subscribers.append(
            self._platform.council.ruling_registry.receive_ruling_propagation
        )
        # All other clusters — stub receivers (ic_integration_stubs.py)
        self._ic08_subscribers.extend(
            build_ic08_subscribers(self._platform, self._logger)
        )

    def _register_ic11_subscribers(self) -> None:
        """
        IC-11: Language Compliance Clearance — broadcast to all document-producing modules.
        All clusters receive stub handlers pending per-cluster clearance gating.
        """
        self._ic11_subscribers.extend(
            build_ic11_subscribers(self._platform, self._logger)
        )

    def _register_ic12_subscribers(self) -> None:
        """
        IC-12: Lexicon Update Propagation — broadcast to all clusters.
        CLU-05.3 disqualification trigger wired directly below in emit_ic_12().
        All cluster-level subscriptions are stub handlers.
        """
        self._ic12_subscribers.extend(
            build_ic12_subscribers(self._platform, self._logger)
        )

    # ------------------------------------------------------------------
    # IC-01 — Assessment-to-Fracture Profile
    # Producer: CLU-01.1 | Consumers: CLU-01.2, CLU-01.5
    # ------------------------------------------------------------------

    def emit_ic_01(self, payload: IC01Payload) -> None:
        """
        Dispatch IC-01 assessment payload from CLU-01.1 to:
          - CLU-01.2 (StageProgressionLogic) — informs stage context
          - CLU-01.5 (FormationPathwayRouter) — triggers profile receipt
        """
        self._logger.log(
            f"IC-01 dispatched | participant_id={payload.participant_id} | "
            f"assessment_date={payload.assessment_date}"
        )
        # CLU-01.1 — intake trigger; produces a draft Fracture Domain Profile.
        self._platform.restoration_os.fracture_engine.receive_assessment(
            participant_id=payload.participant_id,
            doc_04_1_ref=payload.intake_questionnaire_ref,
            doc_04_2_ref=payload.fracture_map_ref,
        )
        # CLU-01.2 — notify StageProgressionLogic of IC-01 draft profile output.
        # Stub pending CLU-01.2 receive_ic_01_profile() implementation.
        ic_01_stage_progression_stub(
            stage_logic_instance=self._platform.restoration_os.stage_logic,
            payload=payload,
            logger=self._logger,
        )
        # CLU-01.5 — notify FormationPathwayRouter of IC-01 draft profile output.
        # Finalized profile arrives via IC-02 (emit_ic_02). This covers the
        # ICM-01 IC-01 consumer routing requirement for CLU-01.5.
        # Stub pending CLU-01.5 receive_ic_01_profile() implementation.
        ic_01_pathway_router_stub(
            pathway_router_instance=self._platform.restoration_os.pathway_router,
            payload=payload,
            logger=self._logger,
        )

    # ------------------------------------------------------------------
    # IC-02 — Fracture Profile-to-Pathway Assignment
    # Producer: CLU-01.1 | Consumer: CLU-01.5
    # ------------------------------------------------------------------

    def emit_ic_02(self, payload: IC02Payload) -> None:
        """
        Dispatch IC-02 finalized fracture profile from CLU-01.1 to CLU-01.5
        (FormationPathwayRouter) for pathway assignment.
        """
        self._logger.log(
            f"IC-02 dispatched | fracture_profile_id={payload.fracture_profile_id} | "
            f"participant_id={payload.participant_id} | "
            f"active_domains={payload.active_domains}"
        )
        from models import FractureDomainProfile
        # Build a minimal FractureDomainProfile transfer object for the router.
        # Uses model field names (fracture_profile_id / severity_map) per OBJ-05 schema.
        # hub_id is carried in IC-02 payload but not a field on FractureDomainProfile —
        # the router derives hub assignment from pathway logic, not from the profile object.
        profile_transfer = FractureDomainProfile(
            fracture_profile_id=payload.fracture_profile_id,
            participant_id=payload.participant_id,
            facilitator_id=payload.facilitator_id,
            active_domains=payload.active_domains,
            severity_map=payload.severity_per_domain,   # IC-02 ships str; router coerces to enum
        )
        self._platform.restoration_os.pathway_router.receive_finalized_profile(
            profile=profile_transfer
        )

    # ------------------------------------------------------------------
    # IC-03 — Milestone-to-Stage Progression
    # Producer: CLU-01.3 | Consumer: CLU-01.2
    # ------------------------------------------------------------------

    def emit_ic_03(self, payload: IC03Payload) -> None:
        """
        Dispatch IC-03 milestone threshold signal from CLU-01.3 to CLU-01.2
        (StageProgressionLogic) to create a stage progression evaluation.
        """
        self._logger.log(
            f"IC-03 dispatched | participant_id={payload.participant_id} | "
            f"stage={payload.current_stage} | "
            f"threshold_met={payload.milestone_threshold_met} | "
            f"completion_pct={payload.completion_percentage:.1f}%"
        )
        self._platform.restoration_os.stage_logic.receive_milestone_signal(
            participant_id=payload.participant_id,
            evaluation_data={
                "current_stage": payload.current_stage,
                "milestones_completed": payload.milestones_completed,
                "milestones_pending": payload.milestones_pending,
                "facilitator_attestation_ids": payload.facilitator_attestation_ids,
                "last_assessment_date": payload.last_assessment_date,
                "milestone_threshold_met": payload.milestone_threshold_met,
                "completion_percentage": payload.completion_percentage,
                **payload.evaluation_data,
            },
        )

    # ------------------------------------------------------------------
    # IC-04 — Blockage-to-Stage Hold (hold and clear)
    # Producer: CLU-01.4 | Consumer: CLU-01.2
    # ------------------------------------------------------------------

    def emit_ic_04_hold(self, payload: IC04HoldPayload) -> None:
        """
        Dispatch IC-04 hold signal from CLU-01.4 to CLU-01.2.
        Immediately sets advancement_blocked on the participant's evaluation record.
        """
        self._logger.log(
            f"IC-04 HOLD dispatched | participant_id={payload.participant_id} | "
            f"blockage_id={payload.blockage_id} | "
            f"type={payload.blockage_type} | severity={payload.blockage_severity}"
        )
        self._platform.restoration_os.stage_logic.receive_blockage_hold(
            participant_id=payload.participant_id,
            blockage_id=payload.blockage_id,
        )

    def emit_ic_04_clear(self, payload: IC04ClearPayload) -> None:
        """
        Dispatch IC-04 clear signal from CLU-01.4 to CLU-01.2.
        Re-evaluates advancement eligibility after blockage resolution.
        """
        self._logger.log(
            f"IC-04 CLEAR dispatched | participant_id={payload.participant_id} | "
            f"blockage_id={payload.blockage_id} | resolved_by={payload.resolved_by}"
        )
        self._platform.restoration_os.stage_logic.receive_blockage_clear(
            participant_id=payload.participant_id,
            blockage_id=payload.blockage_id,
        )

    # ------------------------------------------------------------------
    # IC-05 — Pathway-to-Hub Routing
    # Producer: CLU-01.5 | Consumers: CLU-04.1, CLU-04.3
    # ------------------------------------------------------------------

    def emit_ic_05(self, payload: IC05Payload) -> None:
        """
        Dispatch IC-05 pathway routing signal from CLU-01.5 to:
          - CLU-04.1 (HubFormationProtocol) — registers participant routing
          - CLU-04.3 (HouseholdRhythmScheduler) — schedules session rhythm
          - CLU-04.4 (HospitalityOperationsModule) — hospitality integration
        """
        self._logger.log(
            f"IC-05 dispatched | pathway_id={payload.pathway_id} | "
            f"participant_id={payload.participant_id} | "
            f"hub_id={payload.hub_id} | stage={payload.assigned_stage}"
        )
        # CLU-04.1 — register participant routing
        self._platform.emmaus_road.hub_formation.receive_pathway_routing(
            participant_id=payload.participant_id,
            hub_routing_ref=payload.pathway_id,
        )
        # CLU-04.3 — schedule household rhythm for participant.
        # HouseholdRhythmScheduler.receive_participant_routing() —
        # stub until CLU-04.3 implementation is built.
        self._logger.log(
            f"IC-05 CLU-04.3 stub | pathway_id={payload.pathway_id} | "
            f"participant_id={payload.participant_id} | "
            f"session_types={payload.session_type_requirements}"
        )
        # TODO: self._platform.emmaus_road.rhythm_scheduler.receive_participant_routing(payload)
        # CLU-04.4 — hospitality integration for incoming participant.
        # Stub pending CLU-04.4 receive_pathway_routing() implementation.
        ic_05_hospitality_stub(
            hospitality_instance=self._platform.emmaus_road.hospitality,
            payload=payload,
            logger=self._logger,
        )

    # ------------------------------------------------------------------
    # IC-06 — Formation Record Feed
    # Producer: CLU-01.6 | Consumers: CLU-02.1 (governance), CLU-06.5 (capital)
    # ------------------------------------------------------------------

    def emit_ic_06_governance(self, payload: IC06GovernancePayload) -> None:
        """
        Dispatch IC-06 governance aggregate report from CLU-01.6 to CLU-02.1
        (GoverningAuthorityModule). Report is anonymized per DOC-01.1 (VR-12-03).
        """
        self._logger.log(
            f"IC-06 Governance dispatched | report_id={payload.report_id} | "
            f"period={payload.reporting_period_start}–{payload.reporting_period_end} | "
            f"total_participants={payload.total_participants}"
        )
        self._platform.council.governing_authority.receive_formation_record_feed(
            aggregate_report={
                "report_id": payload.report_id,
                "reporting_period_start": payload.reporting_period_start,
                "reporting_period_end": payload.reporting_period_end,
                "authorization_ref": payload.authorization_ref,
                "total_participants": payload.total_participants,
                "stage_distribution": payload.stage_distribution,
                "domain_prevalence": payload.domain_prevalence,
                "blockage_frequency": payload.blockage_frequency,
                "milestone_completion_rate": payload.milestone_completion_rate,
            }
        )

    def emit_ic_06_capital(self, payload: IC06CapitalPayload) -> None:
        """
        Dispatch IC-06 capital aggregate report from CLU-01.6 to CLU-06.5
        (CapitalReportingInterface). CLU-06.5 has no explicit receive method
        in its TRUSTED skeleton — routed via stub per ic_integration_stubs.py.
        """
        self._logger.log(
            f"IC-06 Capital dispatched | report_id={payload.report_id} | "
            f"period={payload.reporting_period_start}–{payload.reporting_period_end} | "
            f"participant_count={payload.participant_count}"
        )
        ic_06_capital_stub(
            capital_reporting_instance=self._platform.capital_engine.capital_reporting,
            payload=payload,
            logger=self._logger,
        )

    # ------------------------------------------------------------------
    # IC-07 — Theological Review Request
    # Producer: Any cluster | Consumer: CLU-02.2
    # ------------------------------------------------------------------

    def emit_ic_07(self, payload: IC07Payload) -> None:
        """
        Dispatch IC-07 theological review request from any cluster to CLU-02.2
        (TheologicalReviewEngine). Any cluster may submit; CLU-02.2 governs review.
        """
        self._logger.log(
            f"IC-07 dispatched | requesting_module={payload.requesting_module} | "
            f"content_type={payload.content_type} | "
            f"content_ref={payload.content_ref} | "
            f"priority={payload.review_priority}"
        )
        self._platform.council.theological_review.receive_review_request(
            submitted_by_cluster=payload.requesting_module,
            asset_ref=payload.content_ref,
            asset_type=payload.content_type,
            asset_content_summary=payload.asset_content_summary,
        )

    # ------------------------------------------------------------------
    # IC-08 — Council Ruling Propagation (broadcast)
    # Producer: CLU-02.1 | Consumers: CLU-02.4 + all clusters
    # ------------------------------------------------------------------

    def emit_ic_08(self, payload: IC08Payload) -> None:
        """
        Dispatch IC-08 council ruling propagation broadcast from CLU-02.1.
        Dispatched to CLU-02.4 (direct wire) and all cluster stubs.
        CLU-02.4 receives a RulingPropagationRecord via receive_ruling_propagation().
        All other clusters receive stub logging until cluster-level implementation.
        """
        self._logger.log(
            f"IC-08 broadcast dispatched | ruling_id={payload.ruling_id} | "
            f"ruling_type={payload.ruling_type} | "
            f"effective_date={payload.effective_date} | "
            f"affected_clusters={payload.affected_clusters}"
        )
        for subscriber in self._ic08_subscribers:
            try:
                subscriber(payload)
            except Exception as exc:
                self._logger.log(
                    f"IC-08 dispatch error | subscriber={subscriber} | error={exc}"
                )

    # ------------------------------------------------------------------
    # IC-09 — Capital Source Integrity Clearance
    # Producer: CLU-03.1 | Consumers: CLU-03.2, CLU-06.1
    # ------------------------------------------------------------------

    def emit_ic_09(self, payload: IC09Payload) -> None:
        """
        Dispatch IC-09 capital source integrity clearance from CLU-03.1 to:
          - CLU-03.2 (GenerativeGivingEngine) — approved donor enters giving pipeline
          - CLU-06.1 (FundingStreamManager) — approved source creates/updates stream entry
        """
        self._logger.log(
            f"IC-09 dispatched | clearance_id={payload.clearance_id} | "
            f"source_id={payload.source_id} | "
            f"integrity_status={payload.integrity_status} | "
            f"source_type={payload.source_type}"
        )
        # CLU-03.2 — donor engagement pipeline
        self._platform.spikenard.giving_engine.receive_approved_donor(
            source_clearance_ref=payload.clearance_id,
            donor_id=payload.donor_id,
        )
        # CLU-06.1 — funding stream inventory
        self._platform.capital_engine.stream_manager.receive_approved_source(
            source_clearance_ref=payload.clearance_id,
            source_name=payload.source_name,
            stream_type=payload.source_type,
            amount_category=payload.amount_category,
        )

    # ------------------------------------------------------------------
    # IC-10 — Fund Allocation Authorization
    # Producer: CLU-03.5 | Consumer: CLU-06.6
    # ------------------------------------------------------------------

    def emit_ic_10(self, payload: IC10Payload) -> None:
        """
        Dispatch IC-10 fund allocation authorization from CLU-03.5 to CLU-06.6
        (DeploymentFundingLogic). Deployment funding may not be initiated
        without IC-10 clearance (VR-06-17).
        """
        self._logger.log(
            f"IC-10 dispatched | disbursement_authorization_id={payload.disbursement_authorization_id} | "
            f"allocation_type={payload.allocation_type} | "
            f"destination_id={payload.destination_id} | "
            f"effective_date={payload.effective_date}"
        )
        self._platform.capital_engine.deployment_funding.receive_fund_allocation_authorization(
            disbursement_ref=payload.disbursement_authorization_id,
            available_capital_category=payload.authorized_amount_category,
            fund_allocation_ref=payload.allocation_id,
        )

    # ------------------------------------------------------------------
    # IC-11 — Language Compliance Clearance (broadcast)
    # Producer: CLU-05.1 | Consumers: all document-producing modules
    # ------------------------------------------------------------------

    def emit_ic_11(self, payload: IC11Payload) -> None:
        """
        Dispatch IC-11 language compliance clearance broadcast from CLU-05.1.
        All clusters receive stub handlers pending per-cluster gating implementation.
        """
        self._logger.log(
            f"IC-11 broadcast dispatched | clearance_id={payload.clearance_id} | "
            f"content_ref={payload.content_ref} | "
            f"requesting_cluster={payload.requesting_cluster} | "
            f"status={payload.compliance_status}"
        )
        for subscriber in self._ic11_subscribers:
            try:
                subscriber(payload)
            except Exception as exc:
                self._logger.log(
                    f"IC-11 dispatch error | subscriber={subscriber} | error={exc}"
                )

    # ------------------------------------------------------------------
    # IC-12 — Lexicon Update Propagation (broadcast)
    # Producer: CLU-05.2 | Consumers: all clusters + CLU-05.3 on Disqualification
    # ------------------------------------------------------------------

    def emit_ic_12(self, payload: IC12Payload) -> None:
        """
        Dispatch IC-12 lexicon update propagation broadcast from CLU-05.2.
        On Disqualification: additionally triggers CLU-05.3 (LanguageAuditModule)
        to initiate content scan per ICM-01 IC-12 routing rule.
        All cluster-level subscriptions are stub handlers.
        """
        self._logger.log(
            f"IC-12 broadcast dispatched | propagation_id={payload.propagation_id} | "
            f"term='{payload.term}' | "
            f"update_type={payload.update_type} | "
            f"effective_date={payload.effective_date}"
        )
        # All cluster stubs
        for subscriber in self._ic12_subscribers:
            try:
                subscriber(payload)
            except Exception as exc:
                self._logger.log(
                    f"IC-12 dispatch error | subscriber={subscriber} | error={exc}"
                )
        # CLU-05.3 direct trigger on Disqualification
        if payload.update_type == "Disqualification":
            self._logger.log(
                f"IC-12 CLU-05.3 disqualification audit trigger | term='{payload.term}'"
            )
            # TODO: self._platform.linguistic_engine.language_auditor.receive_disqualification_trigger(payload)
            # CLU-05.3 receive method pending — logging dispatch until implementation.

    # ------------------------------------------------------------------
    # IC-13 — Hub Health Escalation
    # Producer: CLU-04.6 | Consumer: CLU-02.1
    # ------------------------------------------------------------------

    def emit_ic_13(self, payload: IC13Payload) -> None:
        """
        Dispatch IC-13 hub health escalation from CLU-04.6 to CLU-02.1
        (GoverningAuthorityModule). Mandatory escalation on two consecutive
        below-threshold assessments (VR-04-18).
        """
        self._logger.log(
            f"IC-13 dispatched | health_assessment_id={payload.health_assessment_id} | "
            f"hub_id={payload.hub_id} | "
            f"health_score={payload.health_score} | "
            f"consecutive_below_threshold={payload.consecutive_below_threshold} | "
            f"risk_areas={payload.risk_areas}"
        )
        self._platform.council.governing_authority.receive_hub_health_escalation(
            escalation={
                "health_assessment_id": payload.health_assessment_id,
                "hub_id": payload.hub_id,
                "health_score": payload.health_score,
                "consecutive_below_threshold": payload.consecutive_below_threshold,
                "risk_areas": payload.risk_areas,
                "hub_leader_id": payload.hub_leader_id,
                "assessment_date": payload.assessment_date,
            }
        )

    # ------------------------------------------------------------------
    # IC-14 — Deployment Funding Authorization
    # Producer: CLU-06.6 | Consumer: CLU-04.1
    # ------------------------------------------------------------------

    def emit_ic_14(self, payload: IC14Payload) -> None:
        """
        Dispatch IC-14 deployment funding authorization from CLU-06.6 to CLU-04.1
        (HubFormationProtocol). Hub formation is blocked until funding is authorized
        (VR-04-03).
        """
        self._logger.log(
            f"IC-14 dispatched | funding_authorization_id={payload.funding_authorization_id} | "
            f"hub_id={payload.hub_id} | "
            f"funding_status={payload.funding_status} | "
            f"authorized_amount_category={payload.authorized_amount_category}"
        )
        self._platform.emmaus_road.hub_formation.receive_deployment_funding_authorization(
            deployment_funding_ref=payload.funding_authorization_id,
            authorized_budget_category=payload.authorized_amount_category,
        )
