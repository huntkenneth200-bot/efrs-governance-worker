"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.startQueueConsumer = startQueueConsumer;
const QueueAdapterRegistry_1 = require("../queue/QueueAdapterRegistry");
const QueueMessage_1 = require("../queue/QueueMessage");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
const GovernanceSignalBus_1 = require("../governance/GovernanceSignalBus");
const ErrorEnvelope_1 = require("../logging/ErrorEnvelope");
const MAX_ATTEMPTS = 3;
const DLQ_SUFFIX = "-dlq";
async function startQueueConsumer(queueName, integrator) {
    const client = (0, QueueAdapterRegistry_1.getQueueAdapter)("default");
    await client.registerConsumer(queueName, async (msg) => {
        (0, QueueMessage_1.assertValidQueueMessage)(msg);
        try {
            await integrator.processMessage(msg);
            await client.ack(msg.id);
        }
        catch (err) {
            const attempts = msg.attempts ?? 0;
            const errorEnvelope = (0, ErrorEnvelope_1.toErrorEnvelope)(err);
            WitnessLogger_1.witness.log("MESSAGE_PROCESSING_ERROR", {
                queueName,
                messageId: msg.id,
                attempts,
                error: errorEnvelope.message,
                errorName: errorEnvelope.name,
                invariantViolation: errorEnvelope.invariantViolation
            }, "ERROR");
            MetricsRegistry_1.metrics.increment("queue_message_processing_error_total", {
                queueName,
                invariantViolation: errorEnvelope.invariantViolation
            });
            // Notify adapter of failure (for logging/metrics at adapter level)
            await client.fail(msg.id, err instanceof Error ? err : new Error(String(err)));
            if (attempts >= MAX_ATTEMPTS) {
                const dlqName = `${queueName}${DLQ_SUFFIX}`;
                await client.enqueue(dlqName, msg.payload);
                await client.ack(msg.id);
                MetricsRegistry_1.metrics.increment("messages_dlq_total", { queueName, dlqName });
                GovernanceSignalBus_1.governanceBus.emitEvent({
                    type: "MESSAGE_FAILED",
                    severity: "ERROR",
                    timestamp: new Date().toISOString(),
                    id: msg.id,
                    details: {
                        queueName,
                        dlqName,
                        attempts,
                        error: String(err)
                    }
                });
                WitnessLogger_1.witness.log("MESSAGE_MOVED_TO_DLQ", {
                    queueName,
                    dlqName,
                    messageId: msg.id,
                    attempts
                }, "ERROR");
            }
            else {
                // Re-enqueue for retry
                await client.enqueue(queueName, msg.payload);
                await client.ack(msg.id);
                MetricsRegistry_1.metrics.increment("messages_retry_total", { queueName });
                WitnessLogger_1.witness.log("MESSAGE_REQUEUED_FOR_RETRY", {
                    queueName,
                    messageId: msg.id,
                    attempts
                }, "WARN");
            }
        }
    });
    WitnessLogger_1.witness.log("QUEUE_CONSUMER_STARTED", { queueName });
}
//# sourceMappingURL=QueueConsumer.js.map