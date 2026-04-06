import { DGEProcessRequest, DGEProcessResponse } from "./DGEClientContract";
import { invariant } from "../invariants/Invariant";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";

export type DGESimMode = "NORMAL" | "ALWAYS_FAIL" | "RANDOM_FAILURE";

export interface DGESimOptions {
  mode?: DGESimMode;
  failureRate?: number; // used only for RANDOM_FAILURE
}

export class DGESimEngine {
  private readonly mode: DGESimMode;
  private readonly failureRate: number;
  private readonly versionMap = new Map<string, number>();

  constructor(options: DGESimOptions = {}) {
    this.mode = options.mode ?? "NORMAL";
    this.failureRate = options.failureRate ?? 0.2;
  }

  process(request: DGEProcessRequest): DGEProcessResponse {
    const key = `${request.tenantId}:${request.documentId}`;
    const previousVersion = this.versionMap.get(key) ?? 0;
    const nextVersion = previousVersion + 1;

    invariant(nextVersion > previousVersion, "DGE version must strictly increase", { previousVersion, nextVersion });

    let status: DGEProcessResponse["status"] = "ACCEPTED";
    let reason: string | undefined;

    if (this.mode === "ALWAYS_FAIL") {
      status = "REJECTED";
      reason = "Simulated DGE failure (ALWAYS_FAIL mode).";
    } else if (this.mode === "RANDOM_FAILURE" && Math.random() < this.failureRate) {
      status = "REJECTED";
      reason = "Simulated DGE failure (RANDOM_FAILURE mode).";
    } else if (request.eventType === "PENDING") {
      status = "PENDING";
      reason = "Simulated pending state for eventType=PENDING.";
    }

    invariant(
      status === "ACCEPTED" || status === "REJECTED" || status === "PENDING",
      "Invalid DGE status",
      { status }
    );

    this.versionMap.set(key, nextVersion);

    witness.log(
      "DGE_DECISION",
      {
        key,
        previousVersion,
        nextVersion,
        status,
        mode: this.mode
      },
      "INFO"
    );

    metrics.increment("dge_decision_total", {
      status,
      mode: this.mode
    });

    return {
      documentId: request.documentId,
      tenantId: request.tenantId,
      status,
      version: nextVersion,
      reason
    };
  }
}
