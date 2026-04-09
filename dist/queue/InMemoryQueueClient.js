"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.InMemoryQueueClient = void 0;
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
const Invariant_1 = require("../invariants/Invariant");
const InvariantViolation_1 = require("../invariants/InvariantViolation");
class InMemoryQueueClient {
    constructor() {
        this.queues = new Map();
    }
    async enqueue(queueName, payload) {
        (0, Invariant_1.invariant)(typeof queueName === "string" && queueName.length > 0, "enqueue: queueName must be non-empty", {
            queueName
        });
        (0, Invariant_1.invariant)(payload !== undefined, "enqueue: payload must not be undefined", {
            queueName
        });
        const queue = this.getOrCreateQueue(queueName);
        const message = {
            id: `${queueName}-${Date.now()}-${Math.random().toString(16).slice(2)}`,
            payload,
            attempts: 0,
            enqueuedAt: Date.now()
        };
        queue.messages.push(message);
        MetricsRegistry_1.metrics.increment("queue_enqueued_total", { queueName });
        WitnessLogger_1.witness.log("QUEUE_ENQUEUED", { queueName, messageId: message.id });
        const size = queue.messages.length;
        MetricsRegistry_1.metrics.observe("queue_depth", size, { queueName });
        this.maybeDispatch(queueName);
    }
    async registerConsumer(queueName, consumer) {
        const queue = this.getOrCreateQueue(queueName);
        queue.consumer = consumer;
        WitnessLogger_1.witness.log("QUEUE_CONSUMER_REGISTERED", { queueName });
        this.maybeDispatch(queueName);
    }
    async ack(messageId) {
        (0, Invariant_1.invariant)(typeof messageId === "string" && messageId.length > 0, "ack: messageId must be a non-empty string", { messageId });
        WitnessLogger_1.witness.log("QUEUE_MESSAGE_ACK", { messageId }, "INFO");
        MetricsRegistry_1.metrics.increment("queue_message_ack_total", { messageId });
    }
    async fail(messageId, error) {
        (0, Invariant_1.invariant)(typeof messageId === "string" && messageId.length > 0, "fail: messageId must be a non-empty string", { messageId });
        WitnessLogger_1.witness.log("QUEUE_MESSAGE_FAIL", {
            messageId,
            error: String(error),
            invariantViolation: error instanceof InvariantViolation_1.InvariantViolation
        }, "WARN");
        MetricsRegistry_1.metrics.increment("queue_message_fail_total", { messageId });
    }
    async getQueueSize(queueName) {
        (0, Invariant_1.invariant)(typeof queueName === "string" && queueName.length > 0, "getQueueSize: queueName must be non-empty", { queueName });
        const queue = this.queues.get(queueName);
        return queue ? queue.messages.length : 0;
    }
    async peekQueue(queueName, limit = 10) {
        (0, Invariant_1.invariant)(typeof queueName === "string" && queueName.length > 0, "peekQueue: queueName must be non-empty", { queueName });
        (0, Invariant_1.invariant)(typeof limit === "number" && limit > 0, "peekQueue: limit must be a positive number", { limit });
        const queue = this.queues.get(queueName);
        if (!queue)
            return [];
        return queue.messages.slice(0, limit);
    }
    async drainQueue(queueName) {
        (0, Invariant_1.invariant)(typeof queueName === "string" && queueName.length > 0, "drainQueue: queueName must be non-empty", { queueName });
        const queue = this.queues.get(queueName);
        if (!queue)
            return;
        const drained = queue.messages.length;
        queue.messages = [];
        WitnessLogger_1.witness.log("QUEUE_DRAINED", { queueName, drained });
    }
    getOrCreateQueue(name) {
        let queue = this.queues.get(name);
        if (!queue) {
            queue = { name, messages: [] };
            this.queues.set(name, queue);
        }
        return queue;
    }
    async maybeDispatch(queueName) {
        const queue = this.queues.get(queueName);
        if (!queue || !queue.consumer)
            return;
        (0, Invariant_1.invariant)(Array.isArray(queue.messages), "Queue messages must be an array", {
            queueName
        });
        while (queue.messages.length > 0) {
            const msg = queue.messages.shift();
            if (!msg)
                break;
            MetricsRegistry_1.metrics.increment("queue_dispatched_total", { queueName });
            WitnessLogger_1.witness.log("QUEUE_MESSAGE_DISPATCHED", { queueName, messageId: msg.id });
            try {
                msg.attempts += 1;
                await queue.consumer(msg);
            }
            catch (err) {
                WitnessLogger_1.witness.log("QUEUE_CONSUMER_ERROR", { queueName, messageId: msg.id, error: String(err) }, "ERROR");
                await this.fail(msg.id, err instanceof Error ? err : new Error(String(err)));
            }
        }
        const remaining = queue.messages.length;
        MetricsRegistry_1.metrics.observe("queue_depth", remaining, { queueName });
    }
}
exports.InMemoryQueueClient = InMemoryQueueClient;
//# sourceMappingURL=InMemoryQueueClient.js.map