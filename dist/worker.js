"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const queue_1 = require("./config/queue");
const SqsQueueClient_1 = require("./adapters/queue/SqsQueueClient");
const GovernanceSignalBus_1 = require("./governance/GovernanceSignalBus");
const ModuleIntegrator_1 = require("./integration/ModuleIntegrator");
const WorkerBootstrap_1 = require("./integration/WorkerBootstrap");
const DGEClient_1 = require("./engines/DGEClient");
const LGEClient_1 = require("./engines/LGEClient");
const WitnessLogger_1 = require("./logging/WitnessLogger");
console.log("ENV_DEBUG", {
    QUEUE_PROVIDER: process.env.QUEUE_PROVIDER,
    QUEUE_URL: process.env.QUEUE_URL,
    AWS_REGION: process.env.AWS_REGION,
    AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID ? "SET" : "MISSING",
    AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY ? "SET" : "MISSING",
});
async function main() {
    const queueConfig = (0, queue_1.loadQueueConfig)();
    const queueClient = new SqsQueueClient_1.SqsQueueClient(queueConfig);
    const moduleIntegrator = new ModuleIntegrator_1.ModuleIntegrator({
        governanceBus: GovernanceSignalBus_1.governanceBus,
        dgeClient: new DGEClient_1.DGEClient(),
        lgeClient: new LGEClient_1.LGEClient(),
    });
    const worker = new WorkerBootstrap_1.WorkerBootstrap({
        queueClient,
        governanceBus: GovernanceSignalBus_1.governanceBus,
        moduleIntegrator,
        healthPort: Number(process.env.HEALTH_PORT ?? 3000),
        heartbeatIntervalMs: Number(process.env.HEARTBEAT_INTERVAL_MS ?? 5000),
        queueName: process.env.QUEUE_NAME ?? "efrs-tasks",
    });
    process.on("SIGINT", async () => {
        WitnessLogger_1.witness.log("WORKER_SIGNAL_RECEIVED", { signal: "SIGINT" });
        await worker.shutdown();
        process.exit(0);
    });
    process.on("SIGTERM", async () => {
        WitnessLogger_1.witness.log("WORKER_SIGNAL_RECEIVED", { signal: "SIGTERM" });
        await worker.shutdown();
        process.exit(0);
    });
    await worker.start();
}
main().catch((err) => {
    WitnessLogger_1.witness.log("WORKER_FATAL_ERROR", { error: String(err) });
    process.exit(1);
});
//# sourceMappingURL=worker.js.map