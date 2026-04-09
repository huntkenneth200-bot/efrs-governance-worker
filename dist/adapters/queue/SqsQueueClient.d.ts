import { BaseQueueAdapter } from "./BaseQueueAdapter";
import { QueueMessage } from "../../queue/QueueClient";
import { QueueAdapterConfig } from "./types";
import type { GovernanceBus } from "../../governance/GovernanceBus";
export declare class SqsQueueClient extends BaseQueueAdapter {
    private readonly sqs;
    private readonly queueUrl;
    private readonly governanceBus?;
    constructor(config: QueueAdapterConfig, governanceBus?: GovernanceBus);
    enqueue<T>(queueName: string, payload: T): Promise<void>;
    registerConsumer<T>(queueName: string, consumer: (msg: QueueMessage<T>) => Promise<void>): Promise<void>;
    ack(receiptHandle: string): Promise<void>;
    fail(receiptHandle: string, error: Error): Promise<void>;
    getQueueSize(_queueName: string): Promise<number>;
    peekQueue<T>(_queueName: string, _limit: number): Promise<QueueMessage<T>[]>;
    drainQueue(_queueName: string): Promise<void>;
}
//# sourceMappingURL=SqsQueueClient.d.ts.map