"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerQueueAdapter = registerQueueAdapter;
exports.getQueueAdapter = getQueueAdapter;
const registry = new Map();
function registerQueueAdapter(name, adapter) {
    registry.set(name, adapter);
}
function getQueueAdapter(name) {
    const adapter = registry.get(name);
    if (!adapter)
        throw new Error(`Queue adapter not registered: ${name}`);
    return adapter;
}
//# sourceMappingURL=QueueAdapterRegistry.js.map