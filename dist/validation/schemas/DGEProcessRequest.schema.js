"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DGEProcessRequestSchema = void 0;
exports.DGEProcessRequestSchema = {
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
//# sourceMappingURL=DGEProcessRequest.schema.js.map