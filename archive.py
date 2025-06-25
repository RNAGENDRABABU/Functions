from datetime import datetime, timedelta
import json
import os
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import logging

COSMOS_CONN = os.environ["COSMOS_CONN"]
STORAGE_CONN = os.environ["STORAGE_CONN"]
DATABASE_NAME = "billing-db"
CONTAINER_NAME = "billing"
BLOB_CONTAINER = "archived-billing"

cosmos_client = CosmosClient.from_connection_string(COSMOS_CONN)
database = cosmos_client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

blob_service = BlobServiceClient.from_connection_string(STORAGE_CONN)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

def archive_old_records():
    Archives billing records older than 90 days from Cosmos DB to Azure Blob Storage.
    try:
        threshold_date = (datetime.utcnow() - timedelta(days=90)).isoformat()
        query = f"SELECT * FROM c WHERE c.createdAt < '{threshold_date}'"
        old_records = container.query_items(query=query, enable_cross_partition_query=True)

    for item in old_records:
        record_id = item["id"]
        created_at = item.get("createdAt", datetime.utcnow().isoformat())
        partition_key = item["partitionKey"] 

        blob_path = f"billing/{created_at[:7]}/{record_id}.json"

        Upload to Azure Blob Storage
        blob_container.upload_blob(
        name=blob_path,
        data=json.dumps(item),
        overwrite=True
        )
        container.delete_item(item=record_id, partition_key=partition_key)
        logging.info(f"Archived record {record_id} to blob path: {blob_path}")
  except:
        logging.error(f"Archival failed: {e}")
