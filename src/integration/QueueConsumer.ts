import { getQueueAdapter } from "../queue/QueueAdapterRegistry";
import { DocumentEvent } from "../validation/schemas/DocumentEvent.schema";
import { QueueMessage, assertValidQueueMessage } from "../queue/QueueMessage";
import { ModuleIntegrator } from "./ModuleIntegrator";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";
import { governanceBus } from "../governance/GovernanceSignalBus";
import { toErrorEnvelope } from "../logging/ErrorEnvelope";

const MAX_ATTEMPTS = 3;
const DLQ_SUFFIX = "-dlq";

export async function startQueueConsumer(
  queueName: string,
  integrator: ModuleIntegrator
): Promise<void> {
  const client = getQueueAdapter("default");

  await client.registerConsumer(queueName, async (msg: QueueMessage<DocumentEvent>) => {
    assertValidQueueMessage(msg);

    try {
      await integrator.processMessage(msg);
      await client.ack(msg.id);
    } catch (err) {
      const attempts = msg.attempts ?? 0;
      const errorEnvelope = toErrorEnvelope(err);

      witness.log(
        "MESSAGE_PROCESSING_ERROR",
        {
          queueName,
          messageId: msg.id,
          attempts,
          error: errorEnvelope.message,
          errorName: errorEnvelope.name,
          invariantViolation: errorEnvelope.invariantViolation
        },
        "ERROR"
      );

      metrics.increment("queue_message_processing_error_total", {
        queueName,
        invariantViolation: errorEnvelope.invariantViolation
      });

      // Notify adapter of failure (for logging/metrics at adapter level)
      await client.fail(msg.id, err instanceof Error ? err : new Error(String(err)));

      if (attempts >= MAX_ATTEMPTS) {
        const dlqName = `${queueName}${DLQ_SUFFIX}`;

        await client.enqueue(dlqName, msg.payload);
        await client.ack(msg.id);

        metrics.increment("messages_dlq_total", { queueName, dlqName });

        governanceBus.emitEvent({
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

        witness.log(
          "MESSAGE_MOVED_TO_DLQ",
          {
            queueName,
            dlqName,
            messageId: msg.id,
            attempts
          },
          "ERROR"
        );
      } else {
        // Re-enqueue for retry
        await client.enqueue(queueName, msg.payload);
        await client.ack(msg.id);

        metrics.increment("messages_retry_total", { queueName });

        witness.log(
          "MESSAGE_REQUEUED_FOR_RETRY",
          {
            queueName,
            messageId: msg.id,
            attempts
          },
          "WARN"
        );
      }
    }
  });

  witness.log("QUEUE_CONSUMER_STARTED", { queueName });
}
