import { QueueClient, QueueMessage } from "../../queue/QueueClient";
export declare abstract class BaseQueueAdapter implements QueueClient {
    abstract enqueue<T>(queueName: string, payload: T): Promise<void>;
    abstract registerConsumer<T>(queueName: string, consumer: (msg: QueueMessage<T>) => Promise<void>): Promise<void>;
    abstract ack(messageId: string): Promise<void>;
    abstract fail(messageId: string, error: Error): Promise<void>;
    abstract getQueueSize(queueName: string): Promise<number>;
    abstract peekQueue<T>(queueName: string, limit: number): Promise<QueueMessage<T>[]>;
    abstract drainQueue(queueName: string): Promise<void>;
}
//# sourceMappingURL=BaseQueueAdapter.d.ts.map