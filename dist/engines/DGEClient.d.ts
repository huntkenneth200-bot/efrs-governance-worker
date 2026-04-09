import { DGEClientContract, DGEProcessRequest, DGEProcessResponse, DgeEvaluateRequest, DgeEvaluateResult } from "./DGEClientContract";
import { DGESimOptions } from "./DGESimEngine";
import type { ApiResponse } from "../contracts";
export type { DgeEvaluateRequest, DgeEvaluateResult };
export interface DGEClientOptions extends DGESimOptions {
    endpoint?: string;
    latencyMs?: number;
}
export declare class DGEClient implements DGEClientContract {
    private readonly endpoint;
    private readonly latencyMs;
    private readonly simEngine;
    private readonly simEngineMode;
    constructor(options?: DGEClientOptions);
    process(request: DGEProcessRequest): Promise<DGEProcessResponse>;
    evaluate(request: DgeEvaluateRequest): Promise<ApiResponse<DgeEvaluateResult>>;
}
//# sourceMappingURL=DGEClient.d.ts.map