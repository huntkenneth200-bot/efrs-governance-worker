"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.success = success;
exports.failure = failure;
/**
 * Generic helper to build a success envelope.
 */
function success(data) {
    return { ok: true, data };
}
/**
 * Generic helper to build an error envelope.
 */
function failure(code, message, details) {
    return {
        ok: false,
        error: { code, message, details },
    };
}
//# sourceMappingURL=index.js.map