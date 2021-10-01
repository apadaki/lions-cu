import time, requests, json
import os

# get environment variable from local .env file
from dotenv import load_dotenv
load_dotenv()

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from datetime import datetime

# empties a file and creates it if it doesn't exist
def clear_file(filename):
    open(filename, 'w').close()

# try:
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

# create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = 'lion-data-container-v4'

local_path = "./data"
local_fname = "history.json"
local_file_path = os.path.join(local_path, local_fname)

# create blob client
blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_fname)

# download from Azure
download_file_path = local_file_path
print("\nDownloading blob to \n\t" + download_file_path)
with open(download_file_path, "wb") as download_file:
    download_file.write(blob_client.download_blob().readall()) 

# except Exception as ex:
#     print('Exception:')
#     print(ex)