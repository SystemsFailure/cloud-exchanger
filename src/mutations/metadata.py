from google.cloud import storage

class Bucket_mutations:
    project_id = None
    local_storage_client = None
    def __init__(self, project_id:str) -> None:
        self.project_id = project_id
        self.local_storage_client = storage.Client(project=project_id)

    # This method call only with permission IAM google.cloud.storage 
    def delete_bucket(self, bucket_name:str) -> None:
        local_bucket = self.local_storage_client.get_bucket(bucket_or_name=bucket_name)
        local_bucket.delete()
        print('{} been deleted'.format(local_bucket.name))


def get_all_metadata_by_bucket(bucket_name:str = 'exchangefiles-ae5e7.appspot.com', project_id:str = 'exchangefiles-ae5e7') -> None:
    """ prints out a bucket's metadata. """
    # bucket_name = 'my_bucket_name'
    # All other scripts files where to invoke some cloud client needed in posfix ((LOCAL))
    local_storage_client = storage.Client(project=project_id)
    local_bucket = local_storage_client.get_bucket(bucket_or_name=bucket_name)

    if (local_bucket):
            print('\nMETADATA: \n')
            print("ID: {}".format(local_bucket.id))
            print(f"Name: {local_bucket.name}")
            print(f"Storage Class: {local_bucket.storage_class}")
            print(f"Location: {local_bucket.location}")
            print(f"Location Type: {local_bucket.location_type}")
            print(f"Cors: {local_bucket.cors}")
            print(f"Default Event Based Hold: {local_bucket.default_event_based_hold}")
            print(f"Default KMS Key Name: {local_bucket.default_kms_key_name}")
            print(f"Metageneration: {local_bucket.metageneration}")
            print(f"Public Access Prevention: {local_bucket.iam_configuration.public_access_prevention}")
            print(f"Retention Effective Time: {local_bucket.retention_policy_effective_time}")
            print(f"Retention Period: {local_bucket.retention_period}")
            print(f"Retention Policy Locked: {local_bucket.retention_policy_locked}")
            print(f"Requester Pays: {local_bucket.requester_pays}")
            print(f"Self Link: {local_bucket.self_link}")
            print(f"Time Created: {local_bucket.time_created}")
            print(f"Versioning Enabled: {local_bucket.versioning_enabled}")
            print(f"Labels: {local_bucket.labels}")
    else:
        print('not found so bucket')


# bucket_name = 'exchangefiles-ae5e7.appspot.com/'
# bucket = storage_client.create_bucket(bucket_name)
# gs://exchangefiles-ae5e7.appspot.com/
