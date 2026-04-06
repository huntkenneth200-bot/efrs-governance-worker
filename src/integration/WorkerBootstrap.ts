import http from "http";
import { registerQueueAdapter } from "../queue/QueueAdapterRegistry";
import { QueueClient } from "../queue/QueueClient";
import { GovernanceBus } from "../governance/GovernanceBus";
import { ModuleIntegrator } from "./ModuleIntegrator";
import { startQueueConsumer } from "./QueueConsumer";
import { runDriftChecks } from "./DriftDetector";
import { witness } from "../logging/WitnessLogger";
import { bootstrapSchemas } from "../validation/SchemaBootstrap";
import { metrics } from "../metrics/MetricsRegistry";
import { eventLineageStore } from "../lineage/EventLineageStore";
import { success, failure, ApiResponse } from "../contracts";
import type { DgeEvaluateRequest, DgeEvaluateResult } from "../dge/DGEClient";
import type { LgeLexiconRequest, LgeLexiconResult } from "../lge/LGEClient";

interface WorkerState {
  ready: boolean;
  shuttingDown: boolean;
  startTime: number;
}

export class WorkerBootstrap {
  private readonly queueClient: QueueClient;
  private readonly governanceBus: GovernanceBus;
  private readonly moduleIntegrator: ModuleIntegrator;
  private readonly healthPort: number;
  private readonly heartbeatIntervalMs: number;
  private readonly queueName: string;

  private state: WorkerState = {
    ready: false,
    shuttingDown: false,
    startTime: Date.now()
  };

  private heartbeatTimer: NodeJS.Timeout | null = null;
  private server: http.Server | null = null;

  constructor(options: {
    queueClient: QueueClient;
    governanceBus: GovernanceBus;
    moduleIntegrator: ModuleIntegrator;
    healthPort: number;
    heartbeatIntervalMs?: number;
    queueName?: string;
  }) {
    this.queueClient = options.queueClient;
    this.governanceBus = options.governanceBus;
    this.moduleIntegrator = options.moduleIntegrator;
    this.healthPort = options.healthPort;
    this.heartbeatIntervalMs = options.heartbeatIntervalMs ?? 15000;
    this.queueName = options.queueName ?? "document-events";
  }

  async start(): Promise<void> {
    witness.log("WORKER_INITIALIZING", { healthPort: this.healthPort });
    this.governanceBus.emitEvent({
      type: "WORKER_STARTED",
      severity: "INFO",
      timestamp: new Date().toISOString()
    });

    bootstrapSchemas();
    registerQueueAdapter("default", this.queueClient);
    runDriftChecks();

    await this.startHealthServer();
    this.startHeartbeat();

    await startQueueConsumer(this.queueName, this.moduleIntegrator);

    this.state.ready = true;
    witness.log("WORKER_READY", { startedAt: this.state.startTime });
    this.governanceBus.emitEvent({
      type: "WORKER_READY",
      severity: "INFO",
      timestamp: new Date().toISOString()
    });
  }

