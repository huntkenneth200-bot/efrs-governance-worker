import { QueueAdapterConfig } from "../adapters/queue/types";

export function loadQueueConfig(): QueueAdapterConfig {
  const queueUrl = process.env.QUEUE_URL ?? "";

  const queueConfig: QueueAdapterConfig = {
    provider: (process.env.QUEUE_PROVIDER as QueueAdapterConfig["provider"]) ?? "SQS",
    queueUrl,
    region: process.env.AWS_REGION ?? "",
    accessKeyId: process.env.AWS_ACCESS_KEY_ID ?? "",
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY ?? "",
  };

  console.log("QUEUE CONFIG DEBUG", queueConfig);

  return queueConfig;
}
