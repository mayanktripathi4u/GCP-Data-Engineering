# Fundamentals of Observability

[Refer](https://github.com/iam-veeramalla/observability-zero-to-hero/)

## 3 pillars of Observability
* Metrics --> Historical data if the events. Ex. CPU usage (over or under utilization); Memory Usage; Disk; HTTP Requests
* Logs --> To understand the application better.
* Traces --> Extensive information to debug; troubleshoot and identify the loop-hole and fix it.

# Observability 
It is the ability to measure and understand the internal state of a system based on the data it produces, allowing you to diagnose issues, monitor performance, and optimize operations. It typically encompasses three key pillars: logs, metrics, and traces.

## Key Components
* **Logs**: Unstructured or semi-structured data that records events and actions taken by the system.
* **Metrics**: Numerical data that provides information about system performance, health, and usage over time.
* **Traces**: Data that captures the flow of requests through a system, helping to identify bottlenecks and latency issues.

## Tools for Observability
1. Logging Tools:
* Elasticsearch, Logstash, Kibana (ELK Stack): A popular stack for searching, analyzing, and visualizing log data.
* Splunk: A powerful platform for searching, monitoring, and analyzing machine-generated big data.
* Fluentd: An open-source data collector for unified logging.

2. Monitoring and Metrics Tools:
* Prometheus: An open-source monitoring system and time series database, especially popular for Kubernetes environments.
* Grafana: An analytics and monitoring platform that integrates with various data sources, including Prometheus.
* Datadog: A monitoring and analytics platform that offers visibility across cloud applications.

3. Tracing Tools:
* Jaeger: An open-source end-to-end distributed tracing tool for monitoring and troubleshooting microservices.
* OpenTelemetry: A framework for collecting telemetry data, supporting both metrics and traces.
* Zipkin: A distributed tracing system that helps gather timing data needed to troubleshoot latency problems.

4. Full-Stack Observability Platforms:
* New Relic: Offers full-stack observability with features for application performance monitoring, infrastructure monitoring, and more.
* AppDynamics: Provides application performance management and real-time monitoring of application performance.

5. Cloud-Native Tools:
* AWS CloudWatch: A monitoring service for AWS resources and applications.
* Azure Monitor: Provides a complete view of your applications and infrastructure in Microsoft Azure.

# Monitoring Vs Observability
* Monitoring focus on Metrics.
* Observability

# Prometheus
One of the top monitoring tool in the world of Kubernetes.