  private async startHealthServer(): Promise<void> {
    const healthPort = this.healthPort;

    this.server = http.createServer(async (req, res) => {
      try {
        if (!req.url) {
          res.statusCode = 400;
          res.end("Bad Request");
          return;
        }

        const url = new URL(req.url, `http://localhost:${healthPort}`);
        const path = url.pathname;
        const method = req.method ?? "";

        if (path === "/health") {
          const envelope = success({ status: "ok" });
          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify(envelope));
          return;
        }

        if (path === "/ready") {
          const ready =
            this.queueClient != null &&
            this.governanceBus != null &&
            this.moduleIntegrator != null;

          const adapterReady =
            typeof this.queueClient.enqueue === "function" &&
            typeof this.queueClient.registerConsumer === "function";

          const envelope = ready && adapterReady
            ? success({ status: "ready", adapterReady })
            : failure("NOT_READY", "Worker is not ready", {
                queueClient: this.queueClient != null,
                governanceBus: this.governanceBus != null,
                moduleIntegrator: this.moduleIntegrator != null,
                adapterReady
              });

          res.statusCode = ready && adapterReady ? 200 : 503;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify(envelope));
          return;
        }

        if (path === "/version") {
          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(
            JSON.stringify({
              version: "1.0.0",
              startedAt: this.state.startTime
            })
          );
          return;
        }

        if (path === "/lineage" && method === "GET") {
          const urlSearch = url.searchParams;
          const documentId = urlSearch.get("documentId");
          const limitParam = urlSearch.get("limit");
          const limit = limitParam ? Number(limitParam) : 50;

          let records;
          if (documentId) {
            records = eventLineageStore.getByDocumentId(documentId);
          } else {
            records = eventLineageStore.getRecent(Number.isNaN(limit) ? 50 : limit);
          }

          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ records }));
          return;
        }

        if (path === "/lineage/recent" && method === "GET") {
          const limitParam = url.searchParams.get("limit");
          const limit = limitParam ? Number(limitParam) : 50;
          const records = eventLineageStore.getRecent(Number.isNaN(limit) ? 50 : limit);
          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ count: records.length, records }));
          return;
        }

        if (path.startsWith("/lineage/") && method === "GET") {
          const segments = path.split("/").filter(Boolean); // ["lineage", "<id>"]
          const correlationId = segments[1];

          if (!correlationId) {
            res.statusCode = 400;
            res.end("Correlation ID required");
            return;
          }

          const record = eventLineageStore.getByCorrelationId(correlationId);
          if (!record) {
            res.statusCode = 404;
            res.setHeader("Content-Type", "application/json");
            res.end(JSON.stringify({ error: "Lineage record not found" }));
            return;
          }

          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify(record));
          return;
        }

        if (path.startsWith("/queue/")) {
          const segments = path.split("/").filter(Boolean); // ["queue", "<name>", ...]
          const queueName = segments[1];

          if (!queueName) {
            res.statusCode = 400;
            res.end("Queue name required");
            return;
          }

          if (segments.length === 3 && segments[2] === "size" && method === "GET") {
            const size = await this.queueClient.getQueueSize(queueName);
            res.statusCode = 200;
            res.setHeader("Content-Type", "application/json");
            res.end(JSON.stringify({ queueName, size }));
            return;
          }

          if (segments.length === 3 && segments[2] === "peek" && method === "GET") {
            const limitParam = url.searchParams.get("limit");
            const limit = limitParam ? Number(limitParam) : 10;
            const messages = await this.queueClient.peekQueue(queueName, Number.isNaN(limit) ? 10 : limit);
            res.statusCode = 200;
            res.setHeader("Content-Type", "application/json");
            res.end(
              JSON.stringify({
                queueName,
                count: messages.length,
                messages
              })
            );
            return;
          }

          if (segments.length === 3 && segments[2] === "drain" && method === "POST") {
            await this.queueClient.drainQueue(queueName);
            res.statusCode = 200;
            res.setHeader("Content-Type", "application/json");
            res.end(JSON.stringify({ queueName, drained: true }));
            return;
          }
        }

        if (method === "POST" && path === "/dge/evaluate") {
          let body = "";
          req.on("data", (chunk) => {
            body += chunk;
          });
          req.on("end", async () => {
            try {
              const parsed = JSON.parse(body) as DgeEvaluateRequest;
              const response = await this.moduleIntegrator.handleDgeEvaluate(parsed);
              const envelope: ApiResponse<DgeEvaluateResult> = response;
              res.statusCode = envelope.ok ? 200 : 400;
              res.setHeader("Content-Type", "application/json");
              res.end(JSON.stringify(envelope));
            } catch (err) {
              const envelope = failure(
                "INVALID_REQUEST",
                "Failed to process DGE evaluate request",
                { error: (err as Error).message }
              );
              res.statusCode = 400;
              res.setHeader("Content-Type", "application/json");
              res.end(JSON.stringify(envelope));
            }
          });
          return;
        }

        if (method === "POST" && path === "/lge/resolve") {
          let body = "";
          req.on("data", (chunk) => {
            body += chunk;
          });
          req.on("end", async () => {
            try {
              const parsed = JSON.parse(body) as LgeLexiconRequest;
              const response = await this.moduleIntegrator.handleLgeResolve(parsed);
              const envelope: ApiResponse<LgeLexiconResult> = response;
              res.statusCode = envelope.ok ? 200 : 400;
              res.setHeader("Content-Type", "application/json");
              res.end(JSON.stringify(envelope));
            } catch (err) {
              const envelope = failure(
                "INVALID_REQUEST",
                "Failed to process LGE resolve request",
                { error: (err as Error).message }
              );
              res.statusCode = 400;
              res.setHeader("Content-Type", "application/json");
              res.end(JSON.stringify(envelope));
            }
          });
          return;
        }

        res.statusCode = 404;
        res.end("Not Found");
      } catch (err) {
        witness.log(
          "HEALTH_SERVER_HANDLER_ERROR",
          { error: String(err) },
          "ERROR"
        );
        res.statusCode = 500;
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify({ error: "Internal Server Error" }));
      }
    });

    await new Promise<void>((resolve) => {
      this.server!.listen(healthPort, () => {
        witness.log("WORKER_HEALTH_SERVER_STARTED", { port: healthPort });
        resolve();
      });
    });
  }

  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      metrics.increment("worker_heartbeat_total", { source: "WorkerBootstrap" });
      witness.log("WORKER_HEARTBEAT", {
        uptimeMs: Date.now() - this.state.startTime
      });
      this.governanceBus.emitEvent({
        type: "WORKER_HEARTBEAT",
        severity: "INFO",
        timestamp: new Date().toISOString(),
        id: "WORKER_HEARTBEAT"
      });
    }, this.heartbeatIntervalMs);
  }

  async shutdown(): Promise<void> {
    if (this.state.shuttingDown) return;
    this.state.shuttingDown = true;

    witness.log("WORKER_SHUTDOWN_INITIATED", {});
    metrics.increment("worker_shutdown_total");

    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }

    if (this.server) {
      await new Promise<void>((resolve) => {
        this.server!.close(() => {
          witness.log("WORKER_HEALTH_SERVER_STOPPED", {});
          resolve();
        });
      });
    }

    this.governanceBus.emitEvent({
      type: "WORKER_SHUTDOWN",
      severity: "INFO",
      timestamp: new Date().toISOString()
    });

    witness.log("WORKER_SHUTDOWN_COMPLETED", {});
  }
}
