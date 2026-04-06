"""
FORMATION INTELLIGENCE PLATFORM
Platform Logger

Provides the PlatformLogger used by all cluster submodules and ICBus.
All log entries route through this class. Log levels: CRITICAL, ERROR, WARNING, INFO.
Retention governed by PlatformConfig log retention settings.

Authority: DOC-01.1 (audit trail requirements)
Version: 1.0
Status: WIRED — Step 11 Activation

TODO: Implement structured log persistence (database or log service).
      Currently writes to stdout for activation verification.
"""

from __future__ import annotations
import datetime
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config import PlatformConfig


class PlatformLogger:
    """
    Central logging interface for the Formation Intelligence Platform.

    All platform events — IC dispatches, cluster operations, audit events —
    route through this logger. Supports leveled logging with retention
    rules governed by PlatformConfig.

    STATUS: ACTIVATION STUB — console output only.
    TODO: Wire to persistent log store per audit trail requirements (DOC-01.1).
    """

    LEVELS = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG")

    def __init__(self, config: "PlatformConfig"):
        self.config = config
        self._min_level = config.LOG_LEVEL if hasattr(config, "LOG_LEVEL") else "INFO"

    # ------------------------------------------------------------------
    # Primary interface — called throughout the platform
    # ------------------------------------------------------------------

    def log(self, message: str, level: str = "INFO") -> None:
        """
        Emit a log entry at the specified level.
        Default level is INFO. CRITICAL and ERROR always emit.
        """
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        line = f"[{timestamp}] [{level}] {message}"
        print(line, file=sys.stdout, flush=True)
        # TODO: Persist to structured log store with retention policy.

    def info(self, message: str) -> None:
        """Emit an INFO log entry."""
        self.log(message, level="INFO")

    def warning(self, message: str) -> None:
        """Emit a WARNING log entry."""
        self.log(message, level="WARNING")

    def error(self, message: str) -> None:
        """Emit an ERROR log entry."""
        self.log(message, level="ERROR")

    def critical(self, message: str) -> None:
        """
        Emit a CRITICAL log entry.
        CRITICAL entries are retained permanently per PlatformConfig (retention = 0).
        """
        self.log(message, level="CRITICAL")

    # ------------------------------------------------------------------
    # Activation heartbeat
    # ------------------------------------------------------------------

    def heartbeat(self, component: str) -> None:
        """
        Emit a heartbeat signal for a platform component during boot sequence.
        Used by STEP 11 activation to confirm each component initializes cleanly.
        """
        self.log(f"HEARTBEAT | component={component} | status=OK", level="INFO")
