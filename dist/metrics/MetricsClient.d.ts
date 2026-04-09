import { MetricLabels } from "./MetricsRegistry";
export type { MetricLabels };
export interface MetricsClient {
    increment(name: string, labels?: MetricLabels): void;
    observe(name: string, value: number, labels?: MetricLabels): void;
}
export declare const metrics: MetricsClient;
//# sourceMappingURL=MetricsClient.d.ts.map