import boto3

class S3API:
    def __init__(self, access_key: str, secret_key: str, region_name: str):
        self.s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

    def create_bucket(self, bucket_name: str):
        self.s3.create_bucket(Bucket=bucket_name)

    def list_buckets(self):
        return [bucket.name for bucket in self.s3.buckets.all()]

    def upload_file(self, local_file_path: str, bucket_name: str, s3_file_path: str):
        self.s3.Object(bucket_name, s3_file_path).put(Body=open(local_file_path, 'rb'))

    def download_file(self, bucket_name: str, s3_file_path: str, local_file_path: str):
        self.s3.Object(bucket_name, s3_file_path).download_file(local_file_path)

    def delete_file(self, bucket_name: str, s3_file_path: str):
        self.s3.Object(bucket_name, s3_file_path).delete()

    def delete_bucket(self, bucket_name: str):
        bucket = self.s3.Bucket(bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

    def list_files(self, bucket_name: str):
        return [obj.key for obj in self.s3.Bucket(bucket_name).objects.all()]

    def get_file_url(self, bucket_name: str, s3_file_path: str):
        return self.s3.meta.client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': s3_file_path}, ExpiresIn=3600)

      
# Create an instance of the S3API class
s3 = S3API(access_key='your_access_key', secret_key='your_secret_key', region_name='your_region_name')

# Create a new S3 bucket
s3.create_bucket(bucket_name='my-new-bucket')

# List all S3 buckets
print(s3.list_buckets())

# Upload a local file to the S3 bucket
s3.upload_file(local_file_path='/path/to/local/file', bucket_name='my-new-bucket', s3_file_path='path/to/s3/file')

# Download an S3 file to the local machine
s3.download_file(bucket_name='my-new-bucket', s3_file_path='path/to/s3/file', local_file_path='/path/to/local/file')

# Delete an S3 file
s3.delete_file(bucket_name='my-new-bucket', s3_file_path='path/to/s3/file')

# Delete an S3 bucket and all its contents
s3.delete_bucket(bucket_name='my-new-bucket')

# List all files in an S3 bucket
print(s3.list_files(bucket_name='my-existing-bucket'))

# Get a pre-signed URL for an S3 file
print(s3.get_file_url(bucket_name='my-existing-bucket', s3_file_path='path/to/s3/file'))
