"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SqsQueueClient = void 0;
const client_sqs_1 = require("@aws-sdk/client-sqs");
const crypto_1 = require("crypto");
const BaseQueueAdapter_1 = require("./BaseQueueAdapter");
class SqsQueueClient extends BaseQueueAdapter_1.BaseQueueAdapter {
    constructor(config, governanceBus) {
        super();
        this.queueUrl = config.queueUrl;
        this.governanceBus = governanceBus;
        this.sqs = new client_sqs_1.SQSClient({
            region: config.region,
            credentials: config.accessKeyId
                ? {
                    accessKeyId: config.accessKeyId,
                    secretAccessKey: config.secretAccessKey,
                }
                : undefined,
        });
    }
    async enqueue(queueName, payload) {
        await this.sqs.send(new client_sqs_1.SendMessageCommand({
            QueueUrl: this.queueUrl,
            MessageBody: JSON.stringify({
                id: (0, crypto_1.randomUUID)(),
                payload,
                attempts: 0,
                enqueuedAt: new Date().toISOString(),
            }),
        }));
        this.governanceBus?.emitEvent({
            type: "QUEUE_ENQUEUE",
            severity: "INFO",
            timestamp: new Date().toISOString(),
            details: { provider: "SQS", queueUrl: this.queueUrl, queueName },
        });
    }
    async registerConsumer(queueName, consumer) {
        const poll = async () => {
            const response = await this.sqs.send(new client_sqs_1.ReceiveMessageCommand({
                QueueUrl: this.queueUrl,
                MaxNumberOfMessages: 1,
                WaitTimeSeconds: 10,
            }));
            if (response.Messages && response.Messages.length > 0) {
                const raw = response.Messages[0];
                const body = JSON.parse(raw.Body);
                const message = {
                    id: body.id,
                    payload: body.payload,
                    attempts: body.attempts,
                    enqueuedAt: body.enqueuedAt,
                };
                this.governanceBus?.emitEvent({
                    type: "QUEUE_CONSUME",
                    severity: "INFO",
                    timestamp: new Date().toISOString(),
                    details: { provider: "SQS", queueUrl: this.queueUrl, queueName, messageId: message.id },
                });
                try {
                    await consumer(message);
                    await this.ack(raw.ReceiptHandle);
                }
                catch (err) {
                    await this.fail(raw.ReceiptHandle, err);
                }
            }
            setImmediate(poll);
        };
        poll();
    }
    async ack(receiptHandle) {
        await this.sqs.send(new client_sqs_1.DeleteMessageCommand({
            QueueUrl: this.queueUrl,
            ReceiptHandle: receiptHandle,
        }));
        this.governanceBus?.emitEvent({
            type: "QUEUE_ACK",
            severity: "INFO",
            timestamp: new Date().toISOString(),
            details: { provider: "SQS", queueUrl: this.queueUrl, receiptHandle },
        });
    }
    async fail(receiptHandle, error) {
        this.governanceBus?.emitEvent({
            type: "QUEUE_FAIL",
            severity: "WARN",
            timestamp: new Date().toISOString(),
            details: { provider: "SQS", queueUrl: this.queueUrl, receiptHandle, error: error.message },
        });
        // Treat fail as ack for now; future packets may implement DLQ routing.
        await this.ack(receiptHandle);
    }
    async getQueueSize(_queueName) {
        // SQS does not provide exact size; future packet may add CloudWatch integration.
        return 0;
    }
    async peekQueue(_queueName, _limit) {
        // SQS does not support peek; placeholder for future provider-specific logic.
        return [];
    }
    async drainQueue(_queueName) {
        // No native drain; future packet may implement iterative purge.
    }
}
exports.SqsQueueClient = SqsQueueClient;
//# sourceMappingURL=SqsQueueClient.js.map