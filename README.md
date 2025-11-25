SupplyChain-Delivery

Real-Time Shipment Tracking, Data Ingestion & Delivery Monitoring Platform

This project is a modern supply-chain data pipeline that automates shipment generation, processes real-time logistics data, stores it in PostgreSQL, and exposes results through a dashboard/API layer. It demonstrates practical skills in 
Python, PostgreSQL, Docker, REST API design, and end-to-end data engineering workflows.

Features

1. Automated Shipment Generation**

Python script generates realistic shipment data
Drivers, locations, package sizes, status codes
Timestamps for ingestion and delivery lifecycle

2. ETL Pipeline (Extract → Transform → Load)**

Raw shipment JSON → cleaned, validated, enriched
Inserts into PostgreSQL tables
Ensures idempotency & duplicate safety
Configurable batch sizes

3. PostgreSQL Database Layer**

Normalized schema for shipments, drivers, routes
Indexes for high-performance queries
SQL scripts for creating tables and inserting data

4. Dockerized Architecture**

Fully containerized using `docker-compose`
Includes PostgreSQL + Adminer/pgAdmin
Reproducible environment — runs anywhere

5. Future Features (Planned)**

Streamlit dashboard for real-time monitoring
API endpoints for shipment lookups
Driver performance analytics
Alerts for delayed shipments


Project Structure


SupplyChain-Delivery/
│
├── ingestion/
│   ├── generate_shipments.py      # Creates synthetic shipment data
│   ├── load_to_postgres.py        # Loads data into PostgreSQL
│
├── db/
│   ├── add_drivers.sql            # Initial seed data
│   ├── create_tables.sql          # Database schema
│
├── docker/
│   ├── Dockerfile                 # App image
│   ├── docker-compose.yml         # Full stack (app + Postgres)
│
├── app/
│   ├── api.py                     # FastAPI/Flask endpoint
│   ├── dashboard.py               # Streamlit interface
│
├── README.md
└── requirements.txt


Technologies Used

| Category            | Tools                  |
| ------------------- | ---------------------- |
| Language            | Python 3               |
| Database            | PostgreSQL 16          |
| Containers          | Docker, Docker Compose |
| Dashboard           | Streamlit              |
| API Layer           | FastAPI or Flask       |
| Environment         | VS Code, GitHub        |

Installation & Setup

1. Clone the repository

bash
git clone https://github.com/Chenti-prog/SupplyChain-Delivery.git
cd SupplyChain-Delivery

 2. Build and start with Docker

Ensure Docker Desktop is running.

bash
docker compose up --build


This starts:

PostgreSQL
Your Python ETL service
Adminer/pgAdmin (if included)

3. Run the ETL pipeline manually (local mode)

Generate shipments:

bash
python ingestion/generate_shipments.py


#### Load into PostgreSQL:

bash
python ingestion/load_to_postgres.py


4. Access PostgreSQL

If using pgAdmin / Adminer:

Host: `localhost`
Port: `5432`
User: `postgres`
Password: *set in docker-compose*

Example Queries

Total shipments:

sql
SELECT COUNT(*) FROM shipments;


Shipments by status:

sql
SELECT status, COUNT(*) 
FROM shipments 
GROUP BY status;


Delayed shipments:

sql
SELECT * FROM shipments WHERE delivery_time > expected_delivery_time;


 What This Project Demonstrates

This project is built to show hiring managers your ability to:

Build real-world ETL pipelines

Design normalized SQL schemas

Implement batch ingestion with Python

Work with Dockerized databases

Organize a clean production-ready folder structure

Prepare for real-time dashboards & API integrations

Document and publish software professionally on GitHub

Future Improvements

Real-time Kafka streaming
ML model for ETA prediction
Driver performance analytics
Full Streamlit dashboard
Containerized REST API
CI/CD workflow with GitHub Actions
