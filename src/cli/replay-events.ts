#!/usr/bin/env ts-node

import fs from "fs";
import readline from "readline";
import { registerQueueAdapter } from "../queue/QueueAdapterRegistry";
import { InMemoryQueueClient } from "../queue/InMemoryQueueClient";
import { bootstrapSchemas } from "../validation/SchemaBootstrap";
import { validateOrThrow } from "../validation/ValidatorFactory";
import { witness } from "../logging/WitnessLogger";

interface DocumentEvent {
  documentId: string;
  tenantId: string;
  eventType: string;
  payload: Record<string, unknown>;
  occurredAt: string;
}

async function main() {
  const filePath = process.argv[2];
  const queueName = process.argv[3] ?? "document-events";

  if (!filePath) {
    console.error("Usage: ts-node src/cli/replay-events.ts <filePath> [queueName]");
    process.exit(1);
  }

  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }

  bootstrapSchemas();

  const client = new InMemoryQueueClient();
  registerQueueAdapter("default", client);

  const stream = fs.createReadStream(filePath, { encoding: "utf-8" });
  const rl = readline.createInterface({ input: stream, crlfDelay: Infinity });

  let count = 0;

  for await (const line of rl) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    let parsed: unknown;
    try {
      parsed = JSON.parse(trimmed);
    } catch (err) {
      witness.log("REPLAY_EVENT_PARSE_ERROR", { line, error: String(err) }, "WARN");
      continue;
    }

    try {
      const validated = validateOrThrow<DocumentEvent>("DocumentEvent", parsed);
      await client.enqueue(queueName, validated);
      count += 1;
    } catch (err) {
      witness.log("REPLAY_EVENT_VALIDATION_ERROR", { event: parsed, error: String(err) }, "WARN");
    }
  }

  witness.log("REPLAY_EVENTS_COMPLETED", { filePath, queueName, count });
}

main().catch((err) => {
  witness.log("REPLAY_EVENTS_FATAL", { error: String(err) }, "ERROR");
  process.exit(1);
});
