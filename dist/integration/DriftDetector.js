"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.runDriftChecks = runDriftChecks;
const WitnessLogger_1 = require("../logging/WitnessLogger");
const GovernanceSignalBus_1 = require("../governance/GovernanceSignalBus");
const SchemaRegistry_1 = require("../validation/SchemaRegistry");
const QueueAdapterRegistry_1 = require("../queue/QueueAdapterRegistry");
const EXPECTED_SCHEMAS = [
    "DGEProcessRequest",
    "DGEProcessResponse",
    "LGEUpdateRequest",
    "LGEUpdateResponse",
    "DocumentEvent"
];
function checkSchemaPresence() {
    const issues = [];
    for (const name of EXPECTED_SCHEMAS) {
        try {
            (0, SchemaRegistry_1.getValidator)(name);
        }
        catch {
            issues.push({
                code: "SCHEMA_MISSING",
                message: `Required schema not registered: ${name}`,
                severity: "ERROR"
            });
        }
    }
    return issues;
}
function checkEngineContracts() {
    const issues = [];
    // These checks are structural sanity checks, not runtime validation.
    // They ensure that the TypeScript contracts still align with expectations.
    const dgeRequestSample = {
        documentId: "sample",
        tenantId: "sample",
        eventType: "SAMPLE",
        payload: {},
        occurredAt: new Date().toISOString()
    };
    const dgeResponseSample = {
        documentId: "sample",
        tenantId: "sample",
        status: "ACCEPTED",
        version: 1
    };
    const lgeRequestSample = {
        documentId: "sample",
        tenantId: "sample",
        lexiconKey: "sample",
        payload: {},
        occurredAt: new Date().toISOString()
    };
    const lgeResponseSample = {
        documentId: "sample",
        tenantId: "sample",
        status: "UPDATED"
    };
    if (!dgeRequestSample.documentId || !dgeRequestSample.tenantId) {
        issues.push({
            code: "ENGINE_CONTRACT_DGE_REQUEST_INVALID",
            message: "DGEProcessRequest contract appears malformed.",
            severity: "ERROR"
        });
    }
    if (!dgeResponseSample.documentId || !dgeResponseSample.tenantId) {
        issues.push({
            code: "ENGINE_CONTRACT_DGE_RESPONSE_INVALID",
            message: "DGEProcessResponse contract appears malformed.",
            severity: "ERROR"
        });
    }
    if (!lgeRequestSample.documentId || !lgeRequestSample.tenantId) {
        issues.push({
            code: "ENGINE_CONTRACT_LGE_REQUEST_INVALID",
            message: "LGEUpdateRequest contract appears malformed.",
            severity: "ERROR"
        });
    }
    if (!lgeResponseSample.documentId || !lgeResponseSample.tenantId) {
        issues.push({
            code: "ENGINE_CONTRACT_LGE_RESPONSE_INVALID",
            message: "LGEUpdateResponse contract appears malformed.",
            severity: "ERROR"
        });
    }
    return issues;
}
function checkQueueAdapter() {
    const issues = [];
    try {
        (0, QueueAdapterRegistry_1.getQueueAdapter)("default");
    }
    catch {
        issues.push({
            code: "QUEUE_ADAPTER_MISSING",
            message: "Default queue adapter is not registered.",
            severity: "ERROR"
        });
    }
    return issues;
}
function runDriftChecks() {
    const issues = [
        ...checkSchemaPresence(),
        ...checkEngineContracts(),
        ...checkQueueAdapter()
    ];
    if (issues.length === 0) {
        WitnessLogger_1.witness.log("DRIFT_CHECKS_PASSED", {});
        GovernanceSignalBus_1.governanceBus.emitEvent({
            type: "DRIFT_CHECKS_PASSED",
            severity: "INFO",
            timestamp: new Date().toISOString(),
            id: "DRIFT_CHECKS"
        });
        return;
    }
    for (const issue of issues) {
        WitnessLogger_1.witness.log("DRIFT_ISSUE_DETECTED", issue);
    }
    const hasError = issues.some((i) => i.severity === "ERROR");
    if (hasError) {
        GovernanceSignalBus_1.governanceBus.emitEvent({
            type: "DRIFT_ISSUE_DETECTED",
            severity: "ERROR",
            timestamp: new Date().toISOString(),
            id: "DRIFT_CHECKS",
            details: { message: "Drift detected during startup." }
        });
        throw new Error("Drift detected. Worker startup aborted.");
    }
    else {
        GovernanceSignalBus_1.governanceBus.emitEvent({
            type: "DRIFT_ISSUE_DETECTED",
            severity: "WARN",
            timestamp: new Date().toISOString(),
            id: "DRIFT_CHECKS_WARN"
        });
    }
}
//# sourceMappingURL=DriftDetector.js.map