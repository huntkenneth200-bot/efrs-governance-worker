export type IsoTimestamp = string; // ISO 8601

export interface ErrorEnvelope {
  ok: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

export interface SuccessEnvelope<T> {
  ok: true;
  data: T;
}

export type ApiResponse<T> = SuccessEnvelope<T> | ErrorEnvelope;

export interface Pagination {
  limit: number;
  offset: number;
}

export interface VersionedDto {
  version: string;
}

/**
 * Generic helper to build a success envelope.
 */
export function success<T>(data: T): SuccessEnvelope<T> {
  return { ok: true, data };
}

/**
 * Generic helper to build an error envelope.
 */
export function failure(
  code: string,
  message: string,
  details?: Record<string, unknown>
): ErrorEnvelope {
  return {
    ok: false,
    error: { code, message, details },
  };
}
