import uuid
import random
from datetime import datetime, timedelta
from azure.cosmos import CosmosClient
import os

COSMOS_CONN = os.environ["COSMOS_CONN"]
DATABASE_NAME = "billing-db"
CONTAINER_NAME = "billing"

client = CosmosClient.from_connection_string(COSMOS_CONN)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def generate_record(days_ago):
    created_date = (datetime.utcnow() - timedelta(days=days_ago)).isoformat()
    record_id = str(uuid.uuid4())

    record = {
        "id": record_id,
        "partitionKey": record_id,
        "amount": round(random.uniform(100, 1000), 2),
        "status": random.choice(["paid", "unpaid", "pending"]),
        "date": created_date,
        "customer_id": f"cust-{random.randint(1000, 9999)}"
    }

    return record
def insert_test_records(count=10):
    for i in range(count):
        days_old = random.randint(0, 180)  # records from 0 to 6 months old
        record = generate_record(days_old)
        container.upsert_item(record)
        print(f"Inserted record ID: {record['id']} ({days_old} days old)")
if __name__ == "__main__":
    insert_test_records(20)
