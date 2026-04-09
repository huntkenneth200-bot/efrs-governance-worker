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
export declare class InMemoryGovernanceBus implements GovernanceBus {
    private events;
    emitEvent(event: GovernanceEvent): void;
    getEvents(): GovernanceEvent[];
    clear(): void;
}
//# sourceMappingURL=GovernanceBus.d.ts.map