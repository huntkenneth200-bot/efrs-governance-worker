import { QueueClient, QueueMessage } from "./QueueClient";
export declare class InMemoryQueueClient implements QueueClient {
    private queues;
    enqueue<T>(queueName: string, payload: T): Promise<void>;
    registerConsumer<T>(queueName: string, consumer: (msg: QueueMessage<T>) => Promise<void>): Promise<void>;
    ack(messageId: string): Promise<void>;
    fail(messageId: string, error: Error): Promise<void>;
    getQueueSize(queueName: string): Promise<number>;
    peekQueue<T = unknown>(queueName: string, limit?: number): Promise<QueueMessage<T>[]>;
    drainQueue(queueName: string): Promise<void>;
    private getOrCreateQueue;
    private maybeDispatch;
}
//# sourceMappingURL=InMemoryQueueClient.d.ts.map