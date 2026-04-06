"""
FORMATION INTELLIGENCE PLATFORM
Platform Configuration

Reference: CONFIG-01
Version: 0.1-scaffold
"""


class PlatformConfig:
    """
    Platform-wide configuration container.

    TODO: Load values from environment variables or .env file.
    No secrets in source code.
    """

    # Database
    DATABASE_URL: str = ""                  # TODO: Set from environment
    DATABASE_POOL_SIZE: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_RETENTION_DAYS_CRITICAL: int = 0    # 0 = permanent
    LOG_RETENTION_DAYS_ERROR: int = 0       # 0 = permanent
    LOG_RETENTION_DAYS_WARNING: int = 2555  # ~7 years
    LOG_RETENTION_DAYS_INFO: int = 1095     # ~3 years

    # Formation thresholds — governed by DOC-03.3 and DOC-03.4
    MAX_TIME_IN_STAGE_DAYS: dict = {
        "STAGE_1": 180,
        "STAGE_2": 365,
        "STAGE_3": 365,
        "STAGE_4": 365,
        "STAGE_5": 180,
    }
    MILESTONE_OVERDUE_THRESHOLD_DAYS: int = 30   # TODO: Per-milestone overrides in DOC-03.4
    PERIODIC_ASSESSMENT_INTERVAL_DAYS: int = 90  # DOC-04.3 interval

    # Hub thresholds — governed by DOC-02.2
    HUB_HEALTH_BELOW_THRESHOLD_SCORE: float = 70.0
    HUB_HEALTH_ASSESSMENT_INTERVAL_DAYS: int = 90
    HUB_HEALTH_ESCALATION_CONSECUTIVE_COUNT: int = 2

    # Council timing — governed by DOC-01.2
    COUNCIL_ACKNOWLEDGMENT_REQUIRED_DAYS: int = 14
    COUNCIL_REVIEW_WINDOW_DAYS: int = 30
    FACILITATOR_REVIEW_WINDOW_DAYS: int = 7

    # Capital — governed by DOC-01.4
    MAX_SINGLE_SOURCE_CONCENTRATION_PCT: float = 40.0  # TODO: Council to define
    CLEARANCE_RENEWAL_INTERVAL_DAYS: int = 365
    DEPLOYMENT_AUTHORIZATION_EXPIRY_DAYS: int = 180

    # Language — governed by DOC-01.5
    LANGUAGE_AUDIT_INTERVAL_DAYS: int = 365
    LEXICON_REVIEW_INTERVAL_DAYS: int = 365

    # Governance Layer — governed by DOC-01.1, DOC-01.2
    COUNCIL_QUORUM_MINIMUM: int = 3                        # DOC-01.2 Article III
    GOVERNANCE_DRIFT_WARNING_THRESHOLD: float = 0.65       # Drift alert threshold
    GOVERNANCE_DRIFT_REMEDIATION_THRESHOLD: float = 0.85   # Drift remediation threshold
