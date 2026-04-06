import { JSONSchemaType } from "ajv";
import { DGEProcessResponse } from "../../engines/DGEClientContract";

export const DGEProcessResponseSchema: JSONSchemaType<DGEProcessResponse> = {
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
