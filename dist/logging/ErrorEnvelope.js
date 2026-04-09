"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.toErrorEnvelope = toErrorEnvelope;
function toErrorEnvelope(err) {
    if (err instanceof Error) {
        return {
            message: err.message,
            name: err.name,
            stack: err.stack,
            invariantViolation: err.name === "InvariantViolation"
        };
    }
    return {
        message: String(err),
        name: "NonErrorThrow",
        stack: undefined,
        invariantViolation: false
    };
}
//# sourceMappingURL=ErrorEnvelope.js.map