"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DGEProcessResponseSchema = void 0;
exports.DGEProcessResponseSchema = {
    type: "object",
    properties: {
        documentId: { type: "string" },
        tenantId: { type: "string" },
        status: { type: "string", enum: ["ACCEPTED", "REJECTED", "PENDING"] },
        reason: { type: "string", nullable: true },
        version: { type: "number", nullable: true }
    },
    required: ["documentId", "tenantId", "status"],
    additionalProperties: false
};
//# sourceMappingURL=DGEProcessResponse.schema.js.map