"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DGEClient = void 0;
const ValidatorFactory_1 = require("../validation/ValidatorFactory");
const RetryEnvelope_1 = require("../retry/RetryEnvelope");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
const GovernanceSignalBus_1 = require("../governance/GovernanceSignalBus");
const DGESimEngine_1 = require("./DGESimEngine");
const contracts_1 = require("../contracts");
const DGE_REQUEST_SCHEMA_NAME = "DGEProcessRequest";
const DGE_RESPONSE_SCHEMA_NAME = "DGEProcessResponse";
class DGEClient {
    constructor(options = {}) {
        this.endpoint = options.endpoint ?? "http://dge.local/process";
        const rawMode = options.mode ??
            process.env.DGE_SIM_MODE ??
            "NORMAL";
        const mode = rawMode === "NORMAL" ||
            rawMode === "ALWAYS_FAIL" ||
            rawMode === "RANDOM_FAILURE"
            ? rawMode
            : "NORMAL";
        this.simEngineMode = mode;
        let failureRate = options.failureRate ??
            (process.env.DGE_SIM_FAILURE_RATE
                ? Number(process.env.DGE_SIM_FAILURE_RATE)
                : undefined);
        if (failureRate === undefined ||
            Number.isNaN(failureRate) ||
            failureRate < 0 ||
            failureRate > 1) {
            failureRate = 0.2;
        }
        const latency = options.latencyMs ?? 0;
        this.latencyMs = latency < 0 ? 0 : latency;
        this.simEngine = new DGESimEngine_1.DGESimEngine({ mode, failureRate });
    }
    async process(request) {
        MetricsRegistry_1.metrics.increment("dge_requests_total", { endpoint: this.endpoint });
        WitnessLogger_1.witness.log("DGE_REQUEST_INITIATED", { request, endpoint: this.endpoint });
        const validatedRequest = (0, ValidatorFactory_1.validateOrThrow)(DGE_REQUEST_SCHEMA_NAME, request);
        return (0, RetryEnvelope_1.withRetry)(async () => {
            const timerName = "dge_request_duration_ms";
            MetricsRegistry_1.metrics.startTimer(timerName, { endpoint: this.endpoint });
            if (this.latencyMs > 0) {
                await new Promise((resolve) => setTimeout(resolve, this.latencyMs));
            }
            const startedAt = Date.now();
            const simulatedResponse = this.simEngine.process(validatedRequest);
            const completedAt = Date.now();
            const durationMs = completedAt - startedAt;
            MetricsRegistry_1.metrics.observe("dge_call_latency_ms", durationMs, {
                mode: this.simEngineMode,
                status: simulatedResponse.status
            });
            const duration = MetricsRegistry_1.metrics.endTimer(timerName, { endpoint: this.endpoint });
            WitnessLogger_1.witness.log("DGE_REQUEST_COMPLETED", {
                duration,
                response: simulatedResponse,
                endpoint: this.endpoint
            });
            const validatedResponse = (0, ValidatorFactory_1.validateOrThrow)(DGE_RESPONSE_SCHEMA_NAME, simulatedResponse);
            GovernanceSignalBus_1.governanceBus.emitEvent({
                type: "MESSAGE_PROCESSED",
                severity: "INFO",
                timestamp: new Date().toISOString(),
                id: validatedResponse.documentId,
                details: {
                    engine: "DGE",
                    status: validatedResponse.status
                }
            });
            return validatedResponse;
        });
    }
    async evaluate(request) {
        try {
            const processResult = await this.process({
                documentId: `${request.tenantId}:${request.documentType}`,
                tenantId: request.tenantId,
                eventType: request.documentType,
                // ⭐ FIXED: cast payload to match DGEProcessRequest
                payload: request.payload,
                occurredAt: new Date().toISOString()
            });
            const decision = processResult.status === "ACCEPTED" ? "ALLOW" :
                processResult.status === "REJECTED" ? "DENY" :
                    "REVIEW";
            return (0, contracts_1.success)({
                tenantId: processResult.tenantId,
                documentType: request.documentType,
                decision,
                reasons: processResult.reason ? [processResult.reason] : [],
                version: "v1"
            });
        }
        catch (err) {
            return (0, contracts_1.failure)("DGE_EVALUATE_ERROR", err instanceof Error ? err.message : String(err));
        }
    }
}
exports.DGEClient = DGEClient;
//# sourceMappingURL=DGEClient.js.map