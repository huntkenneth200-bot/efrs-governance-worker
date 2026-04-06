import { witness } from "../logging/WitnessLogger";

export async function withRetry<T>(
  operation: () => Promise<T>,
  attempts = 3,
  delayMs = 250
): Promise<T> {
  let lastError: unknown;

  for (let i = 0; i < attempts; i++) {
    try {
      return await operation();
    } catch (err) {
      lastError = err;
      witness.log("RETRY_ATTEMPT_FAILED", { attempt: i + 1, error: String(err) });
      await new Promise((res) => setTimeout(res, delayMs * (i + 1)));
    }
  }

  throw lastError;
}
