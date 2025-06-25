
import logging
import json
from azure.cosmos import CosmosClient
from datetime import datetime
import os

def main(req):
    try:
        data = req.get_json()
        data['createdat'] = datetime.utcnow().isoformat()

        cosmos = CosmosClient(os.environ['COSMOS_URI'], os.environ['COSMOS_KEY'])
        container = cosmos.get_database_client('billing-db').get_container_client('records')
        container.create_item(body=data)

        return func.HttpResponse("Record created", status_code=200)
  except:
        logging.error(f"Write error: {e}")
        return func.HttpResponse("Error", status_code=500)
