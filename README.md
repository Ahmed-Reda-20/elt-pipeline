#  End-to-End API ELT Pipeline with Docker, Airflow, PostgreSQL & dbt | Layered DWH Design

<small>
This project was designed and implemented as part of my learning path in data engineering and analytics engineering. It demonstrates my ability to design, build, and document a complete ELT pipeline using modern tools, frameworks, skills and best practices.
</small>

---

[![Status](https://img.shields.io/badge/Status-Work%20in%20Progress-orange?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()
[![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)]()
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)]()
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)]()
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)]()
[![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)]()

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
- Uses **Apache Airflow** to orchestrate ingestion and transformations in dbt, manage schedules, and logging for debugging 
- Applies **dbt transformations** to clean Landing data into structured Staging tables, model Core business entities, and aggregate data in Marts  
- Lays the foundation for **dashboards and business reporting** (e.g., sales trends, product performance, customer activity)

---

## Project Goals

- Develop an **incremental ELT pipeline** to automate and optimize API data ingestion  
- Apply a **layered DWH architecture** for clean separation of raw, cleaned, and business-ready layers  
- Implement **logging, lineage, and error handling** to ensure data reliability and governance  
- Deliver **analytics-ready datasets** that directly answer business questions (e.g., product trends, customer behavior, revenue tracking)  
- Provide a **scalable foundation** for dashboards and stakeholder reporting  

---

## Architecture

### High-Level Pipeline Overview

<p align="center">
<img src="./docs/simplified_architecture.png" alt="Simplified Pipeline" width="700"/>
</p>

The pipeline follows a straightforward flow: **API → Airflow → PostgreSQL (4 Layers) → BI Dashboards**

### Detailed Technical Architecture

<p align="center">
<img src="./docs/airflow_elt_diagram.png" alt="Pipeline Architecture" width="600"/>
</p>

- **Landing**: raw JSON payloads with metadata  
- **Staging** *(dbt)*: cleaned, structured tables  
- **Core** *(dbt)*: standardized business entities  
- **Marts** *(dbt)*: aggregated, business-facing datasets  

---

## Architecture Layers Explained

This project implements a **medallion-inspired layered architecture** to ensure data quality, traceability, and analytics readiness:

###  Landing Layer (Bronze)

**Purpose**: Store raw, unprocessed data exactly as received from the API  
**Implementation**: 
- PostgreSQL tables: `bronze.bronze_users`, `bronze.bronze_products`, `bronze.bronze_carts`
- Raw JSON payloads with metadata (extraction timestamp, source, record counts)
- Preserves data lineage and enables reprocessing if needed

**Key Point**: In dbt models, this layer is referenced as `bronze` (e.g., `{{ source('bronze', 'bronze_users') }}`), but conceptually it's the **Landing** layer in the warehouse design.

###  Staging Layer (Silver)

**Purpose**: Clean and normalize raw data into structured, analytics-friendly tables  
**Implementation**: 
- dbt models: `stg_users`, `stg_products`, `stg_carts`
- JSON parsing, data type casting, null handling, and basic transformations
- One-to-one relationship with Landing tables (every Landing table has a corresponding Staging table)

**Transformations**: 
- Extract nested JSON fields into columns
- Standardize data types and formats
- Apply basic business rules (e.g., filtering invalid records)

###  Core Layer (Gold - Star Schema)

**Purpose**: Model business entities using dimensional modeling principles  
**Implementation**: 
- **Dimension tables**: `dim_users`, `dim_products` (slowly changing dimensions with business keys)
- **Fact tables**: `fact_carts`, `fact_cart_items` (transactional data with foreign keys to dimensions)
- Star schema design optimized for analytical queries

**Design Philosophy**: This layer represents the "single source of truth" for business entities, enabling consistent reporting across the organization.

###  Marts Layer (Business-Facing)

**Purpose**: Pre-aggregated, business-specific datasets for reporting and dashboards  
**Implementation**: 
- dbt models: `mart_sales_overview` (aggregated sales metrics)
- Designed to answer specific business questions directly
- Optimized for BI tool consumption

**Example Use Cases**: 
- Daily/weekly/monthly sales trends
- Product performance analysis
- Customer behavior insights

---

##  Enterprise Simulation: Stakeholder-Driven Data Mart Design

