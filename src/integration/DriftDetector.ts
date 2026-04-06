import { witness } from "../logging/WitnessLogger";
import { governanceBus } from "../governance/GovernanceSignalBus";
import { getValidator } from "../validation/SchemaRegistry";
import { DGEProcessRequest, DGEProcessResponse } from "../engines/DGEClientContract";
import { LGEUpdateRequest, LGEUpdateResponse } from "../engines/LGEClientContract";
import { getQueueAdapter } from "../queue/QueueAdapterRegistry";

type DriftIssueSeverity = "WARN" | "ERROR";

interface DriftIssue {
  code: string;
  message: string;
  severity: DriftIssueSeverity;
}

const EXPECTED_SCHEMAS = [
  "DGEProcessRequest",
  "DGEProcessResponse",
  "LGEUpdateRequest",
  "LGEUpdateResponse",
  "DocumentEvent"
];

function checkSchemaPresence(): DriftIssue[] {
  const issues: DriftIssue[] = [];

  for (const name of EXPECTED_SCHEMAS) {
    try {
      getValidator(name);
    } catch {
      issues.push({
        code: "SCHEMA_MISSING",
        message: `Required schema not registered: ${name}`,
        severity: "ERROR"
      });
    }
  }

  return issues;
}

function checkEngineContracts(): DriftIssue[] {
  const issues: DriftIssue[] = [];

  // These checks are structural sanity checks, not runtime validation.
  // They ensure that the TypeScript contracts still align with expectations.

  const dgeRequestSample: DGEProcessRequest = {
    documentId: "sample",
    tenantId: "sample",
    eventType: "SAMPLE",
    payload: {},
    occurredAt: new Date().toISOString()
  };

  const dgeResponseSample: DGEProcessResponse = {
    documentId: "sample",
    tenantId: "sample",
    status: "ACCEPTED",
    version: 1
  };

  const lgeRequestSample: LGEUpdateRequest = {
    documentId: "sample",
    tenantId: "sample",
    lexiconKey: "sample",
    payload: {},
    occurredAt: new Date().toISOString()
  };

  const lgeResponseSample: LGEUpdateResponse = {
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

function checkQueueAdapter(): DriftIssue[] {
  const issues: DriftIssue[] = [];

  try {
    getQueueAdapter("default");
  } catch {
    issues.push({
      code: "QUEUE_ADAPTER_MISSING",
      message: "Default queue adapter is not registered.",
      severity: "ERROR"
    });
  }

  return issues;
}

export function runDriftChecks(): void {
  const issues: DriftIssue[] = [
    ...checkSchemaPresence(),
    ...checkEngineContracts(),
    ...checkQueueAdapter()
  ];

  if (issues.length === 0) {
    witness.log("DRIFT_CHECKS_PASSED", {});
    governanceBus.emitEvent({
      type: "DRIFT_CHECKS_PASSED",
      severity: "INFO",
      timestamp: Date.now(),
      id: "DRIFT_CHECKS"
    });
    return;
  }

  for (const issue of issues) {
    witness.log("DRIFT_ISSUE_DETECTED", issue);
  }

  const hasError = issues.some((i) => i.severity === "ERROR");

  if (hasError) {
    governanceBus.emitEvent({
      type: "DRIFT_ISSUE_DETECTED",
      severity: "ERROR",
      timestamp: Date.now(),
      id: "DRIFT_CHECKS",
      details: { message: "Drift detected during startup." }
    });
    throw new Error("Drift detected. Worker startup aborted.");
  } else {
    governanceBus.emitEvent({
      type: "DRIFT_ISSUE_DETECTED",
      severity: "WARN",
      timestamp: Date.now(),
      id: "DRIFT_CHECKS_WARN"
    });
  }
}
