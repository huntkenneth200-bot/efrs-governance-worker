import { MetricLabels, metrics as registryMetrics } from "./MetricsRegistry";

export type { MetricLabels };

export interface MetricsClient {
  increment(name: string, labels?: MetricLabels): void;
  observe(name: string, value: number, labels?: MetricLabels): void;
}

export const metrics: MetricsClient = registryMetrics;
