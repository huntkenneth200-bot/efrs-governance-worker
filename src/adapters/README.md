# Adapters

This directory hosts real infrastructure adapters that implement the
governance-grade contracts defined in:

- src/queue/QueueClient.ts
- src/governance/GovernanceBus.ts

Each adapter must:

- implement the relevant interface(s)
- preserve invariant-first behavior
- emit metrics and governance events consistent with the in-memory versions
- avoid leaking provider-specific details into core modules

Examples (to be implemented in future packets):

- src/adapters/queue/SqsQueueClient.ts
- src/adapters/governance/EventBridgeGovernanceBus.ts
