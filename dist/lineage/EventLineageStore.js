"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.eventLineageStore = exports.EventLineageStore = void 0;
const Invariant_1 = require("../invariants/Invariant");
class EventLineageStore {
    constructor(maxSize = 1000) {
        this.records = [];
        this.maxSize = maxSize;
    }
    add(record) {
        (0, Invariant_1.invariant)(record.startedAt <= record.completedAt, "Lineage timestamps out of order", record);
        (0, Invariant_1.invariant)(record.finalStatus === "SUCCESS" || record.finalStatus === "FAILED", "Invalid finalStatus", record);
        (0, Invariant_1.invariant)(record.retries >= 0, "Retries must be non-negative", record);
        this.records.push(record);
        if (this.records.length > this.maxSize) {
            this.records.shift();
        }
    }
    getByCorrelationId(correlationId) {
        return this.records.find((r) => r.correlationId === correlationId);
    }
    getByDocumentId(documentId) {
        return this.records.filter((r) => r.documentId === documentId);
    }
    getRecent(limit = 50) {
        if (limit <= 0)
            return [];
        return this.records.slice(-limit).reverse();
    }
}
exports.EventLineageStore = EventLineageStore;
exports.eventLineageStore = new EventLineageStore();
//# sourceMappingURL=EventLineageStore.js.map