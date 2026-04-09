"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateOrThrow = validateOrThrow;
const SchemaRegistry_1 = require("./SchemaRegistry");
function validateOrThrow(schemaName, data) {
    const validator = (0, SchemaRegistry_1.getValidator)(schemaName);
    if (!validator(data)) {
        const errors = validator.errors ?? [];
        throw new Error(`Validation failed for ${schemaName}: ${JSON.stringify(errors)}`);
    }
    return data;
}
//# sourceMappingURL=ValidatorFactory.js.map