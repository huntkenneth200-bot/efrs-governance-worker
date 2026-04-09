export type LineageFinalStatus = "SUCCESS" | "FAILED";
export interface EventLineageRecord {
    correlationId: string;
    messageId?: string;
    documentId: string;
    tenantId: string;
    eventType: string;
    dgeStatus?: string;
    lgeStatus?: string;
    startedAt: number;
    completedAt: number;
    retries: number;
    finalStatus: LineageFinalStatus;
}
export declare class EventLineageStore {
    private readonly maxSize;
    private readonly records;
    constructor(maxSize?: number);
    add(record: EventLineageRecord): void;
    getByCorrelationId(correlationId: string): EventLineageRecord | undefined;
    getByDocumentId(documentId: string): EventLineageRecord[];
    getRecent(limit?: number): EventLineageRecord[];
}
export declare const eventLineageStore: EventLineageStore;
//# sourceMappingURL=EventLineageStore.d.ts.map