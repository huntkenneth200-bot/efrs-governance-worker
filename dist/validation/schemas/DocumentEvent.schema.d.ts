import { JSONSchemaType } from "ajv";
export interface DocumentEvent {
    documentId: string;
    tenantId: string;
    eventType: string;
    payload: Record<string, unknown>;
    occurredAt: string;
}
export declare const DocumentEventSchema: JSONSchemaType<DocumentEvent>;
export declare function assertValidDocumentEvent(value: DocumentEvent): void;
//# sourceMappingURL=DocumentEvent.schema.d.ts.map