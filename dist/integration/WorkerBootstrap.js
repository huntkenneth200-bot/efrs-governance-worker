"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkerBootstrap = void 0;
const http_1 = __importDefault(require("http"));
const QueueAdapterRegistry_1 = require("../queue/QueueAdapterRegistry");
const QueueConsumer_1 = require("./QueueConsumer");
const DriftDetector_1 = require("./DriftDetector");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const SchemaBootstrap_1 = require("../validation/SchemaBootstrap");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
const EventLineageStore_1 = require("../lineage/EventLineageStore");
const contracts_1 = require("../contracts");
class WorkerBootstrap {
    constructor(options) {
        this.state = {
            ready: false,
            shuttingDown: false,
            startTime: Date.now()
        };
        this.heartbeatTimer = null;
        this.server = null;
        this.queueClient = options.queueClient;
        this.governanceBus = options.governanceBus;
        this.moduleIntegrator = options.moduleIntegrator;
        this.healthPort = options.healthPort;
        this.heartbeatIntervalMs = options.heartbeatIntervalMs ?? 15000;
        this.queueName = options.queueName ?? "document-events";
    }
    async start() {
        WitnessLogger_1.witness.log("WORKER_INITIALIZING", { healthPort: this.healthPort });
        this.governanceBus.emitEvent({
            type: "WORKER_STARTED",
            severity: "INFO",
            timestamp: new Date().toISOString()
        });
        (0, SchemaBootstrap_1.bootstrapSchemas)();
        (0, QueueAdapterRegistry_1.registerQueueAdapter)("default", this.queueClient);
        (0, DriftDetector_1.runDriftChecks)();
        await this.startHealthServer();
        this.startHeartbeat();
        await (0, QueueConsumer_1.startQueueConsumer)(this.queueName, this.moduleIntegrator);
        this.state.ready = true;
        WitnessLogger_1.witness.log("WORKER_READY", { startedAt: this.state.startTime });
        this.governanceBus.emitEvent({
            type: "WORKER_READY",
            severity: "INFO",
            timestamp: new Date().toISOString()
        });
    }
    async startHealthServer() {
        const healthPort = this.healthPort;
        this.server = http_1.default.createServer(async (req, res) => {
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
                    const envelope = (0, contracts_1.success)({ status: "ok" });
                    res.statusCode = 200;
                    res.setHeader("Content-Type", "application/json");
                    res.end(JSON.stringify(envelope));
                    return;
                }
                if (path === "/ready") {
                    const ready = this.queueClient != null &&
                        this.governanceBus != null &&
                        this.moduleIntegrator != null;
                    const adapterReady = typeof this.queueClient.enqueue === "function" &&
                        typeof this.queueClient.registerConsumer === "function";
                    const envelope = ready && adapterReady
                        ? (0, contracts_1.success)({ status: "ready", adapterReady })
                        : (0, contracts_1.failure)("NOT_READY", "Worker is not ready", {
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
                    res.end(JSON.stringify({
                        version: "1.0.0",
                        startedAt: this.state.startTime
                    }));
                    return;
                }
                if (path === "/lineage" && method === "GET") {
                    const urlSearch = url.searchParams;
                    const documentId = urlSearch.get("documentId");
                    const limitParam = urlSearch.get("limit");
                    const limit = limitParam ? Number(limitParam) : 50;
                    let records;
                    if (documentId) {
                        records = EventLineageStore_1.eventLineageStore.getByDocumentId(documentId);
                    }
                    else {
                        records = EventLineageStore_1.eventLineageStore.getRecent(Number.isNaN(limit) ? 50 : limit);
                    }
                    res.statusCode = 200;
                    res.setHeader("Content-Type", "application/json");
                    res.end(JSON.stringify({ records }));
                    return;
                }
                if (path === "/lineage/recent" && method === "GET") {
                    const limitParam = url.searchParams.get("limit");
                    const limit = limitParam ? Number(limitParam) : 50;
                    const records = EventLineageStore_1.eventLineageStore.getRecent(Number.isNaN(limit) ? 50 : limit);
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
                    const record = EventLineageStore_1.eventLineageStore.getByCorrelationId(correlationId);
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
                        res.end(JSON.stringify({
                            queueName,
                            count: messages.length,
                            messages
                        }));
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
                            const parsed = JSON.parse(body);
                            const response = await this.moduleIntegrator.handleDgeEvaluate(parsed);
                            const envelope = response;
                            res.statusCode = envelope.ok ? 200 : 400;
                            res.setHeader("Content-Type", "application/json");
                            res.end(JSON.stringify(envelope));
                        }
                        catch (err) {
                            const envelope = (0, contracts_1.failure)("INVALID_REQUEST", "Failed to process DGE evaluate request", { error: err.message });
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
                            const parsed = JSON.parse(body);
                            const response = await this.moduleIntegrator.handleLgeResolve(parsed);
                            const envelope = response;
                            res.statusCode = envelope.ok ? 200 : 400;
                            res.setHeader("Content-Type", "application/json");
                            res.end(JSON.stringify(envelope));
                        }
                        catch (err) {
                            const envelope = (0, contracts_1.failure)("INVALID_REQUEST", "Failed to process LGE resolve request", { error: err.message });
                            res.statusCode = 400;
                            res.setHeader("Content-Type", "application/json");
                            res.end(JSON.stringify(envelope));
                        }
                    });
                    return;
                }
                res.statusCode = 404;
                res.end("Not Found");
            }
            catch (err) {
                WitnessLogger_1.witness.log("HEALTH_SERVER_HANDLER_ERROR", { error: String(err) }, "ERROR");
                res.statusCode = 500;
                res.setHeader("Content-Type", "application/json");
                res.end(JSON.stringify({ error: "Internal Server Error" }));
            }
        });
        await new Promise((resolve) => {
            this.server.listen(healthPort, () => {
                WitnessLogger_1.witness.log("WORKER_HEALTH_SERVER_STARTED", { port: healthPort });
                resolve();
            });
        });
    }
    startHeartbeat() {
        this.heartbeatTimer = setInterval(() => {
            MetricsRegistry_1.metrics.increment("worker_heartbeat_total", { source: "WorkerBootstrap" });
            WitnessLogger_1.witness.log("WORKER_HEARTBEAT", {
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
    async shutdown() {
        if (this.state.shuttingDown)
            return;
        this.state.shuttingDown = true;
        WitnessLogger_1.witness.log("WORKER_SHUTDOWN_INITIATED", {});
        MetricsRegistry_1.metrics.increment("worker_shutdown_total");
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
        if (this.server) {
            await new Promise((resolve) => {
                this.server.close(() => {
                    WitnessLogger_1.witness.log("WORKER_HEALTH_SERVER_STOPPED", {});
                    resolve();
                });
            });
        }
        this.governanceBus.emitEvent({
            type: "WORKER_SHUTDOWN",
            severity: "INFO",
            timestamp: new Date().toISOString()
        });
        WitnessLogger_1.witness.log("WORKER_SHUTDOWN_COMPLETED", {});
    }
}
exports.WorkerBootstrap = WorkerBootstrap;
//# sourceMappingURL=WorkerBootstrap.js.map