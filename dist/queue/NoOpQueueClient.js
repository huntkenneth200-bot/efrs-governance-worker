"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.NoOpQueueClient = void 0;
class NoOpQueueClient {
    async enqueue(_queueName, _payload) { }
    async registerConsumer(_queueName, _consumer) { }
    async ack(_messageId) { }
    async fail(_messageId, _error) { }
    async getQueueSize(_queueName) { return 0; }
    async peekQueue(_queueName, _limit) { return []; }
    async drainQueue(_queueName) { }
}
exports.NoOpQueueClient = NoOpQueueClient;
//# sourceMappingURL=NoOpQueueClient.js.map