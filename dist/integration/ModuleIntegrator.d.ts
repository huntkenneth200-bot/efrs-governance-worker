import type { DGEClient } from "../engines/DGEClient";
import type { DgeEvaluateRequest, DgeEvaluateResult } from "../engines/DGEClientContract";
import type { LGEClient } from "../engines/LGEClient";
import type { LgeLexiconRequest, LgeLexiconResult } from "../engines/LGEClientContract";
import type { ApiResponse } from "../contracts";
import { DocumentEvent } from "../validation/schemas/DocumentEvent.schema";
import { QueueMessage } from "../queue/QueueMessage";
import type { LineageStore } from "../lineage/LineageTypes";
import { GovernanceBus } from "../governance/GovernanceBus";
export declare class ModuleIntegrator {
    private readonly governanceBus;
    private readonly dgeClient;
    private readonly lgeClient;
    private readonly lineageStore?;
    constructor(options: {
        governanceBus: GovernanceBus;
        dgeClient: DGEClient;
        lgeClient: LGEClient;
        lineageStore?: LineageStore;
    });
    processMessage(message: QueueMessage<DocumentEvent>): Promise<void>;
    handleDgeEvaluate(request: DgeEvaluateRequest): Promise<ApiResponse<DgeEvaluateResult>>;
    handleLgeResolve(request: LgeLexiconRequest): Promise<ApiResponse<LgeLexiconResult>>;
}
//# sourceMappingURL=ModuleIntegrator.d.ts.map