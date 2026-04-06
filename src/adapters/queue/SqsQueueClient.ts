import {
  SQSClient,
  SendMessageCommand,
  ReceiveMessageCommand,
  DeleteMessageCommand,
} from "@aws-sdk/client-sqs";
import { randomUUID } from "crypto";
import { BaseQueueAdapter } from "./BaseQueueAdapter";
import { QueueMessage } from "../../queue/QueueClient";
import { QueueAdapterConfig } from "./types";
import type { GovernanceBus } from "../../governance/GovernanceBus";

export class SqsQueueClient extends BaseQueueAdapter {
  private readonly sqs: SQSClient;
  private readonly queueUrl: string;
  private readonly governanceBus?: GovernanceBus;

  constructor(config: QueueAdapterConfig, governanceBus?: GovernanceBus) {
    super();
    this.queueUrl = config.queueUrl;
    this.governanceBus = governanceBus;

    this.sqs = new SQSClient({
      region: config.region,
      credentials: config.accessKeyId
        ? {
            accessKeyId: config.accessKeyId,
            secretAccessKey: config.secretAccessKey!,
          }
        : undefined,
    });
  }

  async enqueue<T>(queueName: string, payload: T): Promise<void> {
    await this.sqs.send(
      new SendMessageCommand({
        QueueUrl: this.queueUrl,
        MessageBody: JSON.stringify({
          id: randomUUID(),
          payload,
          attempts: 0,
          enqueuedAt: new Date().toISOString(),
        }),
      })
    );

    this.governanceBus?.emitEvent({
      type: "QUEUE_ENQUEUE",
      severity: "INFO",
      timestamp: new Date().toISOString(),
      details: { provider: "SQS", queueUrl: this.queueUrl, queueName },
    });
  }

  async registerConsumer<T>(
    queueName: string,
    consumer: (msg: QueueMessage<T>) => Promise<void>
  ): Promise<void> {
    const poll = async () => {
      const response = await this.sqs.send(
        new ReceiveMessageCommand({
          QueueUrl: this.queueUrl,
          MaxNumberOfMessages: 1,
          WaitTimeSeconds: 10,
        })
      );

      if (response.Messages && response.Messages.length > 0) {
        const raw = response.Messages[0];
        const body = JSON.parse(raw.Body!);
        const message: QueueMessage<T> = {
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
          await this.ack(raw.ReceiptHandle!);
        } catch (err) {
          await this.fail(raw.ReceiptHandle!, err as Error);
        }
      }

      setImmediate(poll);
    };

    poll();
  }

  async ack(receiptHandle: string): Promise<void> {
    await this.sqs.send(
      new DeleteMessageCommand({
        QueueUrl: this.queueUrl,
        ReceiptHandle: receiptHandle,
      })
    );

    this.governanceBus?.emitEvent({
      type: "QUEUE_ACK",
      severity: "INFO",
      timestamp: new Date().toISOString(),
      details: { provider: "SQS", queueUrl: this.queueUrl, receiptHandle },
    });
  }

  async fail(receiptHandle: string, error: Error): Promise<void> {
    this.governanceBus?.emitEvent({
      type: "QUEUE_FAIL",
      severity: "WARN",
      timestamp: new Date().toISOString(),
      details: { provider: "SQS", queueUrl: this.queueUrl, receiptHandle, error: error.message },
    });

    // Treat fail as ack for now; future packets may implement DLQ routing.
    await this.ack(receiptHandle);
  }

  async getQueueSize(_queueName: string): Promise<number> {
    // SQS does not provide exact size; future packet may add CloudWatch integration.
    return 0;
  }

  async peekQueue<T>(_queueName: string, _limit: number): Promise<QueueMessage<T>[]> {
    // SQS does not support peek; placeholder for future provider-specific logic.
    return [];
  }

  async drainQueue(_queueName: string): Promise<void> {
    // No native drain; future packet may implement iterative purge.
  }
}
