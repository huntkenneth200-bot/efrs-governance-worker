import { randomUUID } from "crypto";
import { validateOrThrow } from "../validation/ValidatorFactory";
import { witness } from "../logging/WitnessLogger";
import { metrics } from "../metrics/MetricsRegistry";
import type { DGEClient } from "../engines/DGEClient";
import type { DgeEvaluateRequest, DgeEvaluateResult } from "../engines/DGEClientContract";
import type { LGEClient } from "../engines/LGEClient";
import type { LgeLexiconRequest, LgeLexiconResult } from "../engines/LGEClientContract";
import type { ApiResponse } from "../contracts";
import { DocumentEvent, assertValidDocumentEvent } from "../validation/schemas/DocumentEvent.schema";
import { QueueMessage } from "../queue/QueueMessage";
import { eventLineageStore } from "../lineage/EventLineageStore";
import { invariant } from "../invariants/Invariant";
import { toErrorEnvelope } from "../logging/ErrorEnvelope";
import type { LineageStore } from "../lineage/LineageTypes";
import { GovernanceBus } from "../governance/GovernanceBus";

export class ModuleIntegrator {
  private readonly governanceBus: GovernanceBus;
  private readonly dgeClient: DGEClient;
  private readonly lgeClient: LGEClient;
  private readonly lineageStore?: LineageStore;

  constructor(options: {
    governanceBus: GovernanceBus;
    dgeClient: DGEClient;
    lgeClient: LGEClient;
    lineageStore?: LineageStore;
  }) {
    this.governanceBus = options.governanceBus;
    this.dgeClient = options.dgeClient;
    this.lgeClient = options.lgeClient;
    this.lineageStore = options.lineageStore;
  }

  async processMessage(message: QueueMessage<DocumentEvent>): Promise<void> {
    const { payload } = message;
    const correlationId = randomUUID();
    const startedAt = Date.now();

    const validated = validateOrThrow<DocumentEvent>("DocumentEvent", payload);

    assertValidDocumentEvent(validated);
    invariant(validated.documentId, "Integrator: documentId missing", validated);
    invariant(validated.tenantId, "Integrator: tenantId missing", validated);
    invariant(validated.eventType, "Integrator: eventType missing", validated);

    metrics.increment("messages_received", { schema: "DocumentEvent" });
    this.governanceBus.emitEvent({
      type: "MESSAGE_RECEIVED",
      severity: "INFO",
      timestamp: new Date().toISOString(),
      id: validated.documentId,
      details: { correlationId }
    });

    witness.log(
      "MESSAGE_RECEIVED",
      { documentId: validated.documentId, tenantId: validated.tenantId },
      "INFO",
      correlationId
    );

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

      const dgeResult = dgeResponse.data as DgeEvaluateResult;
      invariant(dgeResult.tenantId, "DGE result missing tenantId", dgeResult);
      invariant(dgeResult.decision, "DGE result missing decision", dgeResult);

      const lgeResponse = await this.lgeClient.resolve({
        tenantId: validated.tenantId,
        lexiconName: "default",
        input: JSON.stringify(dgeResult),
        version: "v1"
      });

      if (!lgeResponse.ok) {
        throw new Error(lgeResponse.error.message);
      }

      const lgeResult = lgeResponse.data as LgeLexiconResult;
      invariant(lgeResult.tenantId, "LGE result missing tenantId", lgeResult);

      const completedAt = Date.now();

      eventLineageStore.add({
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

      metrics.increment("messages_processed", { schema: "DocumentEvent" });

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

      witness.log(
        "MESSAGE_PROCESSED",
        {
          documentId: validated.documentId,
          tenantId: validated.tenantId,
          dgeDecision: dgeResult.decision,
          lgeOutput: lgeResult.output,
          durationMs: completedAt - startedAt
        },
        "INFO",
        correlationId
      );
    } catch (err) {
      const completedAt = Date.now();
      const errorEnvelope = toErrorEnvelope(err);

      eventLineageStore.add({
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

      witness.log(
        "MESSAGE_FAILED",
        {
          documentId: validated.documentId,
          tenantId: validated.tenantId,
          error: errorEnvelope.message,
          errorName: errorEnvelope.name,
          invariantViolation: errorEnvelope.invariantViolation
        },
        "ERROR",
        correlationId
      );

      throw err;
    }
  }

  async handleDgeEvaluate(
    request: DgeEvaluateRequest
  ): Promise<ApiResponse<DgeEvaluateResult>> {
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
      context: { result: result as unknown as Record<string, unknown> }
    });

    return result;
  }

  async handleLgeResolve(
    request: LgeLexiconRequest
  ): Promise<ApiResponse<LgeLexiconResult>> {
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
      context: { result: result as unknown as Record<string, unknown> }
    });

    return result;
  }
}