"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.LGESimEngine = void 0;
const Invariant_1 = require("../invariants/Invariant");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
class LGESimEngine {
    constructor(options = {}) {
        this.state = new Map();
        this.mode = options.mode ?? "NORMAL";
        this.failureRate = options.failureRate ?? 0.2;
    }
    update(request) {
        const key = `${request.tenantId}:${request.documentId}:${request.lexiconKey}`;
        let status = "UPDATED";
        let reason;
        if (this.mode === "ALWAYS_FAIL") {
            status = "FAILED";
            reason = "Simulated LGE failure (ALWAYS_FAIL mode).";
            (0, Invariant_1.invariant)(true, "Invalid LGE status", { status });
            WitnessLogger_1.witness.log("LGE_DECISION", { documentId: request.documentId, status, mode: this.mode }, "INFO");
            MetricsRegistry_1.metrics.increment("lge_decision_total", { status, mode: this.mode });
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
            (0, Invariant_1.invariant)(true, "Invalid LGE status", { status });
            WitnessLogger_1.witness.log("LGE_DECISION", { documentId: request.documentId, status, mode: this.mode }, "INFO");
            MetricsRegistry_1.metrics.increment("lge_decision_total", { status, mode: this.mode });
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
        }
        else {
            status = "UPDATED";
            this.state.set(key, current);
        }
        (0, Invariant_1.invariant)(true, "Invalid LGE status", { status });
        if (status === "NO_CHANGE") {
            (0, Invariant_1.invariant)(previousJson === currentJson, "NO_CHANGE requires identical payload", {
                previousJson,
                currentJson
            });
        }
        WitnessLogger_1.witness.log("LGE_DECISION", { documentId: request.documentId, status, mode: this.mode }, "INFO");
        MetricsRegistry_1.metrics.increment("lge_decision_total", { status, mode: this.mode });
        return {
            documentId: request.documentId,
            tenantId: request.tenantId,
            status,
            reason
        };
    }
}
exports.LGESimEngine = LGESimEngine;
//# sourceMappingURL=LGESimEngine.js.map