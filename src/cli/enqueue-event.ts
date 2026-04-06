#!/usr/bin/env ts-node

import { registerQueueAdapter } from "../queue/QueueAdapterRegistry";
import { InMemoryQueueClient } from "../queue/InMemoryQueueClient";
import { bootstrapSchemas } from "../validation/SchemaBootstrap";
import { validateOrThrow } from "../validation/ValidatorFactory";
import { witness } from "../logging/WitnessLogger";

interface DocumentEvent {
  documentId: string;
  tenantId: string;
  eventType: string;
  payload: unknown;
  occurredAt: string;
}

async function main() {
  const queueName = process.argv[2] ?? "document-events";
  const documentId = process.argv[3] ?? "doc-1";
  const tenantId = process.argv[4] ?? "tenant-1";
  const eventType = process.argv[5] ?? "TEST_EVENT";

  bootstrapSchemas();

  const client = new InMemoryQueueClient();
  registerQueueAdapter("default", client);

  const event: DocumentEvent = {
    documentId,
    tenantId,
    eventType,
    payload: {
      example: true,
      note: "Injected via CLI enqueue-event.ts"
    },
    occurredAt: new Date().toISOString()
  };

  const validated = validateOrThrow<DocumentEvent>("DocumentEvent", event);

  witness.log("CLI_ENQUEUE_EVENT", { queueName, event: validated });

  await client.enqueue(queueName, validated);
}

main().catch((err) => {
  witness.log("CLI_ENQUEUE_FATAL", { error: String(err) }, "ERROR");
  process.exit(1);
});
