from prefect import flow
import os

from prefect_azure import AzureBlobStorageCredentials
from prefect_azure.blob_storage import blob_storage_download



os.environ[""] = os.get

@flow
def dataset_blob_storage_download_flow():
    connection_string = "connection_string"
    blob_storage_credentials = AzureBlobStorageCredentials(
        connection_string=connection_string,
    )
    data = blob_storage_download(
        blob="prefect.txt",
        container="prefect",
        azure_credentials=blob_storage_credentials,
    )
    return data

dataset_blob_storage_download_flow()


custom_blob_storage_download_flow = dataset_blob_storage_download_flow.with_options(
    name="My custom task name",
    retries=2,
    retry_delay_seconds=10,
)

################ create block ###################
