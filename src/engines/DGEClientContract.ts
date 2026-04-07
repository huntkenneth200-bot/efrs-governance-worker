export interface DGEProcessRequest {
  documentId: string;
  tenantId: string;
  eventType: string;
  payload: Record<string, unknown>;
  occurredAt: string; // ISO timestamp
}

export interface DGEProcessResponse {
  documentId: string;
  tenantId: string;
  status: "ACCEPTED" | "REJECTED" | "PENDING";
  reason?: string;
  version?: number;
}

export interface DGEClientContract {
  process(request: DGEProcessRequest): Promise<DGEProcessResponse>;
}
