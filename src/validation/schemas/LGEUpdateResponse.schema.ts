import { JSONSchemaType } from "ajv";
import { LGEUpdateResponse } from "../../engines/LGEClientContract";

export const LGEUpdateResponseSchema: JSONSchemaType<LGEUpdateResponse> = {
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
