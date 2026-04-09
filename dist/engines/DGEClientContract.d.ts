export interface DGEProcessRequest {
    documentId: string;
    tenantId: string;
    eventType: string;
    payload: Record<string, unknown>;
    occurredAt: string;
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
export interface DgeEvaluateRequest {
    tenantId: string;
    documentType: string;
    payload: Record<string, unknown>;
    version: string;
}
export interface DgeEvaluateResult {
    tenantId: string;
    documentType: string;
    decision: "ALLOW" | "DENY" | "REVIEW";
    reasons: string[];
    version: string;
}
//# sourceMappingURL=DGEClientContract.d.ts.map