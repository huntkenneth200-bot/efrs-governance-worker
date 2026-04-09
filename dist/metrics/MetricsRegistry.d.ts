export interface MetricLabels {
    [key: string]: string | number | boolean;
}
export declare class MetricsRegistry {
    private counters;
    private timers;
    private observations;
    increment(name: string, labels?: MetricLabels): void;
    observe(name: string, value: number, labels?: MetricLabels): void;
    startTimer(name: string, labels?: MetricLabels): void;
    endTimer(name: string, labels?: MetricLabels): number;
}
export declare const metrics: MetricsRegistry;
//# sourceMappingURL=MetricsRegistry.d.ts.map