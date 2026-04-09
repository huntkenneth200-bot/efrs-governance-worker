"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DGESimEngine = void 0;
const Invariant_1 = require("../invariants/Invariant");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
class DGESimEngine {
    constructor(options = {}) {
        this.versionMap = new Map();
        this.mode = options.mode ?? "NORMAL";
        this.failureRate = options.failureRate ?? 0.2;
    }
    process(request) {
        const key = `${request.tenantId}:${request.documentId}`;
        const previousVersion = this.versionMap.get(key) ?? 0;
        const nextVersion = previousVersion + 1;
        (0, Invariant_1.invariant)(nextVersion > previousVersion, "DGE version must strictly increase", { previousVersion, nextVersion });
        let status = "ACCEPTED";
        let reason;
        if (this.mode === "ALWAYS_FAIL") {
            status = "REJECTED";
            reason = "Simulated DGE failure (ALWAYS_FAIL mode).";
        }
        else if (this.mode === "RANDOM_FAILURE" && Math.random() < this.failureRate) {
            status = "REJECTED";
            reason = "Simulated DGE failure (RANDOM_FAILURE mode).";
        }
        else if (request.eventType === "PENDING") {
            status = "PENDING";
            reason = "Simulated pending state for eventType=PENDING.";
        }
        (0, Invariant_1.invariant)(status === "ACCEPTED" || status === "REJECTED" || status === "PENDING", "Invalid DGE status", { status });
        this.versionMap.set(key, nextVersion);
        WitnessLogger_1.witness.log("DGE_DECISION", {
            key,
            previousVersion,
            nextVersion,
            status,
            mode: this.mode
        }, "INFO");
        MetricsRegistry_1.metrics.increment("dge_decision_total", {
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
exports.DGESimEngine = DGESimEngine;
//# sourceMappingURL=DGESimEngine.js.map