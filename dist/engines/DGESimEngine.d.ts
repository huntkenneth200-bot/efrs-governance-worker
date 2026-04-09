import { DGEProcessRequest, DGEProcessResponse } from "./DGEClientContract";
export type DGESimMode = "NORMAL" | "ALWAYS_FAIL" | "RANDOM_FAILURE";
export interface DGESimOptions {
    mode?: DGESimMode;
    failureRate?: number;
}
export declare class DGESimEngine {
    private readonly mode;
    private readonly failureRate;
    private readonly versionMap;
    constructor(options?: DGESimOptions);
    process(request: DGEProcessRequest): DGEProcessResponse;
}
//# sourceMappingURL=DGESimEngine.d.ts.map