import { getValidator } from "./SchemaRegistry";

export function validateOrThrow<T>(schemaName: string, data: T): T {
  const validator = getValidator(schemaName);
  if (!validator(data)) {
    const errors = validator.errors ?? [];
    throw new Error(`Validation failed for ${schemaName}: ${JSON.stringify(errors)}`);
  }
  return data;
}
