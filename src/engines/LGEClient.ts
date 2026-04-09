import { LGEClientContract, LGEUpdateRequest, LGEUpdateResponse, LgeLexiconRequest, LgeLexiconResult } from "./LGEClientContract";
import { validateOrThrow } from "../validation/ValidatorFactory";
import { withRetry } from "../retry/RetryEnvelope";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";
import { governanceBus } from "../governance/GovernanceSignalBus";
import { LGESimEngine, LGESimMode, LGESimOptions } from "./LGESimEngine";
import type { ApiResponse } from "../contracts";
import { success, failure } from "../contracts";

export type { LgeLexiconRequest, LgeLexiconResult };

const LGE_REQUEST_SCHEMA_NAME = "LGEUpdateRequest";
const LGE_RESPONSE_SCHEMA_NAME = "LGEUpdateResponse";

export interface LGEClientOptions extends LGESimOptions {
  endpoint?: string;
  latencyMs?: number;
}

export class LGEClient implements LGEClientContract {
  private readonly endpoint: string;
  private readonly latencyMs: number;
  private readonly simEngine: LGESimEngine;
  private readonly simEngineMode: LGESimMode;

  constructor(options: LGEClientOptions = {}) {
    this.endpoint = options.endpoint ?? "http://lge.local/update";

    const rawMode =
      options.mode ??
      (process.env.LGE_SIM_MODE as LGESimMode | undefined) ??
      "NORMAL";

    const mode: LGESimMode =
      rawMode === "NORMAL" ||
      rawMode === "ALWAYS_FAIL" ||
      rawMode === "RANDOM_FAILURE"
        ? rawMode
        : "NORMAL";

    this.simEngineMode = mode;

    let failureRate =
      options.failureRate ??
      (process.env.LGE_SIM_FAILURE_RATE
        ? Number(process.env.LGE_SIM_FAILURE_RATE)
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

    this.simEngine = new LGESimEngine({ mode, failureRate });
  }

  async update(request: LGEUpdateRequest): Promise<LGEUpdateResponse> {
    metrics.increment("lge_requests_total", { endpoint: this.endpoint });
    witness.log("LGE_REQUEST_INITIATED", { request, endpoint: this.endpoint });

    const validatedRequest = validateOrThrow<LGEUpdateRequest>(LGE_REQUEST_SCHEMA_NAME, request);

    return withRetry(async () => {
      const timerName = "lge_request_duration_ms";
      metrics.startTimer(timerName, { endpoint: this.endpoint });

      if (this.latencyMs > 0) {
        await new Promise<void>((resolve) => setTimeout(resolve, this.latencyMs));
      }

      const startedAt = Date.now();
      const simulatedResponse = this.simEngine.update(validatedRequest);
      const completedAt = Date.now();
      const durationMs = completedAt - startedAt;

      metrics.observe("lge_call_latency_ms", durationMs, {
        mode: this.simEngineMode,
        status: simulatedResponse.status
      });

      const duration = metrics.endTimer(timerName, { endpoint: this.endpoint });
      witness.log("LGE_REQUEST_COMPLETED", {
        duration,
        response: simulatedResponse,
        endpoint: this.endpoint
      });

      const validatedResponse = validateOrThrow<LGEUpdateResponse>(
        LGE_RESPONSE_SCHEMA_NAME,
        simulatedResponse
      );

      governanceBus.emitEvent({
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

  async resolve(request: LgeLexiconRequest): Promise<ApiResponse<LgeLexiconResult>> {
    try {
      const updateResult = await this.update({
        documentId: `${request.tenantId}:${request.lexiconName}`,
        tenantId: request.tenantId,
        lexiconKey: request.lexiconName,
        payload: { input: request.input },
        occurredAt: new Date().toISOString()
      });

      if (updateResult.status === "FAILED") {
        return failure(
          "LGE_RESOLVE_FAILED",
          updateResult.reason ?? "LGE update failed"
        );
      }

      return success({
        tenantId: updateResult.tenantId,
        lexiconName: request.lexiconName,
        output: updateResult.status,
        version: "v1"
      });
    } catch (err) {
      return failure(
        "LGE_RESOLVE_ERROR",
        err instanceof Error ? err.message : String(err)
      );
    }
  }
}
