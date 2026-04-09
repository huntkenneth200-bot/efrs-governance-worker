export type LogLevel = "DEBUG" | "INFO" | "WARN" | "ERROR";
export interface WitnessLogEnvelope {
    level: LogLevel;
    event: string;
    data?: unknown;
    timestamp: number;
    correlationId?: string;
}
export declare class WitnessLogger {
    log(event: string, data?: unknown, level?: LogLevel, correlationId?: string): void;
}
export declare const witness: WitnessLogger;
//# sourceMappingURL=WitnessLogger.d.ts.map