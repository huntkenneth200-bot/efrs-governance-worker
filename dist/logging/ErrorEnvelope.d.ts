export interface ErrorEnvelope {
    message: string;
    name: string;
    stack?: string;
    invariantViolation: boolean;
}
export declare function toErrorEnvelope(err: unknown): ErrorEnvelope;
//# sourceMappingURL=ErrorEnvelope.d.ts.map