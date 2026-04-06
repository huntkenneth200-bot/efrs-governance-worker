import { DGEClientContract, DGEProcessRequest, DGEProcessResponse } from "./DGEClientContract";
import { validateOrThrow } from "../validation/ValidatorFactory";
import { withRetry } from "../retry/RetryEnvelope";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";
import { governanceBus } from "../governance/GovernanceSignalBus";
import { DGESimEngine, DGESimMode, DGESimOptions } from "./DGESimEngine";
import type { DGEClient as DGEClientInterface, DgeEvaluateRequest, DgeEvaluateResult } from "../dge/DGEClient";
import type { ApiResponse } from "../contracts";
import { success, failure } from "../contracts";

const DGE_REQUEST_SCHEMA_NAME = "DGEProcessRequest";
const DGE_RESPONSE_SCHEMA_NAME = "DGEProcessResponse";

export interface DGEClientOptions extends DGESimOptions {
  endpoint?: string;
  latencyMs?: number;
}

export class DGEClient implements DGEClientContract, DGEClientInterface {
  private readonly endpoint: string;
  private readonly latencyMs: number;
  private readonly simEngine: DGESimEngine;
  private readonly simEngineMode: DGESimMode;

  constructor(options: DGEClientOptions = {}) {
    this.endpoint = options.endpoint ?? "http://dge.local/process";

    const rawMode =
      options.mode ??
      (process.env.DGE_SIM_MODE as DGESimMode | undefined) ??
      "NORMAL";

    const mode: DGESimMode =
      rawMode === "NORMAL" ||
      rawMode === "ALWAYS_FAIL" ||
      rawMode === "RANDOM_FAILURE"
        ? rawMode
        : "NORMAL";

    this.simEngineMode = mode;

    let failureRate =
      options.failureRate ??
      (process.env.DGE_SIM_FAILURE_RATE
        ? Number(process.env.DGE_SIM_FAILURE_RATE)
        : undefined);

    if (
      failureRate === undefined ||
      Number.isNaN(failureRate) ||
      failureRate < 0 ||
      failureRate > 1
    ) {
      failureRate = 0.2;
    }

    const latency = options.latencyMs ?? 0;
    this.latencyMs = latency < 0 ? 0 : latency;

    this.simEngine = new DGESimEngine({ mode, failureRate });
  }

  async process(request: DGEProcessRequest): Promise<DGEProcessResponse> {
    metrics.increment("dge_requests_total", { endpoint: this.endpoint });
    witness.log("DGE_REQUEST_INITIATED", { request, endpoint: this.endpoint });

    const validatedRequest = validateOrThrow<DGEProcessRequest>(DGE_REQUEST_SCHEMA_NAME, request);

    return withRetry(async () => {
      const timerName = "dge_request_duration_ms";
      metrics.startTimer(timerName, { endpoint: this.endpoint });

      if (this.latencyMs > 0) {
        await new Promise<void>((resolve) => setTimeout(resolve, this.latencyMs));
      }

      const startedAt = Date.now();
      const simulatedResponse = this.simEngine.process(validatedRequest);
      const completedAt = Date.now();
      const durationMs = completedAt - startedAt;

      metrics.observe("dge_call_latency_ms", durationMs, {
        mode: this.simEngineMode,
        status: simulatedResponse.status
      });

      const duration = metrics.endTimer(timerName, { endpoint: this.endpoint });
      witness.log("DGE_REQUEST_COMPLETED", {
        duration,
        response: simulatedResponse,
        endpoint: this.endpoint
      });

      const validatedResponse = validateOrThrow<DGEProcessResponse>(
        DGE_RESPONSE_SCHEMA_NAME,
        simulatedResponse
      );

      governanceBus.emitEvent({
        type: "MESSAGE_PROCESSED",
        severity: "INFO",
        timestamp: Date.now(),
        id: validatedResponse.documentId,
        details: {
          engine: "DGE",
          status: validatedResponse.status
        }
      });

      return validatedResponse;
    });
  }

  async evaluate(request: DgeEvaluateRequest): Promise<ApiResponse<DgeEvaluateResult>> {
    try {
      const processResult = await this.process({
        documentId: `${request.tenantId}:${request.documentType}`,
        tenantId: request.tenantId,
        eventType: request.documentType,
        payload: request.payload,
        occurredAt: new Date().toISOString()
      });

      const decision: "ALLOW" | "DENY" | "REVIEW" =
        processResult.status === "ACCEPTED" ? "ALLOW" :
        processResult.status === "REJECTED" ? "DENY" :
        "REVIEW";

      return success({
        tenantId: processResult.tenantId,
        documentType: request.documentType,
        decision,
        reasons: processResult.reason ? [processResult.reason] : [],
        version: "v1"
      });
    } catch (err) {
      return failure(
        "DGE_EVALUATE_ERROR",
        err instanceof Error ? err.message : String(err)
      );
    }
  }
}
