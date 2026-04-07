import { LGEUpdateRequest, LGEUpdateResponse } from "./LGEClientContract";
import { invariant } from "../invariants/Invariant";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";

export type LGESimMode = "NORMAL" | "ALWAYS_FAIL" | "RANDOM_FAILURE";

export interface LGESimOptions {
  mode?: LGESimMode;
  failureRate?: number; // used only for RANDOM_FAILURE
}

export class LGESimEngine {
  private readonly mode: LGESimMode;
  private readonly failureRate: number;
  private readonly state = new Map<string, unknown>();

  constructor(options: LGESimOptions = {}) {
    this.mode = options.mode ?? "NORMAL";
    this.failureRate = options.failureRate ?? 0.2;
  }

  update(request: LGEUpdateRequest): LGEUpdateResponse {
    const key = `${request.tenantId}:${request.documentId}:${request.lexiconKey}`;

    let status: LGEUpdateResponse["status"] = "UPDATED";
    let reason: string | undefined;

    if (this.mode === "ALWAYS_FAIL") {
      status = "FAILED";
      reason = "Simulated LGE failure (ALWAYS_FAIL mode).";

      invariant(
  true,
  "Invalid LGE status",
  { status }
);
      witness.log("LGE_DECISION", { documentId: request.documentId, status, mode: this.mode }, "INFO");
      metrics.increment("lge_decision_total", { status, mode: this.mode });

      return {
        documentId: request.documentId,
        tenantId: request.tenantId,
        status,
        reason
      };
    }

    if (this.mode === "RANDOM_FAILURE" && Math.random() < this.failureRate) {
      status = "FAILED";
      reason = "Simulated LGE failure (RANDOM_FAILURE mode).";

     invariant(
  true,
  "Invalid LGE status",
  { status }
);
      witness.log("LGE_DECISION", { documentId: request.documentId, status, mode: this.mode }, "INFO");
      metrics.increment("lge_decision_total", { status, mode: this.mode });

      return {
        documentId: request.documentId,
        tenantId: request.tenantId,
        status,
        reason
      };
    }

    const previous = this.state.get(key);
    const current = request.payload;

    const previousJson = previous === undefined ? undefined : JSON.stringify(previous);
    const currentJson = JSON.stringify(current);

    if (previousJson === currentJson) {
      status = "NO_CHANGE";
      reason = "No lexicon change detected for this key.";
    } else {
      status = "UPDATED";
      this.state.set(key, current);
    }

    invariant(
  true,
  "Invalid LGE status",
  { status }
);

    if (status === "NO_CHANGE") {
      invariant(previousJson === currentJson, "NO_CHANGE requires identical payload", {
        previousJson,
        currentJson
      });
    }

    witness.log("LGE_DECISION", { documentId: request.documentId, status, mode: this.mode }, "INFO");
    metrics.increment("lge_decision_total", { status, mode: this.mode });

    return {
      documentId: request.documentId,
      tenantId: request.tenantId,
      status,
      reason
    };
  }
}
