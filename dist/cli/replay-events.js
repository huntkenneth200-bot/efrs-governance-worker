#!/usr/bin/env ts-node
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs_1 = __importDefault(require("fs"));
const readline_1 = __importDefault(require("readline"));
const QueueAdapterRegistry_1 = require("../queue/QueueAdapterRegistry");
const InMemoryQueueClient_1 = require("../queue/InMemoryQueueClient");
const SchemaBootstrap_1 = require("../validation/SchemaBootstrap");
const ValidatorFactory_1 = require("../validation/ValidatorFactory");
const WitnessLogger_1 = require("../logging/WitnessLogger");
async function main() {
    const filePath = process.argv[2];
    const queueName = process.argv[3] ?? "document-events";
    if (!filePath) {
        console.error("Usage: ts-node src/cli/replay-events.ts <filePath> [queueName]");
        process.exit(1);
    }
    if (!fs_1.default.existsSync(filePath)) {
        console.error(`File not found: ${filePath}`);
        process.exit(1);
    }
    (0, SchemaBootstrap_1.bootstrapSchemas)();
    const client = new InMemoryQueueClient_1.InMemoryQueueClient();
    (0, QueueAdapterRegistry_1.registerQueueAdapter)("default", client);
    const stream = fs_1.default.createReadStream(filePath, { encoding: "utf-8" });
    const rl = readline_1.default.createInterface({ input: stream, crlfDelay: Infinity });
    let count = 0;
    for await (const line of rl) {
        const trimmed = line.trim();
        if (!trimmed)
            continue;
        let parsed;
        try {
            parsed = JSON.parse(trimmed);
        }
        catch (err) {
            WitnessLogger_1.witness.log("REPLAY_EVENT_PARSE_ERROR", { line, error: String(err) }, "WARN");
            continue;
        }
        try {
            const validated = (0, ValidatorFactory_1.validateOrThrow)("DocumentEvent", parsed);
            await client.enqueue(queueName, validated);
            count += 1;
        }
        catch (err) {
            WitnessLogger_1.witness.log("REPLAY_EVENT_VALIDATION_ERROR", { event: parsed, error: String(err) }, "WARN");
        }
    }
    WitnessLogger_1.witness.log("REPLAY_EVENTS_COMPLETED", { filePath, queueName, count });
}
main().catch((err) => {
    WitnessLogger_1.witness.log("REPLAY_EVENTS_FATAL", { error: String(err) }, "ERROR");
    process.exit(1);
});
//# sourceMappingURL=replay-events.js.map