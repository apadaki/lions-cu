import time, requests, json
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from datetime import datetime
from graph_creator import generate_graphs

# empties a file and creates it if it doesn't exist
def clear_file(filename):
    open(filename, 'w').close()

try:
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # create a unique name for the container
    container_name = 'lion-data-container-v4'
    # create the container
    # container_client = blob_service_client.create_container(container_name)

    # creates an empty file at desired pathname
    data_fname = 'history.json'
    graph_fname = 'graph.html'
    upload_file_path = data_fname
    clear_file(upload_file_path)

    print('AAAAAA')
    # create blob client
    blob_client_data = blob_service_client.get_blob_client(container=container_name, blob=data_fname)
    blob_client_johnjay = blob_service_client.get_blob_client(container=container_name, blob='{}_{}'.format('johnjay', graph_fname))
    blob_client_jj = blob_service_client.get_blob_client(container=container_name, blob='{}_{}'.format('jj', graph_fname))
    blob_client_ferris = blob_service_client.get_blob_client(container=container_name, blob='{}_{}'.format('ferris', graph_fname))


    print(blob_client_data)

    # print("\nUploading to Azure Storage as blob:\n\t" + local_fname)
    times = {}

    while True:
        # download from Azure
        download_file_path = upload_file_path
        # print("\nDownloading blob to \n\t" + download_file_path)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client_data.download_blob().readall())   

        if (os.stat(upload_file_path).st_size == 0):
            times = {}
        else:
            # read from local json
            with open(upload_file_path, 'r') as infile:
                times = json.load(infile)
        
        # add next entry using Columbia API call
        dining_url = 'https://dining.columbia.edu/cu_dining/rest/crowdedness'
 
        timestr = str(datetime.now())
        client_json = requests.get(dining_url).json()

        times[timestr] = client_json['data']
        # print('wrote entry at time {} to {}'.format(timestr, upload_file_path))
        
        # write to local json
        with open(upload_file_path, "w") as outfile:
            json.dump(times, outfile)
        
        generate_graphs(data_fname, graph_fname)
        with open('{}_{}'.format('johnjay', graph_fname), 'rb') as data:
            blob_client_johnjay.upload_blob(data, overwrite=True)
        with open('{}_{}'.format('jj', graph_fname), 'rb') as data:
            blob_client_jj.upload_blob(data, overwrite=True)
        with open('{}_{}'.format('ferris', graph_fname), 'rb') as data:
            blob_client_ferris.upload_blob(data, overwrite=True)
        
            
        # upload to Azure
        with open(upload_file_path, "rb") as data:
            blob_client_data.upload_blob(data, overwrite=True)

        time.sleep(60*15)

except Exception as ex:
    print('Exception:')
    print(ex)