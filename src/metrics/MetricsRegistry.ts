export interface MetricLabels {
  [key: string]: string | number | boolean;
}

interface CounterMetric {
  name: string;
  labels?: MetricLabels;
  value: number;
}

interface TimerMetric {
  name: string;
  labels?: MetricLabels;
  startTime: number;
}

interface ObserveMetric {
  name: string;
  labels?: MetricLabels;
  values: number[];
}

export class MetricsRegistry {
  private counters: CounterMetric[] = [];
  private timers: TimerMetric[] = [];
  private observations: ObserveMetric[] = [];

  increment(name: string, labels?: MetricLabels) {
    const metric = this.counters.find(
      (m) => m.name === name && JSON.stringify(m.labels ?? {}) === JSON.stringify(labels ?? {})
    );
    if (metric) {
      metric.value += 1;
    } else {
      this.counters.push({ name, labels, value: 1 });
    }
  }

  observe(name: string, value: number, labels?: MetricLabels) {
    const metric = this.observations.find(
      (m) => m.name === name && JSON.stringify(m.labels ?? {}) === JSON.stringify(labels ?? {})
    );
    if (metric) {
      metric.values.push(value);
    } else {
      this.observations.push({ name, labels, values: [value] });
    }
  }

  startTimer(name: string, labels?: MetricLabels) {
    this.timers.push({ name, labels, startTime: Date.now() });
  }

  endTimer(name: string, labels?: MetricLabels): number {
    const index = this.timers.findIndex(
      (m) => m.name === name && JSON.stringify(m.labels ?? {}) === JSON.stringify(labels ?? {})
    );
    if (index === -1) return 0;

    const metric = this.timers[index];
    const duration = Date.now() - metric.startTime;
    this.timers.splice(index, 1);
    return duration;
  }
}

export const metrics = new MetricsRegistry();
