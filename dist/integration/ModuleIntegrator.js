"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ModuleIntegrator = void 0;
const crypto_1 = require("crypto");
const ValidatorFactory_1 = require("../validation/ValidatorFactory");
const WitnessLogger_1 = require("../logging/WitnessLogger");
const MetricsRegistry_1 = require("../metrics/MetricsRegistry");
const DocumentEvent_schema_1 = require("../validation/schemas/DocumentEvent.schema");
const EventLineageStore_1 = require("../lineage/EventLineageStore");
const Invariant_1 = require("../invariants/Invariant");
const ErrorEnvelope_1 = require("../logging/ErrorEnvelope");
class ModuleIntegrator {
    constructor(options) {
        this.governanceBus = options.governanceBus;
        this.dgeClient = options.dgeClient;
        this.lgeClient = options.lgeClient;
        this.lineageStore = options.lineageStore;
    }
    async processMessage(message) {
        const { payload } = message;
        const correlationId = (0, crypto_1.randomUUID)();
        const startedAt = Date.now();
        const validated = (0, ValidatorFactory_1.validateOrThrow)("DocumentEvent", payload);
        (0, DocumentEvent_schema_1.assertValidDocumentEvent)(validated);
        (0, Invariant_1.invariant)(validated.documentId, "Integrator: documentId missing", validated);
        (0, Invariant_1.invariant)(validated.tenantId, "Integrator: tenantId missing", validated);
        (0, Invariant_1.invariant)(validated.eventType, "Integrator: eventType missing", validated);
        MetricsRegistry_1.metrics.increment("messages_received", { schema: "DocumentEvent" });
        this.governanceBus.emitEvent({
            type: "MESSAGE_RECEIVED",
            severity: "INFO",
            timestamp: new Date().toISOString(),
            id: validated.documentId,
            details: { correlationId }
        });
        WitnessLogger_1.witness.log("MESSAGE_RECEIVED", { documentId: validated.documentId, tenantId: validated.tenantId }, "INFO", correlationId);
        try {
            const dgeResponse = await this.dgeClient.evaluate({
                tenantId: validated.tenantId,
                documentType: validated.eventType,
                payload: validated.payload,
                version: "v1"
            });
            if (!dgeResponse.ok) {
                throw new Error(dgeResponse.error.message);
            }
            const dgeResult = dgeResponse.data;
            (0, Invariant_1.invariant)(dgeResult.tenantId, "DGE result missing tenantId", dgeResult);
            (0, Invariant_1.invariant)(dgeResult.decision, "DGE result missing decision", dgeResult);
            const lgeResponse = await this.lgeClient.resolve({
                tenantId: validated.tenantId,
                lexiconName: "default",
                input: JSON.stringify(dgeResult),
                version: "v1"
            });
            if (!lgeResponse.ok) {
                throw new Error(lgeResponse.error.message);
            }
            const lgeResult = lgeResponse.data;
            (0, Invariant_1.invariant)(lgeResult.tenantId, "LGE result missing tenantId", lgeResult);
            const completedAt = Date.now();
            EventLineageStore_1.eventLineageStore.add({
                correlationId,
                messageId: message.id,
                documentId: validated.documentId,
                tenantId: validated.tenantId,
                eventType: validated.eventType,
                dgeStatus: dgeResult.decision,
                lgeStatus: lgeResult.output,
                startedAt,
                completedAt,
                retries: 0,
                finalStatus: "SUCCESS"
            });
            MetricsRegistry_1.metrics.increment("messages_processed", { schema: "DocumentEvent" });
            this.governanceBus.emitEvent({
                type: "MESSAGE_PROCESSED",
                severity: "INFO",
                timestamp: new Date().toISOString(),
                id: validated.documentId,
                details: {
                    correlationId,
                    dgeDecision: dgeResult.decision,
                    lgeOutput: lgeResult.output
                }
            });
            WitnessLogger_1.witness.log("MESSAGE_PROCESSED", {
                documentId: validated.documentId,
                tenantId: validated.tenantId,
                dgeDecision: dgeResult.decision,
                lgeOutput: lgeResult.output,
                durationMs: completedAt - startedAt
            }, "INFO", correlationId);
        }
        catch (err) {
            const completedAt = Date.now();
            const errorEnvelope = (0, ErrorEnvelope_1.toErrorEnvelope)(err);
            EventLineageStore_1.eventLineageStore.add({
                correlationId,
                messageId: message.id,
                documentId: validated.documentId,
                tenantId: validated.tenantId,
                eventType: validated.eventType,
                dgeStatus: undefined,
                lgeStatus: undefined,
                startedAt,
                completedAt,
                retries: 0,
                finalStatus: "FAILED"
            });
            this.governanceBus.emitEvent({
                type: "MESSAGE_FAILED",
                severity: "ERROR",
                timestamp: new Date().toISOString(),
                id: validated.documentId,
                details: {
                    correlationId,
                    error: errorEnvelope.message,
                    errorName: errorEnvelope.name,
                    invariantViolation: errorEnvelope.invariantViolation
                }
            });
            WitnessLogger_1.witness.log("MESSAGE_FAILED", {
                documentId: validated.documentId,
                tenantId: validated.tenantId,
                error: errorEnvelope.message,
                errorName: errorEnvelope.name,
                invariantViolation: errorEnvelope.invariantViolation
            }, "ERROR", correlationId);
            throw err;
        }
    }
    async handleDgeEvaluate(request) {
        const correlationId = request.tenantId + ":" + request.documentType + ":" + Date.now();
        await this.lineageStore?.append({
            id: correlationId,
            correlationId,
            eventType: "REQUEST_RECEIVED",
            timestamp: new Date().toISOString(),
            schemaVersion: "v1",
            context: { kind: "DGE_EVALUATE" }
        });
        const result = await this.dgeClient.evaluate(request);
        await this.lineageStore?.append({
            id: correlationId + ":RESULT",
            correlationId,
            eventType: result.ok ? "REQUEST_VALIDATED" : "ERROR",
            timestamp: new Date().toISOString(),
            schemaVersion: "v1",
            context: { result: result }
        });
        return result;
    }
    async handleLgeResolve(request) {
        const correlationId = request.tenantId + ":" + request.lexiconName + ":" + Date.now();
        await this.lineageStore?.append({
            id: correlationId,
            correlationId,
            eventType: "REQUEST_RECEIVED",
            timestamp: new Date().toISOString(),
            schemaVersion: "v1",
            context: { kind: "LGE_RESOLVE" }
        });
        const result = await this.lgeClient.resolve(request);
        await this.lineageStore?.append({
            id: correlationId + ":RESULT",
            correlationId,
            eventType: result.ok ? "REQUEST_VALIDATED" : "ERROR",
            timestamp: new Date().toISOString(),
            schemaVersion: "v1",
            context: { result: result }
        });
        return result;
    }
}
exports.ModuleIntegrator = ModuleIntegrator;
//# sourceMappingURL=ModuleIntegrator.js.map