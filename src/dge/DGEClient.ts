import type { ApiResponse, VersionedDto } from "../contracts";

export interface DgeEvaluateRequest extends VersionedDto {
  tenantId: string;
  documentType: string;
  payload: unknown;
}

export interface DgeEvaluateResult extends VersionedDto {
  tenantId: string;
  documentType: string;
  decision: "ALLOW" | "DENY" | "REVIEW";
  reasons: string[];
  metadata?: Record<string, unknown>;
}

export interface DGEClient {
  evaluate(
    request: DgeEvaluateRequest
  ): Promise<ApiResponse<DgeEvaluateResult>>;
}
