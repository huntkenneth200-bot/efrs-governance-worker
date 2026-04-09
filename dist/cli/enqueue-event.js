#!/usr/bin/env ts-node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const QueueAdapterRegistry_1 = require("../queue/QueueAdapterRegistry");
const InMemoryQueueClient_1 = require("../queue/InMemoryQueueClient");
const SchemaBootstrap_1 = require("../validation/SchemaBootstrap");
const ValidatorFactory_1 = require("../validation/ValidatorFactory");
const WitnessLogger_1 = require("../logging/WitnessLogger");
async function main() {
    const queueName = process.argv[2] ?? "document-events";
    const documentId = process.argv[3] ?? "doc-1";
    const tenantId = process.argv[4] ?? "tenant-1";
    const eventType = process.argv[5] ?? "TEST_EVENT";
    (0, SchemaBootstrap_1.bootstrapSchemas)();
    const client = new InMemoryQueueClient_1.InMemoryQueueClient();
    (0, QueueAdapterRegistry_1.registerQueueAdapter)("default", client);
    const event = {
        documentId,
        tenantId,
        eventType,
        payload: {
            example: true,
            note: "Injected via CLI enqueue-event.ts"
        },
        occurredAt: new Date().toISOString()
    };
    const validated = (0, ValidatorFactory_1.validateOrThrow)("DocumentEvent", event);
    WitnessLogger_1.witness.log("CLI_ENQUEUE_EVENT", { queueName, event: validated });
    await client.enqueue(queueName, validated);
}
main().catch((err) => {
    WitnessLogger_1.witness.log("CLI_ENQUEUE_FATAL", { error: String(err) }, "ERROR");
    process.exit(1);
});
//# sourceMappingURL=enqueue-event.js.map