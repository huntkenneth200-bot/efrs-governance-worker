import { JSONSchemaType } from "ajv";
import { LGEUpdateRequest } from "../../engines/LGEClientContract";

export const LGEUpdateRequestSchema: JSONSchemaType<LGEUpdateRequest> = {
  type: "object",
  properties: {
    documentId: { type: "string" },
    tenantId: { type: "string" },
    lexiconKey: { type: "string" },
    payload: { type: "object" },
    occurredAt: { type: "string" }
  },
  required: ["documentId", "tenantId", "lexiconKey", "payload", "occurredAt"],
  additionalProperties: true
};
