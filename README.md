# 🛠️ End-to-End API ELT Pipeline with Docker, Airflow, PostgreSQL & dbt | Layered DWH Design

[![status](https://img.shields.io/badge/status-WIP-orange)]()  
[![python](https://img.shields.io/badge/Made%20with-Python-blue)]()  
[![docker](https://img.shields.io/badge/Docker-Compose-informational)]()  
[![airflow](https://img.shields.io/badge/Apache-Airflow-0099CC)]()  
[![dbt](https://img.shields.io/badge/dbt-planned-lightgrey)]()  

---

## Business Case & Problem Statement
Modern companies rely on external APIs and third-party systems (e.g., **e-commerce platforms, payment providers, or CRM tools**) to support analytics and decision-making. However, data from these APIs often comes in **raw JSON form**, which is:  

- **Messy and unstructured** → not directly usable for business reporting  
- **Manual and inconsistent** → requires repeated pulls without automation  
- **Lacking traceability** → difficult to track errors or confirm when data was last updated  
- **Not analytics-ready** → business teams cannot immediately use it for dashboards or KPIs  

This project simulates a **retail company scenario** where operations depend on the **Fakestore API** for information about products, users, and orders. Currently, data extraction is manual, which slows down decision-making and risks data inconsistencies.  

To solve this, the project introduces an automated **ELT pipeline** that:  
- Extracts and stores **raw API data** into a PostgreSQL database, applying a **layered architecture (Landing → Staging → Core → Marts)**  
- Uses **Apache Airflow** to orchestrate ingestion, manage schedules, and log batch metadata for auditability  
- Plans **dbt transformations** to clean Landing data into structured Staging tables and aggregated Marts datasets  
- Lays the foundation for **dashboards and business reporting** (e.g., sales trends, product performance, customer activity)

Although traditional DWH staging often lands tabular data directly, this project introduces a raw **Landing schema** inside Postgres to preserve the original API payloads, support lineage, and allow data replay. This hybrid approach combines lakehouse-inspired raw storage with data warehouse-style transformations.

---

## Project Goals  
- Develop an **incremental ELT pipeline** to automate and optimize API data ingestion  
- Apply a **layered DWH architecture** for clean separation of raw, cleaned, and business-ready layers  
- Implement **logging, lineage, and error handling** to ensure data reliability and governance  
- Deliver **analytics-ready datasets** that directly answer business questions (e.g., product trends, customer behavior, revenue tracking)  
- Provide a **scalable foundation** for dashboards and stakeholder reporting  

---

## Architecture

<p align="center">
  <img src="./docs/airflow_elt_diagram.drawio.png" alt="Pipeline Architecture" width="600"/>
</p>

- **Landing**: raw JSON payloads with metadata  
- **Staging** *(planned with dbt)*: cleaned, structured tables  
- **Core** *(planned with dbt)*: standardized business entities  
- **Marts** *(planned with dbt)*: aggregated, business-facing datasets  

---

## Tech Stack
- **Python** (data ingestion, utilities)  
- **Apache Airflow** (scheduling & orchestration)  
- **PostgreSQL** (DWH)  
- **dbt** (transformations — planned)  
- **Docker & Docker Compose** (containerization & local environment setup)  
- *(Future)* **Grafana + Prometheus** for monitoring  

---

## Project Status & Progress
This project is a **work in progress**.  

### Completed
- Set up **Docker Compose** for Airflow, Postgres (DWH with Landing schema), and supporting services  
- Created **Landing schema initialization** with SQL scripts  
- Implemented a **recursive validation utility** to check API data against predefined schemas  
- Built and tested **utility functions** for DAG tasks  
- Developed **Landing ingestion DAG** with 3 tasks:  
  - Ingest Products  
  - Ingest Users  
  - Ingest Orders  
- Successfully ran the DAG in Airflow, with all tasks succeeding  

### Planned (High-Level Vision)
- **Staging layer** with dbt for standardized and structured transformations  
- **Core + Marts layers** with dbt for aggregated and business-ready models  
- **Dashboards & monitoring** for both pipeline health and analytics  
- **Testing & CI/CD** for long-term reliability  

---

## Next Steps Roadmap (Actionable To-Do)
- [ ] **Design Staging layer with dbt** (normalize product, user, and order tables)  
- [ ] **Implement Core + Marts layers** with aggregated metrics (sales trends, order volume by category, etc.)  
- [ ] **Add monitoring** with Grafana + Prometheus (track DAG runs, task failures, latency)  
- [ ] **Expand ingestion** by adding more data sources like real-time currency exchange rate APIs or simulate more batches with synthetic data  
- [ ] **Implement CI/CD** for automated testing and deployment (GitHub Actions or similar)  
- [ ] **Documentation & Tutorials** (how to run locally, example queries, dashboard screenshots)  

---

## Production-Level / Cloud Awareness
This project is built to run locally, but its design already considers scalability and reliability.  
Here’s how it could evolve into a **production or cloud environment**:

- **Orchestration & Workflow Management** → 
  Deploy Airflow on **Amazon MWAA** instead of Docker Compose, with support for **CeleryExecutor** (distributed workers) or **KubernetesExecutor** (auto-scaled pods per task). Alternative serverless orchestration with **AWS Step Functions** for lightweight pipelines.

- **Data Ingestion & Transformation** → 
  Replace local Python ETL with **AWS Glue** (ETL + catalog) for serverless, scalable transformations. For real-time ingestion, integrate **Kinesis** or **MSK (Managed Kafka)**.

- **Data Storage & Warehousing** → 
  Replace PostgreSQL with **Amazon Redshift** for analytical workloads. Use **Athena** for serverless SQL on S3 data that acts as the bronze layer (via the Glue Data Catalog). In this local project, I simulated this Bronze concept inside Postgres with raw JSON storage. Store raw/curated datasets in **S3** with partitioned **Parquet/ORC** formats.

- **Data Quality & Governance** → 
  Integrate **AWS Glue Data Quality** or **Great Expectations** for schema validation. In file-based pipelines this is typically applied at the S3 landing zone before loading to Bronze. In this project’s design (API → Bronze DB with JSON storage), schema validation runs **between extraction and loading**, ensuring malformed records are rejected before persistence. Metadata, lineage, and quality results are tracked inside Bronze.

- **Monitoring & Observability** → 
  Operational monitoring is handled via **Airflow task logs** and retries. Data-centric monitoring is enforced through the **logging table** (row counts, rejected records, timestamps). In production, this could be extended with **Amazon CloudWatch** or **AWS X-Ray** for centralized observability.

- **Security & Compliance** → 
  Encrypt data with **KMS** and manage permissions via **IAM policies**. 
  Control networking with **VPC, subnets,  and security groups**.

- **Cost Optimization** →
  Implement **S3 lifecycle policies** (transition to IA/Glacier for archival data).  
  Use **Redshift pause/resume** for non-production environments.  
  Leverage **Spot instances** for batch processing workloads.

---