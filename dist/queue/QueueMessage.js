"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.assertValidQueueMessage = assertValidQueueMessage;
const Invariant_1 = require("../invariants/Invariant");
function assertValidQueueMessage(msg) {
    (0, Invariant_1.invariant)(typeof msg.id === "string" && msg.id.length > 0, "QueueMessage.id must be a non-empty string", msg);
    (0, Invariant_1.invariant)(typeof msg.attempts === "number" && msg.attempts >= 0, "QueueMessage.attempts must be a non-negative number", msg);
    (0, Invariant_1.invariant)(msg.payload !== undefined, "QueueMessage.payload must not be undefined", msg);
}
//# sourceMappingURL=QueueMessage.js.map