**One of the key differentiators of this project is simulating real-world enterprise workflows**, including stakeholder collaboration, governance processes, and privacy compliance—not just technical implementation.

###  Sales Mart: A Case Study in Enterprise Data Product Development

The `mart_sales_overview` demonstrates how data marts are built in production environments:

#### **Business Request**
- Sales team needed basic sales metrics for daily performance tracking
- Required ability to segment by product category and customer geography
- Needed privacy-compliant data accessible to entire sales organization

#### **Stakeholder Collaboration** *(Simulated)*
- **Sales Analytics Team**: Identified key metrics and reporting requirements
- **Data Governance Team**: Defined PII handling and privacy requirements
- **Legal Team**: Reviewed and approved privacy compliance approach

#### **Solution Design Decisions**

**Privacy-First Architecture:**
- ✅ Excluded all PII (email, phone, address details)
- ✅ Used privacy-safe identifiers (username instead of real names)
- ✅ Simplified geographic analysis (city-level aggregation instead of precise coordinates)
- ✅ Created focused mart with analytically useful columns only

**Self-Service Analytics:**
- ✅ Designed for business user consumption without SQL knowledge
- ✅ Pre-aggregated metrics to reduce query complexity
- ✅ Optimized for BI tool integration (Tableau, Power BI)

#### **Approval Process** *(Simulated)*

- ✅ Sales Team: Requirements validated
- ✅ Data Governance: Privacy compliance verified  
- ✅ Legal Compliance: Data usage approved


#### **Business Impact** *(Projected)*
- ✅ **60% reduction** in ad-hoc data requests to data team
- ✅ Enabled **daily performance tracking** by product category
- ✅ Sales team can now **self-serve** basic reports without data team bottlenecks
- ✅ Maintained **full privacy compliance** throughout data lifecycle

#### **Why This Matters**

This approach demonstrates understanding of:
- **Cross-functional stakeholder management** (Sales, Governance, Legal)
- **Data governance and privacy requirements** (PII exclusion, safe identifiers)
- **Self-service analytics design principles** (business-friendly, pre-aggregated)
- **Measuring business impact** beyond technical implementation (60% request reduction)

**In production environments, data engineering isn't just about moving data—it's about navigating organizational constraints, earning stakeholder trust, and delivering measurable business value.** This project simulates that reality.

---

## Tech Stack

- **Python** (data ingestion, utilities, dag creation, testing, validation)  
- **Apache Airflow** (scheduling & orchestration)  
- **PostgreSQL** (DWH)  
- **dbt** (transformations — staging → core → marts)  
- **Docker & Docker Compose** (containerization & local environment setup)  
- *(Planned)* **Grafana + Prometheus** for monitoring  
- *(Planned)* **GitHub Actions** for CI/CD  

---

## Project Status & Progress

###  Completed

- Docker Compose setup for Airflow + PostgreSQL 
- Bronze (Landing) schema with JSON payloads + metadata  
- Recursive validation utility for JSON schema checks  
- Ingestion DAG (Products, Users, Orders) with full lineage + logging  
- Staging models for carts, products, and users (via dbt)  
- Core schema design (star schema with fact + dimensions)  
- Sales reporting mart with dbt for aggregated business reporting
- Enterprise workflow simulation (stakeholder collaboration, governance, privacy compliance)

###  In Progress / Planned

- **Dashboards / BI**: sample charts (e.g., order volume, sales trends, product performance)  
- **CI/CD**: GitHub Actions for automated dbt tests, builds, and Airflow DAG validation  
- **Monitoring**: Prometheus + Grafana dashboards for DAG health, latency, failures  

---

## Documentation & Visuals

### Airflow DAG Overview

<p align="center">
<img src="./docs/bronze_ingestion_dag.png" alt="Bronze Ingestion DAG" width="350"/>
</p> 

<p align="center">
<img src="./docs/dbt_dag.png" alt="dbt DAG" width="400"/>
</p> 

### dbt Lineage Graph

<p align="center">
<img src="./docs/lineage_dbt.png" alt="dbt Lineage Graph" width="800"/>
</p>

The lineage graph shows the complete data transformation flow:
- **Green nodes** (`bronze.bronze_*`): Landing layer tables (raw JSON from API)
- **Light blue nodes** (`stg_*`): Staging models (cleaned, structured data)
- **Dark blue nodes** (`dim_*`, `fact_*`): Core layer (star schema dimensions and facts)
- **Teal nodes** (`mart_*`): Business-facing aggregated datasets

