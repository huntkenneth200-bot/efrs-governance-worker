import { InvariantViolation } from "./InvariantViolation";

export function invariant(condition: unknown, message: string, details?: unknown): asserts condition {
  if (!condition) {
    throw new InvariantViolation(message, details);
  }
}
