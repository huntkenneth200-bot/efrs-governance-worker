import { QueueClient } from "./QueueClient";

type QueueAdapterMap = Map<string, QueueClient>;

const registry: QueueAdapterMap = new Map();

export function registerQueueAdapter(name: string, adapter: QueueClient) {
  registry.set(name, adapter);
}

export function getQueueAdapter(name: string): QueueClient {
  const adapter = registry.get(name);
  if (!adapter) throw new Error(`Queue adapter not registered: ${name}`);
  return adapter;
}
