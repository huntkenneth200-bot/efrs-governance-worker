"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.witness = exports.WitnessLogger = void 0;
const crypto_1 = require("crypto");
class WitnessLogger {
    log(event, data, level = "INFO", correlationId) {
        const envelope = {
            level,
            event,
            data,
            timestamp: Date.now(),
            correlationId: correlationId ?? (0, crypto_1.randomUUID)()
        };
        // For now, logs go to stdout as JSON.
        console.log(JSON.stringify(envelope));
    }
}
exports.WitnessLogger = WitnessLogger;
exports.witness = new WitnessLogger();
//# sourceMappingURL=WitnessLogger.js.map