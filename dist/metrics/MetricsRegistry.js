"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.metrics = exports.MetricsRegistry = void 0;
class MetricsRegistry {
    constructor() {
        this.counters = [];
        this.timers = [];
        this.observations = [];
    }
    increment(name, labels) {
        const metric = this.counters.find((m) => m.name === name && JSON.stringify(m.labels ?? {}) === JSON.stringify(labels ?? {}));
        if (metric) {
            metric.value += 1;
        }
        else {
            this.counters.push({ name, labels, value: 1 });
        }
    }
    observe(name, value, labels) {
        const metric = this.observations.find((m) => m.name === name && JSON.stringify(m.labels ?? {}) === JSON.stringify(labels ?? {}));
        if (metric) {
            metric.values.push(value);
        }
        else {
            this.observations.push({ name, labels, values: [value] });
        }
    }
    startTimer(name, labels) {
        this.timers.push({ name, labels, startTime: Date.now() });
    }
    endTimer(name, labels) {
        const index = this.timers.findIndex((m) => m.name === name && JSON.stringify(m.labels ?? {}) === JSON.stringify(labels ?? {}));
        if (index === -1)
            return 0;
        const metric = this.timers[index];
        const duration = Date.now() - metric.startTime;
        this.timers.splice(index, 1);
        return duration;
    }
}
exports.MetricsRegistry = MetricsRegistry;
exports.metrics = new MetricsRegistry();
//# sourceMappingURL=MetricsRegistry.js.map