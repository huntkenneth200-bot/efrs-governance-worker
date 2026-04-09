"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DocumentEventSchema = void 0;
exports.assertValidDocumentEvent = assertValidDocumentEvent;
const Invariant_1 = require("../../invariants/Invariant");
exports.DocumentEventSchema = {
    type: "object",
    properties: {
        documentId: { type: "string" },
        tenantId: { type: "string" },
        eventType: { type: "string" },
        payload: {
            type: "object",
            additionalProperties: true
        },
        occurredAt: { type: "string" }
    },
    required: ["documentId", "tenantId", "eventType", "payload", "occurredAt"],
    additionalProperties: true
};
function assertValidDocumentEvent(value) {
    (0, Invariant_1.invariant)(typeof value.documentId === "string" && value.documentId.length > 0, "DocumentEvent.documentId must be a non-empty string", value);
    (0, Invariant_1.invariant)(typeof value.tenantId === "string" && value.tenantId.length > 0, "DocumentEvent.tenantId must be a non-empty string", value);
    (0, Invariant_1.invariant)(typeof value.eventType === "string" && value.eventType.length > 0, "DocumentEvent.eventType must be a non-empty string", value);
    (0, Invariant_1.invariant)(typeof value.occurredAt === "string", "DocumentEvent.occurredAt must be an ISO timestamp string", value);
}
//# sourceMappingURL=DocumentEvent.schema.js.map