export class InvariantViolation extends Error {
  constructor(message: string, readonly details?: unknown) {
    super(message);
    this.name = "InvariantViolation";
  }
}
