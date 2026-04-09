"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LGEUpdateResponseSchema = void 0;
exports.LGEUpdateResponseSchema = {
    type: "object",
    properties: {
        documentId: { type: "string" },
        tenantId: { type: "string" },
        status: { type: "string", enum: ["UPDATED", "NO_CHANGE", "FAILED"] },
        reason: { type: "string", nullable: true }
    },
    required: ["documentId", "tenantId", "status"],
    additionalProperties: false
};
//# sourceMappingURL=LGEUpdateResponse.schema.js.map