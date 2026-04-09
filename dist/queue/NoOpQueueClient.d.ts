import { QueueClient, QueueMessage } from "./QueueClient";
export declare class NoOpQueueClient implements QueueClient {
    enqueue<T>(_queueName: string, _payload: T): Promise<void>;
    registerConsumer<T>(_queueName: string, _consumer: (msg: QueueMessage<T>) => Promise<void>): Promise<void>;
    ack(_messageId: string): Promise<void>;
    fail(_messageId: string, _error: Error): Promise<void>;
    getQueueSize(_queueName: string): Promise<number>;
    peekQueue<T = unknown>(_queueName: string, _limit: number): Promise<QueueMessage<T>[]>;
    drainQueue(_queueName: string): Promise<void>;
}
//# sourceMappingURL=NoOpQueueClient.d.ts.map