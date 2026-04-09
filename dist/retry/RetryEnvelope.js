"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.withRetry = withRetry;
const WitnessLogger_1 = require("../logging/WitnessLogger");
async function withRetry(operation, attempts = 3, delayMs = 250) {
    let lastError;
    for (let i = 0; i < attempts; i++) {
        try {
            return await operation();
        }
        catch (err) {
            lastError = err;
            WitnessLogger_1.witness.log("RETRY_ATTEMPT_FAILED", { attempt: i + 1, error: String(err) });
            await new Promise((res) => setTimeout(res, delayMs * (i + 1)));
        }
    }
    throw lastError;
}
//# sourceMappingURL=RetryEnvelope.js.map