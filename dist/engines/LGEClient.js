"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LGEClient = void 0;
const ValidatorFactory_1 = require("../validation/ValidatorFactory");
const RetryEnvelope_1 = require("../retry/RetryEnvelope");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
const GovernanceSignalBus_1 = require("../governance/GovernanceSignalBus");
const LGESimEngine_1 = require("./LGESimEngine");
const contracts_1 = require("../contracts");
const LGE_REQUEST_SCHEMA_NAME = "LGEUpdateRequest";
const LGE_RESPONSE_SCHEMA_NAME = "LGEUpdateResponse";
class LGEClient {
    constructor(options = {}) {
        this.endpoint = options.endpoint ?? "http://lge.local/update";
        const rawMode = options.mode ??
            process.env.LGE_SIM_MODE ??
            "NORMAL";
        const mode = rawMode === "NORMAL" ||
            rawMode === "ALWAYS_FAIL" ||
            rawMode === "RANDOM_FAILURE"
            ? rawMode
            : "NORMAL";
        this.simEngineMode = mode;
        let failureRate = options.failureRate ??
            (process.env.LGE_SIM_FAILURE_RATE
                ? Number(process.env.LGE_SIM_FAILURE_RATE)
                : undefined);
        if (failureRate === undefined ||
            Number.isNaN(failureRate) ||
            failureRate < 0 ||
            failureRate > 1) {
            failureRate = 0.2;
        }
        const latency = options.latencyMs ?? 0;
        this.latencyMs = latency < 0 ? 0 : latency;
        this.simEngine = new LGESimEngine_1.LGESimEngine({ mode, failureRate });
    }
    async update(request) {
        MetricsRegistry_1.metrics.increment("lge_requests_total", { endpoint: this.endpoint });
        WitnessLogger_1.witness.log("LGE_REQUEST_INITIATED", { request, endpoint: this.endpoint });
        const validatedRequest = (0, ValidatorFactory_1.validateOrThrow)(LGE_REQUEST_SCHEMA_NAME, request);
        return (0, RetryEnvelope_1.withRetry)(async () => {
            const timerName = "lge_request_duration_ms";
            MetricsRegistry_1.metrics.startTimer(timerName, { endpoint: this.endpoint });
            if (this.latencyMs > 0) {
                await new Promise((resolve) => setTimeout(resolve, this.latencyMs));
            }
            const startedAt = Date.now();
            const simulatedResponse = this.simEngine.update(validatedRequest);
            const completedAt = Date.now();
            const durationMs = completedAt - startedAt;
            MetricsRegistry_1.metrics.observe("lge_call_latency_ms", durationMs, {
                mode: this.simEngineMode,
                status: simulatedResponse.status
            });
            const duration = MetricsRegistry_1.metrics.endTimer(timerName, { endpoint: this.endpoint });
            WitnessLogger_1.witness.log("LGE_REQUEST_COMPLETED", {
                duration,
                response: simulatedResponse,
                endpoint: this.endpoint
            });
            const validatedResponse = (0, ValidatorFactory_1.validateOrThrow)(LGE_RESPONSE_SCHEMA_NAME, simulatedResponse);
            GovernanceSignalBus_1.governanceBus.emitEvent({
                type: "MESSAGE_PROCESSED",
                severity: "INFO",
                timestamp: new Date().toISOString(),
                id: validatedResponse.documentId,
                details: {
                    engine: "LGE",
                    status: validatedResponse.status
                }
            });
            return validatedResponse;
        });
    }
    async resolve(request) {
        try {
            const updateResult = await this.update({
                documentId: `${request.tenantId}:${request.lexiconName}`,
                tenantId: request.tenantId,
                lexiconKey: request.lexiconName,
                payload: { input: request.input },
                occurredAt: new Date().toISOString()
            });
            if (updateResult.status === "FAILED") {
                return (0, contracts_1.failure)("LGE_RESOLVE_FAILED", updateResult.reason ?? "LGE update failed");
            }
            return (0, contracts_1.success)({
                tenantId: updateResult.tenantId,
                lexiconName: request.lexiconName,
                output: updateResult.status,
                version: "v1"
            });
        }
        catch (err) {
            return (0, contracts_1.failure)("LGE_RESOLVE_ERROR", err instanceof Error ? err.message : String(err));
        }
    }
}
exports.LGEClient = LGEClient;
//# sourceMappingURL=LGEClient.js.map