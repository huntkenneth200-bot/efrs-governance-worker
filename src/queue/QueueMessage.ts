import { QueueMessage } from "./QueueClient";
import { invariant } from "../invariants/Invariant";

export { QueueMessage };

export function assertValidQueueMessage(msg: QueueMessage<unknown>): void {
  invariant(typeof msg.id === "string" && msg.id.length > 0, "QueueMessage.id must be a non-empty string", msg);
  invariant(typeof msg.attempts === "number" && msg.attempts >= 0, "QueueMessage.attempts must be a non-negative number", msg);
  invariant(msg.payload !== undefined, "QueueMessage.payload must not be undefined", msg);
}
