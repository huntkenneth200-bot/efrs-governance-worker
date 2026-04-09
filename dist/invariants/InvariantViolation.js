"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.InvariantViolation = void 0;
class InvariantViolation extends Error {
    constructor(message, details) {
        super(message);
        this.details = details;
        this.name = "InvariantViolation";
    }
}
exports.InvariantViolation = InvariantViolation;
//# sourceMappingURL=InvariantViolation.js.map