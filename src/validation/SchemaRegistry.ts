import Ajv, { ValidateFunction } from "ajv";
import addFormats from "ajv-formats";

const ajv = new Ajv({ allErrors: true, strict: true });
addFormats(ajv);

const validators = new Map<string, ValidateFunction>();

export function registerSchema(name: string, schema: object) {
  const validate = ajv.compile(schema);
  validators.set(name, validate);
}

export function getValidator(name: string): ValidateFunction {
  const v = validators.get(name);
  if (!v) throw new Error(`Validator not found: ${name}`);
  return v;
}
