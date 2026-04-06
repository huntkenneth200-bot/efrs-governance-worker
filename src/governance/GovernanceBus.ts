import type { IsoTimestamp } from "../contracts";

export interface GovernanceEvent {
  type: string;
  severity: "INFO" | "WARN" | "ERROR";
  timestamp: IsoTimestamp;
  id?: string;
  details?: Record<string, unknown>;
  source?: string;
  correlationId?: string;
}

export interface GovernanceBus {
  emitEvent(event: GovernanceEvent): void;
}

export class InMemoryGovernanceBus implements GovernanceBus {
  private events: GovernanceEvent[] = [];

  emitEvent(event: GovernanceEvent): void {
    this.events.push(event);
  }

  getEvents(): GovernanceEvent[] {
    return [...this.events];
  }

  clear(): void {
    this.events = [];
  }
}
