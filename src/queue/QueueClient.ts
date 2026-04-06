export interface QueueMessage<T = unknown> {
  id: string;
  payload: T;
  attempts: number;
  enqueuedAt: number;
}

export interface QueueClient {
  enqueue<T>(queueName: string, payload: T): Promise<void>;
  registerConsumer<T>(
    queueName: string,
    consumer: (msg: QueueMessage<T>) => Promise<void>
  ): Promise<void>;
  ack(messageId: string): Promise<void>;
  fail(messageId: string, error: Error): Promise<void>;

  // Introspection / health
  getQueueSize(queueName: string): Promise<number>;
  peekQueue<T>(queueName: string, limit: number): Promise<QueueMessage<T>[]>;
  drainQueue(queueName: string): Promise<void>;
}
