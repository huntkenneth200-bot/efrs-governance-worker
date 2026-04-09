import { QueueClient } from "../queue/QueueClient";
import { GovernanceBus } from "../governance/GovernanceBus";
import { ModuleIntegrator } from "./ModuleIntegrator";
export declare class WorkerBootstrap {
    private readonly queueClient;
    private readonly governanceBus;
    private readonly moduleIntegrator;
    private readonly healthPort;
    private readonly heartbeatIntervalMs;
    private readonly queueName;
    private state;
    private heartbeatTimer;
    private server;
    constructor(options: {
        queueClient: QueueClient;
        governanceBus: GovernanceBus;
        moduleIntegrator: ModuleIntegrator;
        healthPort: number;
        heartbeatIntervalMs?: number;
        queueName?: string;
    });
    start(): Promise<void>;
    private startHealthServer;
    private startHeartbeat;
    shutdown(): Promise<void>;
}
//# sourceMappingURL=WorkerBootstrap.d.ts.map