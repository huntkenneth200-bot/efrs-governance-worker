import { EventEmitter } from "events";
import type { GovernanceBus, GovernanceEvent } from "./GovernanceBus";
declare class GovernanceSignalBus extends EventEmitter implements GovernanceBus {
    emitEvent(event: GovernanceEvent): void;
}
export declare const governanceBus: GovernanceSignalBus;
export {};
//# sourceMappingURL=GovernanceSignalBus.d.ts.map