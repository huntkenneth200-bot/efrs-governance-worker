import { invariant } from "../invariants/Invariant";

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

export class EventLineageStore {
  private readonly maxSize: number;
  private readonly records: EventLineageRecord[] = [];

  constructor(maxSize = 1000) {
    this.maxSize = maxSize;
  }

  add(record: EventLineageRecord): void {
    invariant(record.startedAt <= record.completedAt, "Lineage timestamps out of order", record);
    invariant(record.finalStatus === "SUCCESS" || record.finalStatus === "FAILED", "Invalid finalStatus", record);
    invariant(record.retries >= 0, "Retries must be non-negative", record);

    this.records.push(record);
    if (this.records.length > this.maxSize) {
      this.records.shift();
    }
  }

  getByCorrelationId(correlationId: string): EventLineageRecord | undefined {
    return this.records.find((r) => r.correlationId === correlationId);
  }

  getByDocumentId(documentId: string): EventLineageRecord[] {
    return this.records.filter((r) => r.documentId === documentId);
  }

  getRecent(limit = 50): EventLineageRecord[] {
    if (limit <= 0) return [];
    return this.records.slice(-limit).reverse();
  }
}

export const eventLineageStore = new EventLineageStore();
