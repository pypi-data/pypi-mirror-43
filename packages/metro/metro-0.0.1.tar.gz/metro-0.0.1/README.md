# Metro
The Metro framework for Airflow allows you to build common and well-known pipeline patterns. It comprises a number of
composable modules:

- Metro Core: consolidate all your metrics for a given granularity of data into a single source of truth, from which denormalized tables can be created.
- Metro Accumulator: implements the daily aggregation + day-over-day join pattern that lets you accumulate a metric over time.
- Metro Aggregator: implements the table aggregation pattern to produce cube-like tables for use in reports.
