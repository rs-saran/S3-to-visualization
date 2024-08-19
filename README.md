# S3-to-visualization

## Overview

The **S3-to-Postgres Data Pipeline** is a streamlined solution designed to transfer Parquet files from S3, load them into a PostgreSQL database, and visualize the data using Metabase. This pipeline ensures efficient data processing and provides actionable insights through visual analytics.

## Workflow
1. **Extract Data**: Download Parquet files from an S3 bucket using an Airflow DAG.
2. **Load Data**: Upload the downloaded Parquet files to a PostgreSQL data warehouse using another Airflow DAG.
3. **Visualize Data**: Use Metabase to visualize the data stored in the PostgreSQL warehouse.

## Setup

1. **Docker Compose Setup**

The project uses [Docker Compose](./docker-compose.yaml) to set up and manage necessary services:

- **MinIO**: S3-compatible object storage.
- **PostgreSQL**: Data storage.
- **Redis**: Message broker for Airflow.
- **Airflow**: Manages data workflows.
- **Metabase**: Visualization platform.

3. **Install Required Libraries**
   ```bash
   pip install boto3 sqlalchemy pandas pyarrow
   ```
   Mount the env dir to airflow

4. **Airflow DAG Setup**
   - Create a script to download Parquet files from S3. ([Extract](./scripts/extract.py))
   - Develop a script to transform and load Parquet files into PostgreSQL. ([Load](./scripts/load.py))
   - Write DAG Code to execute the extract and load scripts. ([DAG](./airflow/dags/dag_s3_to_warehouse.py))

   Mount the scripts dir to airflow

6. **Configure Metabase**
   - Connect Metabase to the PostgreSQL database.
   - Create dashboards and visualizations as needed. 
