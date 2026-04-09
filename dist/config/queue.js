"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadQueueConfig = loadQueueConfig;
function loadQueueConfig() {
    const queueUrl = process.env.QUEUE_URL ?? "";
    const queueConfig = {
        provider: process.env.QUEUE_PROVIDER ?? "SQS",
        queueUrl,
        region: process.env.AWS_REGION ?? "",
        accessKeyId: process.env.AWS_ACCESS_KEY_ID ?? "",
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY ?? "",
    };
    console.log("QUEUE CONFIG DEBUG", queueConfig);
    return queueConfig;
}
//# sourceMappingURL=queue.js.map