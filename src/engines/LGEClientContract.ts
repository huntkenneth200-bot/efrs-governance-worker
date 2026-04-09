export interface LGEUpdateRequest {
  documentId: string;
  tenantId: string;
  lexiconKey: string;
  payload: Record<string, unknown>;
  occurredAt: string; // ISO timestamp
}

export interface LGEUpdateResponse {
  documentId: string;
  tenantId: string;
  status: "UPDATED" | "NO_CHANGE" | "FAILED";
  reason?: string;
}

export interface LGEClientContract {
  update(request: LGEUpdateRequest): Promise<LGEUpdateResponse>;
}

export interface LgeLexiconRequest {
  tenantId: string;
  lexiconName: string;
  input: string;
  version: string;
}

export interface LgeLexiconResult {
  tenantId: string;
  lexiconName: string;
  output: string;
  version: string;
}
