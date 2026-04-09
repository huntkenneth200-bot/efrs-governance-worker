import { EventEmitter } from "events";
import type { GovernanceBus, GovernanceEvent } from "./GovernanceBus";

class GovernanceSignalBus extends EventEmitter implements GovernanceBus {
  emitEvent(event: GovernanceEvent) {
    this.emit(event.type, event);
  }
}


export const governanceBus = new GovernanceSignalBus();

// TEMPORARY DEBUG HANDLERS FOR INTERNAL WORKER EVENTS
governanceBus.on("MESSAGE_RECEIVED", (event) => {
  console.log("📥 MESSAGE_RECEIVED", event);
});

governanceBus.on("MESSAGE_PROCESSED", (event) => {
  console.log("📤 MESSAGE_PROCESSED", event);
});

governanceBus.on("MESSAGE_FAILED", (event) => {
  console.log("💥 MESSAGE_FAILED", event);
});
