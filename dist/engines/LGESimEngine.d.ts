import { LGEUpdateRequest, LGEUpdateResponse } from "./LGEClientContract";
export type LGESimMode = "NORMAL" | "ALWAYS_FAIL" | "RANDOM_FAILURE";
export interface LGESimOptions {
    mode?: LGESimMode;
    failureRate?: number;
}
export declare class LGESimEngine {
    private readonly mode;
    private readonly failureRate;
    private readonly state;
    constructor(options?: LGESimOptions);
    update(request: LGEUpdateRequest): LGEUpdateResponse;
}
//# sourceMappingURL=LGESimEngine.d.ts.map