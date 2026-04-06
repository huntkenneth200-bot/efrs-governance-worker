import { randomUUID } from "crypto";

export type LogLevel = "DEBUG" | "INFO" | "WARN" | "ERROR";

export interface WitnessLogEnvelope {
  level: LogLevel;
  event: string;
  data?: unknown;
  timestamp: number;
  correlationId?: string;
}

export class WitnessLogger {
  log(event: string, data?: unknown, level: LogLevel = "INFO", correlationId?: string) {
    const envelope: WitnessLogEnvelope = {
      level,
      event,
      data,
      timestamp: Date.now(),
      correlationId: correlationId ?? randomUUID()
    };

    // For now, logs go to stdout as JSON.
    console.log(JSON.stringify(envelope));
  }
}

export const witness = new WitnessLogger();
