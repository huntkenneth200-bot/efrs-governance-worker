import { QueueClient, QueueMessage } from "./QueueClient";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";
import { invariant } from "../invariants/Invariant";
import { InvariantViolation } from "../invariants/InvariantViolation";

type InternalQueueMessage<T = unknown> = QueueMessage<T>;

interface InMemoryQueue<T = unknown> {
  name: string;
  messages: InternalQueueMessage<T>[];
  consumer?: (msg: InternalQueueMessage<T>) => Promise<void>;
}

export class InMemoryQueueClient implements QueueClient {
  private queues = new Map<string, InMemoryQueue>();

  async enqueue<T>(queueName: string, payload: T): Promise<void> {
    invariant(typeof queueName === "string" && queueName.length > 0, "enqueue: queueName must be non-empty", {
      queueName
    });
    invariant(payload !== undefined, "enqueue: payload must not be undefined", {
      queueName
    });

    const queue = this.getOrCreateQueue<T>(queueName);
    const message: InternalQueueMessage<T> = {
      id: `${queueName}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
      payload,
      attempts: 0,
      enqueuedAt: Date.now()
    };

    queue.messages.push(message);
    metrics.increment("queue_enqueued_total", { queueName });
    witness.log("QUEUE_ENQUEUED", { queueName, messageId: message.id });

    const size = queue.messages.length;
    metrics.observe("queue_depth", size, { queueName });

    this.maybeDispatch(queueName);
  }

  async registerConsumer<T>(
    queueName: string,
    consumer: (msg: QueueMessage<T>) => Promise<void>
  ): Promise<void> {
    const queue = this.getOrCreateQueue<T>(queueName);
    queue.consumer = consumer as (msg: InternalQueueMessage<unknown>) => Promise<void>;
    witness.log("QUEUE_CONSUMER_REGISTERED", { queueName });
    this.maybeDispatch(queueName);
  }

  async ack(messageId: string): Promise<void> {
    invariant(
      typeof messageId === "string" && messageId.length > 0,
      "ack: messageId must be a non-empty string",
      { messageId }
    );

    witness.log(
      "QUEUE_MESSAGE_ACK",
      { messageId },
      "INFO"
    );

    metrics.increment("queue_message_ack_total", { messageId });
  }

  async fail(messageId: string, error: Error): Promise<void> {
    invariant(
      typeof messageId === "string" && messageId.length > 0,
      "fail: messageId must be a non-empty string",
      { messageId }
    );

    witness.log(
      "QUEUE_MESSAGE_FAIL",
      {
        messageId,
        error: String(error),
        invariantViolation: error instanceof InvariantViolation
      },
      "WARN"
    );

    metrics.increment("queue_message_fail_total", { messageId });
  }

  async getQueueSize(queueName: string): Promise<number> {
    invariant(
      typeof queueName === "string" && queueName.length > 0,
      "getQueueSize: queueName must be non-empty",
      { queueName }
    );
    const queue = this.queues.get(queueName);
    return queue ? queue.messages.length : 0;
  }

  async peekQueue<T = unknown>(queueName: string, limit = 10): Promise<QueueMessage<T>[]> {
    invariant(
      typeof queueName === "string" && queueName.length > 0,
      "peekQueue: queueName must be non-empty",
      { queueName }
    );
    invariant(
      typeof limit === "number" && limit > 0,
      "peekQueue: limit must be a positive number",
      { limit }
    );
    const queue = this.queues.get(queueName);
    if (!queue) return [];
    return queue.messages.slice(0, limit) as QueueMessage<T>[];
  }

  async drainQueue(queueName: string): Promise<void> {
    invariant(
      typeof queueName === "string" && queueName.length > 0,
      "drainQueue: queueName must be non-empty",
      { queueName }
    );
    const queue = this.queues.get(queueName);
    if (!queue) return;
    const drained = queue.messages.length;
    queue.messages = [];
    witness.log("QUEUE_DRAINED", { queueName, drained });
  }

  private getOrCreateQueue<T>(name: string): InMemoryQueue<T> {
    let queue = this.queues.get(name);
    if (!queue) {
      queue = { name, messages: [] };
      this.queues.set(name, queue);
    }
    return queue as InMemoryQueue<T>;
  }

  private async maybeDispatch(queueName: string): Promise<void> {
    const queue = this.queues.get(queueName);
    if (!queue || !queue.consumer) return;

    invariant(Array.isArray(queue.messages), "Queue messages must be an array", {
      queueName
    });

    while (queue.messages.length > 0) {
      const msg = queue.messages.shift();
      if (!msg) break;

      metrics.increment("queue_dispatched_total", { queueName });
      witness.log("QUEUE_MESSAGE_DISPATCHED", { queueName, messageId: msg.id });

      try {
        msg.attempts += 1;
        await queue.consumer(msg);
      } catch (err) {
        witness.log(
          "QUEUE_CONSUMER_ERROR",
          { queueName, messageId: msg.id, error: String(err) },
          "ERROR"
        );

        await this.fail(
          msg.id,
          err instanceof Error ? err : new Error(String(err))
        );
      }
    }

    const remaining = queue.messages.length;
    metrics.observe("queue_depth", remaining, { queueName });
  }
}
