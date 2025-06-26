RESOURCE_GROUP="billing-rg"
LOCATION="eastus"
STORAGE_ACCOUNT="billingstorage$RANDOM"
COSMOS_ACCOUNT="billingcosmos$RANDOM"
COSMOS_DB="billing-db"
COSMOS_CONTAINER="billing"
ARCHIVE_CONTAINER="archived-billing"

az group create --name $RESOURCE_GROUP --location $LOCATION

az storage account create 
  --name $STORAGE_ACCOUNT 
  --resource-group $RESOURCE_GROUP 
  --location $LOCATION 
  --sku Standard_LRS

STORAGE_CONN=$(az storage account show-connection-string 
  --name $STORAGE_ACCOUNT 
  --resource-group $RESOURCE_GROUP 
  --query connectionString -o tsv)

az storage container create 
  --name $ARCHIVE_CONTAINER 
  --account-name $STORAGE_ACCOUNT
  
az cosmosdb create 
  --name $COSMOS_ACCOUNT 
  --resource-group $RESOURCE_GROUP 
  --locations regionName=$LOCATION 
  --default-consistency-level "Session"

az cosmosdb sql database create 
  --account-name $COSMOS_ACCOUNT 
  --resource-group $RESOURCE_GROUP 
  --name $COSMOS_DB

az cosmosdb sql container create 
  --account-name $COSMOS_ACCOUNT 
  --resource-group $RESOURCE_GROUP 
  --database-name $COSMOS_DB 
  --name $COSMOS_CONTAINER 
  --partition-key-path "/id"
  
COSMOS_CONN=$(az cosmosdb keys list 
  --name $COSMOS_ACCOUNT 
  --resource-group $RESOURCE_GROUP 
  --type connection-strings 
  --query "connectionStrings[0].connectionString" -o tsv)
