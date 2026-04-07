import { loadQueueConfig } from "./config/queue";
import { SqsQueueClient } from "./adapters/queue/SqsQueueClient";
import { InMemoryGovernanceBus } from "./governance/GovernanceBus";
import { ModuleIntegrator } from "./integration/ModuleIntegrator";
import { WorkerBootstrap } from "./integration/WorkerBootstrap";
import { DGEClient } from "./engines/DGEClient";
import { LGEClient } from "./engines/LGEClient";
import { witness } from "./logging/WitnessLogger";

async function main() {
  const queueConfig = loadQueueConfig();
  const queueClient = new SqsQueueClient(queueConfig);
  const governanceBus = new InMemoryGovernanceBus();

  const moduleIntegrator = new ModuleIntegrator({
    governanceBus,
    dgeClient: new DGEClient(),
    lgeClient: new LGEClient(),
  });

  const worker = new WorkerBootstrap({
    queueClient,
    governanceBus,
    moduleIntegrator,
    healthPort: Number(process.env.HEALTH_PORT ?? 3000),
    heartbeatIntervalMs: Number(process.env.HEARTBEAT_INTERVAL_MS ?? 5000),
    queueName: process.env.QUEUE_NAME ?? "efrs-tasks",
  });

  process.on("SIGINT", async () => {
    witness.log("WORKER_SIGNAL_RECEIVED", { signal: "SIGINT" });
    await worker.shutdown();
    process.exit(0);
  });

  process.on("SIGTERM", async () => {
    witness.log("WORKER_SIGNAL_RECEIVED", { signal: "SIGTERM" });
    await worker.shutdown();
    process.exit(0);
  });

  await worker.start();
}

main().catch((err) => {
  witness.log("WORKER_FATAL_ERROR", { error: String(err) });
  process.exit(1);
});
