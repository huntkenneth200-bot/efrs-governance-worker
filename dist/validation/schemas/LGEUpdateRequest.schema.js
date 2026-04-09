"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LGEUpdateRequestSchema = void 0;
exports.LGEUpdateRequestSchema = {
    type: "object",
    properties: {
        documentId: { type: "string" },
        tenantId: { type: "string" },
        lexiconKey: { type: "string" },
        payload: {
            type: "object",
            additionalProperties: true
        },
        occurredAt: { type: "string" }
    },
    required: ["documentId", "tenantId", "lexiconKey", "payload", "occurredAt"],
    additionalProperties: true
};
//# sourceMappingURL=LGEUpdateRequest.schema.js.map