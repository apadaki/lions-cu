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

try:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = 'lion-data-container-v4'

    local_path = "./data"
    local_fname = "history.json"
    upload_file_path = os.path.join(local_path, local_fname)
    clear_file(upload_file_path)

    # create blob client
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_fname)

    # upload to Azure
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

except Exception as ex:
    print('Exception:')
    print(ex)