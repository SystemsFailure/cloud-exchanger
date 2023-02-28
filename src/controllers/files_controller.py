from google.cloud import storage
import io
import os
import tqdm

def upload_as_file_with_progress(project_id:str='exchangefiles-ae5e7', bucket_name:str='exchangefiles-ae5e7.appspot.com',):
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name=bucket_name)
    blob = bucket.blob(blob_name='/package/Enslaved.mp3')
    with open('/home/leonhard/Downloads/Enslaved.mp3', 'rb') as in_file:
        total_bytes = os.fstat(in_file.fileno()).st_size
        with tqdm.tqdm.wrapattr(in_file, 'read', total=total_bytes, miniters=1, desc='Upload ...') as file_obj:
            blob.upload_from_file(file_obj=file_obj, size=total_bytes)
            return blob

def download_as_file(project_id:str='exchangefiles-ae5e7', bucket_name:str='exchangefiles-ae5e7.appspot.com', source_blob_name:str='empty2023', location_file:str='/home/leonhard/Desktop/up') -> None:
    local_storage_client = storage.Client(project=project_id)
    local_bucket = local_storage_client.bucket(bucket_name=bucket_name)
    local_blob = local_bucket.blob(source_blob_name)
    local_blob.download_to_filename(filename=location_file+f'/{local_blob.name}')
    print('Download storage object {} from bucket {} to local file {}.'.format(source_blob_name, bucket_name, location_file))

def download_portion_file(
    project_id:str='exchangefiles-ae5e7',
    bucket_name:str='exchangefiles-ae5e7.appspot.com', 
    source_blob_name:str='empty2023', 
    location_file:str='/home/leonhard/Desktop/up',
    start_byte:int=0,
    end_byte:int=0,
):
    local_storage_client:storage.Client = storage.Client(project=project_id)
    local_bucket = local_storage_client.bucket(bucket_name=bucket_name)
    local_blob = local_bucket.blob(blob_name=source_blob_name)
    local_blob.download_to_filename(location_file, start=start_byte, end=end_byte)

    print(
        "Downloaded bytes {} to {} of object {} from bucket {} to local file {}.".format(
            start_byte, end_byte, source_blob_name, bucket_name, location_file
        )
    )

def download_stream_file(project_id:str='exchangefiles-ae5e7', bucket_name:str='exchangefiles-ae5e7.appspot.com', source_blob_name:str='empty2023') -> io.BytesIO:
    file_object: io.BytesIO = io.BytesIO()
    local_storage_client:storage.Client = storage.Client(project=project_id)
    local_bucket = local_storage_client.bucket(bucket_name=bucket_name)
    local_blob = local_bucket.blob(blob_name=source_blob_name)
    local_blob.download_to_file(file_object)
    print(f"Downloaded blob {source_blob_name} to file-like object.")
    return file_object

# Uploads methods

def upload_blob(project_id, bucket_name, source_file_name, location_blob_name) -> None:
    generation_match_precondition = 0
    local_storage_client = storage.Client(project=project_id)
    local_bucket = local_storage_client.bucket(bucket_name=bucket_name)
    blob = local_bucket.blob(blob_name=location_blob_name)
    result = blob.upload_from_filename(filename=source_file_name, if_generation_match=generation_match_precondition)
    print('result : {}'.format(result))
    print(
        f"File {source_file_name} uploaded to cloud like {location_blob_name}."
    )

class LocalStoreInstance:
    project_id: str = ''
    bucket_name: str = ''
    local_storage_client = None
    default_meta_data = {}
    def __init__(self, project_id: str = 'exchangefiles-ae5e7', bucket_name: str = 'exchangefiles-ae5e7.appspot.com', default_meta_data:dict={}) -> None:
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.default_meta_data = default_meta_data
    
        if self.project_id:
            self.local_storage_client = storage.Client(project=self.project_id)
        else:
            print('{} is None'.format(self.project_id))

    def get_list_blobs(self) -> list:
        list_ = []
        if self.local_storage_client:
            list_blobs = self.local_storage_client.list_blobs(bucket_or_name=self.bucket_name)
            for blob in list_blobs:
                object_ = {
                    'name': blob.name,
                    'size': blob.size,
                    'metadata': blob.metadata or {},
                }
                list_.append(object_)
        return list_

    def write_to_cloud(self, blob_name, local_file):
        local_bucket = self.local_storage_client.bucket(bucket_name=self.bucket_name)
        local_blob = local_bucket.blob(blob_name=blob_name)

        with local_blob.open('w') as f:
            #file - it's file which we'll write in cloud / type data it is bytes / only bytes can writed to gcs
            f.write(local_file)

    def read_from_cloud(self, blob_name):
        local_bucket = self.local_storage_client.bucket(bucket_name=self.bucket_name)
        local_blob = local_bucket.blob(blob_name=blob_name)
        with local_blob.open('r') as f:
            print(f.read())

    def delete_blob_object(self, blob_name):
        local_bucket = self.local_storage_client.bucket(bucket_name=self.bucket_name)
        local_blob = local_bucket.blob(blob_name=blob_name)
        generation_match_precondition = None

        local_blob.reload()
        generation_match_precondition = local_blob.generation
        local_blob.delete(if_generation_match=generation_match_precondition)
        print(f'Blob {blob_name} deleted.')

    def set_metadata_to_blob_object(self, blob_name, blob_metadata_vl: dict = default_meta_data):
        local_bucket = self.local_storage_client.bucket(bucket_name=self.bucket_name)
        local_blob = local_bucket.blob(blob_name=blob_name)
        local_blob.metadata = blob_metadata_vl


    def get_list_blobs_with_prefix(self, prefix, delimiter=None):
        # However, if you specify prefix='a/' and delimiter='/', you'll get back
        # only the file directly under 'a/':
        #     a/1.txt
        list_ = []
        if self.local_storage_client:
            list_blobs_prefix = self.local_storage_client.list_blobs(bucket_or_name=self.bucket_name, prefix=prefix, delimiter=delimiter)
            for blob_prefix in list_blobs_prefix:
                list_.append(blob_prefix)
                print(blob_prefix.name)
            if delimiter:
                print('delimiter')
                for prefix_ in list_blobs_prefix.prefixes:
                    print(prefix_)



#/home/leonhard/Desktop