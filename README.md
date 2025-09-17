# 🛠️ End-to-End API ELT Pipeline with Docker, Airflow, PostgreSQL & dbt | Medallion Architecture

[![status](https://img.shields.io/badge/status-WIP-orange)]()  
[![python](https://img.shields.io/badge/Made%20with-Python-blue)]()  
[![docker](https://img.shields.io/badge/Docker-Compose-informational)]()  
[![airflow](https://img.shields.io/badge/Apache-Airflow-0099CC)]()  
[![dbt](https://img.shields.io/badge/dbt-planned-lightgrey)]()  

---

## 📌 Business Case & Problem Statement
Modern companies rely on external APIs and third-party systems (e.g., **e-commerce platforms, payment providers, or CRM tools**) to support analytics and decision-making. However, data from these APIs often comes in **raw JSON form**, which is:  

- **Messy and unstructured** → not directly usable for business reporting  
- **Manual and inconsistent** → requires repeated pulls without automation  
- **Lacking traceability** → difficult to track errors or confirm when data was last updated  
- **Not analytics-ready** → business teams cannot immediately use it for dashboards or KPIs  

This project simulates a **retail company scenario** where operations depend on the **Fakestore API** for information about products, users, and orders. Currently, data extraction is manual, which slows down decision-making and risks data inconsistencies.  

To solve this, the project introduces an automated **ELT pipeline** that:  
- Extracts and stores **raw API data** into a PostgreSQL database, applying a **Bronze → Silver → Gold** layered architecture  
- Uses **Apache Airflow** to orchestrate ingestion, manage schedules, and log batch metadata for auditability  
- Plans **dbt transformations** to clean Bronze data into structured Silver tables and aggregated Gold datasets  
- Lays the foundation for **dashboards and business reporting** (e.g., sales trends, product performance, customer activity)  

---

## 🎯 Project Goals  
- Develop an **incremental ELT pipeline** to automate and optimize API data ingestion  
- Apply the **Medallion (Bronze/Silver/Gold) architecture** for clean separation of raw, cleaned, and business-ready layers  
- Implement **logging, lineage, and error handling** to ensure data reliability and governance  
- Deliver **analytics-ready datasets** that directly answer business questions (e.g., product trends, customer behavior, revenue tracking)  
- Provide a **scalable foundation** for dashboards and stakeholder reporting  

---

## 🏗️ Architecture

<p align="center">
  <img src="./docs/airflow_elt_diagram.drawio.png" alt="Pipeline Architecture" width="600"/>
</p>

- **Bronze Layer**: Raw JSON with metadata, logs, and error tracking  
- **Silver Layer** *(planned with dbt)*: Cleaned, structured tables  
- **Gold Layer** *(planned with dbt)*: Aggregated, business-facing datasets  

---

## ⚙️ Tech Stack
- **Python** (data ingestion, utilities)  
- **Apache Airflow** (scheduling & orchestration)  
- **PostgreSQL** (data storage)  
- **dbt** (transformations — planned)  
- **Docker & Docker Compose** (containerization & local environment setup)  
- *(Future)* **Grafana + Prometheus** for monitoring  

---

## 🚧 Project Status & Progress
This project is a **work in progress**.  

### ✅ Completed
- Set up **Docker Compose** for Airflow, Postgres (Bronze DB), and supporting services  
- Created **Bronze schema initialization** with SQL scripts  
- Implemented a **recursive validation utility** to check API data against predefined schemas  
- Built and tested **utility functions** for DAG tasks  
- Developed **Bronze ingestion DAG** with 3 tasks:  
  - Ingest Products  
  - Ingest Users  
  - Ingest Orders  
- Successfully ran the DAG in Airflow, with all tasks succeeding  

### 🔮 Planned (High-Level Vision)
- **Silver layer** with dbt transformations  
- **Gold layer** with aggregated business metrics  
- **Dashboards & monitoring** for both pipeline health and analytics  
- **Testing & CI/CD** for long-term reliability  

---

## 🗺️ Next Steps Roadmap (Actionable To-Do)
- [ ] **Design Silver layer with dbt** (normalize product, user, and order tables)  
- [ ] **Implement Gold layer** with aggregated metrics (sales trends, order volume by category, etc.)  
- [ ] **Add monitoring** with Grafana + Prometheus (track DAG runs, task failures, latency)  
- [ ] **Expand ingestion** by adding more data sources like real-time currency exchange rate APIs or additional flat file datasets  
- [ ] **Implement CI/CD** for automated testing and deployment (GitHub Actions or similar)  
- [ ] **Documentation & Tutorials** (how to run locally, example queries, dashboard screenshots)  

---

## ☁️ Production-Level / Cloud Awareness
While this project runs **locally only**, it is designed with scalability, reliability in mind.  
Here’s how it could evolve in a **production or cloud environment**:  

- **Orchestration & Workflow Management** →  
  Deploy Airflow on **Amazon MWAA** instead of Docker Compose,  
  with support for **CeleryExecutor** (distributed workers) or **KubernetesExecutor** (auto-scaled pods per task).  
  Alternative serverless orchestration with **AWS Step Functions** for lightweight pipelines.  

- **Data Ingestion & Transformation** →  
  Replace local Python ETL with **AWS Glue** (ETL + catalog) for serverless, scalable transformations.    
  For real-time ingestion, integrate **Kinesis** or **MSK (Managed Kafka)**.  

- **Data Storage & Warehousing** →  
  Replace PostgreSQL with **Amazon Redshift** for analytical workloads.  
  Use **Athena** for serverless SQL on S3 data acts as the bronze layer (via the Glue Data Catalog).  
  Store raw/curated datasets in **S3** with partitioned **Parquet/ORC** formats.  

- **Data Quality & Governance** →  
  Integrate **AWS Glue Data Quality** or **Great Expectations** for schema validation.  
  In file-based pipelines this is typically applied at the S3 landing zone before loading to Bronze.  
  In this project’s design (API → Bronze DB with JSON storage), schema validation runs **between extraction and loading**,  
  ensuring malformed records are rejected before persistence.  
  Metadata, lineage, and quality results are tracked inside Bronze.  

- **Monitoring & Observability** →  
  Operational monitoring is handled via **Airflow task logs** and retries.  
  Data-centric monitoring is enforced through the **logging table** (row counts, rejected records, timestamps).  
  In production, this could be extended with **Amazon CloudWatch** or **AWS X-Ray** for centralized observability.  

- **Deployment & Infrastructure** →  
  Containerize services with **Docker** and orchestrate using **ECS (Fargate)** or **EKS (Kubernetes)**.  
  Automate deployments via **CI/CD pipelines (AWS CodePipeline + CodeBuild)**.  
  Manage infra with **Terraform** or **AWS CDK** (Infrastructure as Code).  

- **Security & Compliance** →  
  Encrypt data with **KMS** and manage permissions via **IAM policies**.  
  Control networking with **VPC, subnets, and security groups**.  
  Apply fine-grained governance using **Lake Formation** and the **Glue Catalog**.   

---

