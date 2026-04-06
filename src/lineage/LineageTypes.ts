import type { IsoTimestamp } from "../contracts";

export type LineageEventType =
  | "REQUEST_RECEIVED"
  | "REQUEST_VALIDATED"
  | "DGE_CALL"
  | "LGE_CALL"
  | "QUEUE_ENQUEUE"
  | "QUEUE_CONSUME"
  | "ERROR";

export interface VersionedLineageRecord {
  schemaVersion: string;
}

export interface LineageRecord extends VersionedLineageRecord {
  id: string;
  correlationId: string;
  eventType: LineageEventType;
  timestamp: IsoTimestamp;
  actor?: string;
  context?: Record<string, unknown>;
}

export interface LineageStore {
  append(record: LineageRecord): Promise<void>;
  getByCorrelationId(correlationId: string): Promise<LineageRecord[]>;
}
