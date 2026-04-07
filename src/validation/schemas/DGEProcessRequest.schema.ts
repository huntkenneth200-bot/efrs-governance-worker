import { JSONSchemaType } from "ajv";
import { DGEProcessRequest } from "../../engines/DGEClientContract";

export const DGEProcessRequestSchema: JSONSchemaType<DGEProcessRequest> = {
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