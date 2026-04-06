import { JSONSchemaType } from "ajv";
import { invariant } from "../../invariants/Invariant";

export interface DocumentEvent {
  documentId: string;
  tenantId: string;
  eventType: string;
  payload: unknown;
  occurredAt: string;
}

export const DocumentEventSchema: JSONSchemaType<DocumentEvent> = {
  type: "object",
  properties: {
    documentId: { type: "string" },
    tenantId: { type: "string" },
    eventType: { type: "string" },
    payload: { type: "object" },
    occurredAt: { type: "string" }
  },
  required: ["documentId", "tenantId", "eventType", "payload", "occurredAt"],
  additionalProperties: true
};

export function assertValidDocumentEvent(value: DocumentEvent): void {
  invariant(typeof value.documentId === "string" && value.documentId.length > 0, "DocumentEvent.documentId must be a non-empty string", value);
  invariant(typeof value.tenantId === "string" && value.tenantId.length > 0, "DocumentEvent.tenantId must be a non-empty string", value);
  invariant(typeof value.eventType === "string" && value.eventType.length > 0, "DocumentEvent.eventType must be a non-empty string", value);
  invariant(typeof value.occurredAt === "string", "DocumentEvent.occurredAt must be an ISO timestamp string", value);
}
