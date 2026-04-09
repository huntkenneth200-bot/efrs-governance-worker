import { EventEmitter } from "events";

export type GovernanceEventType =
  | "WORKER_STARTED"
  | "WORKER_READY"
  | "WORKER_HEARTBEAT"
  | "WORKER_SHUTDOWN"
  | "MESSAGE_RECEIVED"
  | "MESSAGE_PROCESSED"
  | "MESSAGE_FAILED"
  | "DRIFT_CHECKS_PASSED"
  | "DRIFT_ISSUE_DETECTED";

export type GovernanceSeverity = "INFO" | "WARN" | "ERROR";

export interface GovernanceEventPayload {
  type: GovernanceEventType;
  severity: GovernanceSeverity;
  timestamp: number;
  id?: string;
  details?: unknown;
}

import type { GovernanceBus, GovernanceEvent } from "./GovernanceBus";

class GovernanceSignalBus extends EventEmitter implements GovernanceBus {
  emitEvent(event: GovernanceEvent) {
    this.emit(event.type, event);
  }
}


export const governanceBus = new GovernanceSignalBus();

// TEMPORARY DEBUG HANDLERS FOR INTERNAL WORKER EVENTS
governanceBus.on("MESSAGE_RECEIVED", (event) => {
  console.log("📥 MESSAGE_RECEIVED", event);
});

governanceBus.on("MESSAGE_PROCESSED", (event) => {
  console.log("📤 MESSAGE_PROCESSED", event);
});

governanceBus.on("MESSAGE_FAILED", (event) => {
  console.log("💥 MESSAGE_FAILED", event);
});