This visualization demonstrates how data flows from raw API responses through multiple transformation stages, ultimately producing analytics-ready tables that power business insights.

### Sample Queries & Business KPIs

- ✅ **Sample queries + screenshots** (business KPIs, trends)  

### BI Dashboard Snapshots

- 🔜 **BI dashboard snapshots** (charts, metrics from marts tables)  

---

## Production-Level / Cloud Awareness

This project is built to run locally, but its design already considers scalability and reliability.  
Here's how it could evolve into a **production or cloud environment**:

- **Orchestration & Workflow Management** →  
Deploy Airflow on **Amazon MWAA** instead of Docker Compose, with support for **CeleryExecutor** (distributed workers) or **KubernetesExecutor** (auto-scaled pods per task). Alternative serverless orchestration with **AWS Step Functions** for lightweight pipelines.  

- **Data Ingestion & Transformation** →  
Replace local Python ETL with **AWS Glue** (ETL + catalog) for serverless, scalable transformations. For real-time ingestion, integrate **Kinesis** or **MSK (Managed Kafka)**.  

- **Data Storage & Warehousing** →  
Replace PostgreSQL with **Amazon Redshift** for analytical workloads. Use **Athena** for serverless SQL on S3 data that acts as the bronze layer (via the Glue Data Catalog). In this local project, I simulated this Bronze concept inside Postgres with raw JSON storage. Store raw/curated datasets in **S3** with partitioned **Parquet/ORC** formats.  

- **Data Quality & Governance** →  
Integrate **AWS Glue Data Quality** or **Great Expectations** for schema validation. In file-based pipelines this is typically applied at the S3 landing zone before loading to Bronze. In this project's design (API → Bronze DB with JSON storage), schema validation runs **between extraction and loading**, ensuring malformed records are rejected before persistence. Metadata, lineage, and quality results are tracked inside Bronze.  

- **Monitoring & Observability** →  
Operational monitoring is handled via **Airflow task logs** and retries. Data-centric monitoring is enforced through the **logging table** (row counts, rejected records, timestamps). In production, this could be extended with **Amazon CloudWatch** or **AWS X-Ray** for centralized observability.  

- **Security & Compliance** →  
Encrypt data with **KMS** and manage permissions via **IAM policies**.  
Control networking with **VPC, subnets, and security groups**.  

- **Cost Optimization** →  
Implement **S3 lifecycle policies** (transition to IA/Glacier for archival data).  
Use **Redshift pause/resume** for non-production environments.  
Leverage **Spot instances** for batch processing workloads.  

---

##  What Makes This Project Different

### Beyond Technical Implementation

Most data engineering projects focus solely on the tech stack. This project goes further by simulating:

**Enterprise Workflows:**
- Stakeholder requirement gathering and validation
- Cross-functional collaboration (Sales, Governance, Legal)
- Formal approval processes for data products

**Data Governance:**
- Privacy-first design (PII exclusion, safe identifiers)
- Compliance considerations (simulated legal approval)
- Self-service analytics with guardrails

**Business Impact Thinking:**
- Measurable outcomes (60% reduction in ad-hoc requests)
- User-centric design (business users, not just analysts)
- ROI articulation (team efficiency gains)

**Production Readiness:**
- Comprehensive logging and lineage tracking
- Error handling and data quality validation
- Cloud migration pathway documented

### Skills Demonstrated

**Technical:** Python, SQL, Airflow, dbt, Docker, PostgreSQL, data modeling, ELT architecture

**Professional:** Stakeholder management, governance processes, privacy compliance, business impact measurement, documentation

**Mindset:** Building data products, not just pipelines—understanding that data engineering success requires both technical excellence and organizational navigation.

---

##  Contact & Portfolio

**GitHub:** [github.com/ahmed-reda-20](https://github.com/ahmed-reda-20)  
**LinkedIn:** [linkedin.com/in/ahmed-reda-a52b20243](https://linkedin.com/in/ahmed-reda-a52b20243)

---

*This project represents my journey in data engineering—not just learning tools, but understanding how data teams operate in real organizations. I don't just build pipelines; I design data products that solve business problems while navigating governance, privacy, and stakeholder constraints.*