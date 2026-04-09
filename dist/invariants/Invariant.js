"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.invariant = invariant;
const InvariantViolation_1 = require("./InvariantViolation");
function invariant(condition, message, details) {
    if (!condition) {
        throw new InvariantViolation_1.InvariantViolation(message, details);
    }
}
//# sourceMappingURL=Invariant.js.map