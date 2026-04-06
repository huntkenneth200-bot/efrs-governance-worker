import { QueueClient, QueueMessage } from "./QueueClient";

export class NoOpQueueClient implements QueueClient {
  async enqueue<T>(_queueName: string, _payload: T): Promise<void> {}
  async registerConsumer<T>(_queueName: string, _consumer: (msg: QueueMessage<T>) => Promise<void>): Promise<void> {}
  async ack(_messageId: string): Promise<void> {}
  async fail(_messageId: string, _error: Error): Promise<void> {}
  async getQueueSize(_queueName: string): Promise<number> { return 0; }
  async peekQueue<T = unknown>(_queueName: string, _limit: number): Promise<QueueMessage<T>[]> { return []; }
  async drainQueue(_queueName: string): Promise<void> {}
}
