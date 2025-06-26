# Azure Billing Archival System
 Overview / Description

Describe what the project does.

Mention that it:

Stores recent billing records in Cosmos DB

Archives old records (>90 days) to Blob Storage

Uses Azure Functions to automate this process

Maintains API compatibility and no downtime

Architecture Diagram
architecture-diagram.png

Serverless and scalable

Cost optimization via archival

No data loss or downtime

API contract remains unchanged

Reads data from Cosmos or archive based on age

Uses Azure Functions (HTTP + Timer)

Technologies Used

List all core technologies:

Azure Functions (Python)

Azure Cosmos DB

Azure Blob Storage

Azure CLI or Bicep for deployment

Python (for logic and data scripts)


Folder Structure

├── infra/                  # Deploy script
├── scripts/                # Data simulation
├── functions/              # Azure Functions
│   ├── archiveFunction/
│   ├── readFunction/
│   └── local.settings.json
├── architecture-diagram.png
└── README.md


Deployment Steps

Clone the repo

Run deploy.sh to create Azure resources

Set connection strings in local.settings.json

Run Azure Functions locally using func start

Load test data using test_data_loader.py

Usage

Use readFunction to fetch billing data

Use archiveFunction (timer) to archive old records

Archived records are stored in Blob Storage
