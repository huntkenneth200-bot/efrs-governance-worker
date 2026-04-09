"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.InMemoryGovernanceBus = void 0;
class InMemoryGovernanceBus {
    constructor() {
        this.events = [];
    }
    emitEvent(event) {
        this.events.push(event);
    }
    getEvents() {
        return [...this.events];
    }
    clear() {
        this.events = [];
    }
}
exports.InMemoryGovernanceBus = InMemoryGovernanceBus;
//# sourceMappingURL=GovernanceBus.js.map