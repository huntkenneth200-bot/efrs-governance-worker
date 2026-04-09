"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerSchema = registerSchema;
exports.getValidator = getValidator;
const ajv_1 = __importDefault(require("ajv"));
const ajv_formats_1 = __importDefault(require("ajv-formats"));
const ajv = new ajv_1.default({ allErrors: true, strict: true });
(0, ajv_formats_1.default)(ajv);
const validators = new Map();
function registerSchema(name, schema) {
    const validate = ajv.compile(schema);
    validators.set(name, validate);
}
function getValidator(name) {
    const v = validators.get(name);
    if (!v)
        throw new Error(`Validator not found: ${name}`);
    return v;
}
//# sourceMappingURL=SchemaRegistry.js.map