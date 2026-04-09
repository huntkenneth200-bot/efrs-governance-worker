import { LGEClientContract, LGEUpdateRequest, LGEUpdateResponse, LgeLexiconRequest, LgeLexiconResult } from "./LGEClientContract";
import { LGESimOptions } from "./LGESimEngine";
import type { ApiResponse } from "../contracts";
export type { LgeLexiconRequest, LgeLexiconResult };
export interface LGEClientOptions extends LGESimOptions {
    endpoint?: string;
    latencyMs?: number;
}
export declare class LGEClient implements LGEClientContract {
    private readonly endpoint;
    private readonly latencyMs;
    private readonly simEngine;
    private readonly simEngineMode;
    constructor(options?: LGEClientOptions);
    update(request: LGEUpdateRequest): Promise<LGEUpdateResponse>;
    resolve(request: LgeLexiconRequest): Promise<ApiResponse<LgeLexiconResult>>;
}
//# sourceMappingURL=LGEClient.d.ts.map