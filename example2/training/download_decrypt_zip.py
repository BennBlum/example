import os
import shutil
import zipfile
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient
from azure.ai.ml import MLClient
from enum import Enum

class EnvVars(Enum):
    BASE_PATH = "BASE_PATH"
    DATA_ASSET_NAME = "DATA_ASSET_NAME"
    CONTAINER_NAME = "CONTAINER_NAME"
    SUBSCRIPTION_ID = "SUBSCRIPTION_ID"
    RESOURCE_GROUP = "RESOURCE_GROUP"
    WORKSPACE = "WORKSPACE"
    KEY_VAULT_URL = "KEY_VAULT_URL"
    KEY_SECRET_NAME = "KEY_SECRET_NAME"
    AZURE_STORAGE_URL = "AZURE_STORAGE_URL"

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_env_var(var: EnvVars):
    value = os.getenv(var.value)
    if not value:
        raise EnvironmentError(f"Environment variable {var.value} is not set")
    return value

def check_env_vars():
    for var in EnvVars:
        get_env_var(var)

def extract_zip(file_path, extract_to):
    shutil.rmtree(extract_to, ignore_errors=True)
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)

def get_secret(credential, key_vault_url, secret_name):
    with SecretClient(vault_url=key_vault_url, credential=credential) as client:
        return client.get_secret(secret_name).value

def download_blob(blob_service, blob_name, container_name, download_path):
    blob_client = blob_service.get_blob_client(container=container_name, blob=blob_name)
    with open(download_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

def decrypt_file(encrypted_file_path, decrypted_file_path, secret):
    # Omitted in this example - decryption happes here
    pass

def download_and_decrypt_blob(ml_client, blob_service, encrypted_file_path, decrypted_file_path, secret):
    blob_name = list(ml_client.data.list(name=get_env_var(EnvVars.DATA_ASSET_NAME)))[0].path.split("/")[-1]
    download_blob(blob_service, blob_name, get_env_var(EnvVars.CONTAINER_NAME), encrypted_file_path)
    decrypt_file(encrypted_file_path, decrypted_file_path, secret)

def main():
    setup_logging()
    try:
        check_env_vars()

        base_path = get_env_var(EnvVars.BASE_PATH)
        file_path = os.path.join(base_path, "encrypted")
        encrypted_full_file_name = os.path.join(file_path, "encrypted_blob.zip")
        decrypted_full_file_name = os.path.join(file_path, "decrypted.zip")
        dataset_path = os.path.join(base_path, "dataset")

        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential,
            get_env_var(EnvVars.SUBSCRIPTION_ID),
            get_env_var(EnvVars.RESOURCE_GROUP),
            get_env_var(EnvVars.WORKSPACE)
        )

        secret = get_secret(credential, get_env_var(EnvVars.KEY_VAULT_URL), get_env_var(EnvVars.KEY_SECRET_NAME))

        with BlobServiceClient(account_url=get_env_var(EnvVars.AZURE_STORAGE_URL), credential=credential) as service:
            download_and_decrypt_blob(ml_client, service, encrypted_full_file_name, decrypted_full_file_name, secret)

        extract_zip(decrypted_full_file_name, dataset_path)
        logging.info("Process completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()