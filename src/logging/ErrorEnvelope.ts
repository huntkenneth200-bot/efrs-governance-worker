export interface ErrorEnvelope {
  message: string;
  name: string;
  stack?: string;
  invariantViolation: boolean;
}

export function toErrorEnvelope(err: unknown): ErrorEnvelope {
  if (err instanceof Error) {
    return {
      message: err.message,
      name: err.name,
      stack: err.stack,
      invariantViolation: err.name === "InvariantViolation"
    };
  }

  return {
    message: String(err),
    name: "NonErrorThrow",
    stack: undefined,
    invariantViolation: false
  };
}
