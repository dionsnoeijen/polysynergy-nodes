import io
import json
import os
import boto3
import logging
import mimetypes
from botocore.exceptions import NoCredentialsError, ClientError

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self, tenant_id, public=False):
        self.tenant_id = tenant_id
        self.public = public
        self.region = os.getenv('AWS_REGION', 'eu-central-1')
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=self.region
        )

        scope = "public" if public else "private"
        self.bucket_name = f"ps-{scope}-files-{tenant_id}".lower()

        if not self._bucket_exists(self.bucket_name):
            self._create_bucket(self.bucket_name)

    def _bucket_exists(self, bucket_name):
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False

    def _create_bucket(self, bucket_name):
        logger.info(f"Creating bucket: {bucket_name}")
        try:
            self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )
            logger.info(f"Bucket created: {bucket_name}")

            if self.public:
                self._set_public_bucket_policy(bucket_name)

        except Exception as e:
            logger.error(f"Failed to create bucket {bucket_name}: {e}")
            raise

    def _set_public_bucket_policy(self, bucket_name):
        try:
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowPublicReadAccess",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }
            self.s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy)
            )
            logger.info(f"Public bucket policy set for: {bucket_name}")
        except Exception as e:
            logger.error(f"Failed to set public bucket policy: {e}")

    def upload_file(self, file_obj, file_key):
        try:
            content_type, _ = mimetypes.guess_type(file_key)

            self.s3_client.upload_fileobj(
                io.BytesIO(file_obj),
                self.bucket_name,
                file_key,
                ExtraArgs={
                    'ContentType': content_type
                }
            )
            logger.info(f"Uploaded: {file_key}")
            if self.public:
                return f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
            else:
                return self.get_file_url(file_key)
        except NoCredentialsError:
            logger.error("No valid AWS credentials found.")
            return None
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return None

    def get_file_url(self, file_key):
        try:
            return self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=3600
            )
        except Exception as e:
            logger.error(f"URL generation error: {e}")
            return None

    def list_files(self, prefix=""):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            return [item['Key'] for item in response.get('Contents', [])]
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
