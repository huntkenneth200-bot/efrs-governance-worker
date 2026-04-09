export interface QueueAdapterConfig {
    provider: "SQS" | "AZURE" | "GCP";
    queueUrl: string;
    region?: string;
    accessKeyId?: string;
    secretAccessKey?: string;
    connectionString?: string;
}
//# sourceMappingURL=types.d.ts.map