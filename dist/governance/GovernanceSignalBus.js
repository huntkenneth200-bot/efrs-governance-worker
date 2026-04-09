"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.governanceBus = void 0;
const events_1 = require("events");
class GovernanceSignalBus extends events_1.EventEmitter {
    emitEvent(event) {
        this.emit(event.type, event);
    }
}
exports.governanceBus = new GovernanceSignalBus();
// TEMPORARY DEBUG HANDLERS FOR INTERNAL WORKER EVENTS
exports.governanceBus.on("MESSAGE_RECEIVED", (event) => {
    console.log("📥 MESSAGE_RECEIVED", event);
});
exports.governanceBus.on("MESSAGE_PROCESSED", (event) => {
    console.log("📤 MESSAGE_PROCESSED", event);
});
exports.governanceBus.on("MESSAGE_FAILED", (event) => {
    console.log("💥 MESSAGE_FAILED", event);
});
//# sourceMappingURL=GovernanceSignalBus.js.map