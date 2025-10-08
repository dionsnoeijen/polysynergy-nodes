import os
import boto3
import hashlib
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional


class S3ImageService:
    """Service for uploading images to S3 with project-based bucket isolation"""
    
    def __init__(self):
        self.is_lambda = os.getenv("AWS_EXECUTION_ENV") is not None
        
        if self.is_lambda:
            # In Lambda, use IAM role
            self.s3_client = boto3.client(
                's3',
                region_name=os.getenv("AWS_REGION", "eu-central-1")
            )
        else:
            # Local development
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "eu-central-1")
            )
        
        self.region = os.getenv("AWS_REGION", "eu-central-1")
        self.cdn_domain = os.getenv("CDN_DOMAIN")  # Optional CloudFront domain
        self.use_signed_urls = os.getenv("USE_SIGNED_URLS", "true").lower() == "true"
    
    def get_bucket_name(self) -> str:
        """Get bucket name based on project ID"""
        project_id = os.getenv('PROJECT_ID', 'default')
        tenant_id = os.getenv('TENANT_ID', 'default')
        
        # For long tenant/project IDs (UUIDs), create shortened versions using hash
        # This ensures bucket names stay within S3 limits (63 chars) and remain unique
        if len(tenant_id) > 8:
            tenant_short = hashlib.md5(tenant_id.encode()).hexdigest()[:8]
        else:
            tenant_short = tenant_id
            
        if len(project_id) > 8:
            project_short = hashlib.md5(project_id.encode()).hexdigest()[:8]
        else:
            project_short = project_id
        
        # Bucket naming pattern: polysynergy-{tenant_hash}-{project_hash}-media
        # This keeps bucket names under 63 characters while maintaining uniqueness
        bucket_name = f"polysynergy-{tenant_short}-{project_short}-media".lower()
        
        # Ensure bucket name is valid (lowercase, no underscores)
        bucket_name = bucket_name.replace('_', '-')
        
        # Final safety check - should never exceed 63 chars with our hash approach
        if len(bucket_name) > 63:
            # Emergency fallback: use shorter hashes
            tenant_short = hashlib.md5(tenant_id.encode()).hexdigest()[:6]
            project_short = hashlib.md5(project_id.encode()).hexdigest()[:6]
            bucket_name = f"poly-{tenant_short}-{project_short}-media".lower()
        
        return bucket_name
    
    def ensure_bucket_exists(self, bucket_name: str) -> bool:
        """Ensure the bucket exists, create if it doesn't"""
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            # Bucket exists - only try to set public policy if signed URLs are disabled
            if not self.use_signed_urls:
                self.set_bucket_public_read_policy(bucket_name)
            return True
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Bucket doesn't exist, try to create it
                try:
                    if self.region == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region}
                        )

                    # Set CORS for all buckets
                    self.set_bucket_cors(bucket_name)

                    # Only set public access policy if signed URLs are disabled
                    if not self.use_signed_urls:
                        self.set_bucket_public_read_policy(bucket_name)

                    return True
                except ClientError as create_error:
                    print(f"Failed to create bucket {bucket_name}: {create_error}")
                    return False
            else:
                print(f"Error checking bucket {bucket_name}: {e}")
                return False
    
    def set_bucket_cors(self, bucket_name: str):
        """Set CORS configuration for the bucket"""
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['GET', 'HEAD'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': ['ETag'],
                'MaxAgeSeconds': 3000
            }]
        }
        
        try:
            self.s3_client.put_bucket_cors(
                Bucket=bucket_name,
                CORSConfiguration=cors_configuration
            )
        except ClientError as e:
            print(f"Failed to set CORS for bucket {bucket_name}: {e}")
    
    def set_bucket_public_read_policy(self, bucket_name: str):
        """Set bucket policy to allow public read access"""
        import json

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        try:
            self.s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy)
            )
            print(f"Successfully set public read policy for bucket {bucket_name}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            # Don't fail the entire operation if public access is blocked
            if error_code == 'AccessDenied' and 'BlockPublicPolicy' in str(e):
                print(f"Note: Public bucket policy blocked for {bucket_name} - using signed URLs instead")
            else:
                print(f"Failed to set public read policy for bucket {bucket_name}: {e}")
            # Continue execution - signed URLs will be used as fallback
    
    def upload_image(
        self,
        image_data: bytes,
        key: str,
        content_type: str = 'image/png',
        metadata: Optional[Dict[str, str]] = None,
        cache_control: str = 'public, max-age=31536000'  # 1 year cache
    ) -> Dict[str, Any]:
        """Upload image to S3 and return the URL"""
        
        bucket_name = self.get_bucket_name()
        
        # Ensure bucket exists
        if not self.ensure_bucket_exists(bucket_name):
            return {
                'success': False,
                'error': f'Failed to ensure bucket {bucket_name} exists'
            }
        
        try:
            # Prepare upload parameters
            upload_params = {
                'Bucket': bucket_name,
                'Key': key,
                'Body': image_data,
                'ContentType': content_type,
                'CacheControl': cache_control
                # Note: No ACL needed - bucket policy handles public access
            }
            
            # Add metadata if provided
            if metadata:
                upload_params['Metadata'] = metadata
            
            # Upload the image
            response = self.s3_client.put_object(**upload_params)
            
            # Generate URL based on configuration
            if self.cdn_domain:
                # Use CloudFront CDN if available
                url = f"https://{self.cdn_domain}/{key}"
            elif self.use_signed_urls:
                # Generate pre-signed URL for private bucket access
                url = self.get_signed_url(key, expiration=86400)  # 24 hours
                if not url:
                    # Fallback to direct URL (may not work if bucket is private)
                    url = f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{key}"
            else:
                # Use direct S3 URL (requires public bucket)
                url = f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{key}"
            
            return {
                'success': True,
                'url': url,
                'bucket': bucket_name,
                'key': key,
                'etag': response.get('ETag', '').strip('"'),
                'version_id': response.get('VersionId')
            }
            
        except ClientError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_image(self, key: str) -> bool:
        """Delete an image from S3"""
        bucket_name = self.get_bucket_name()
        
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=key)
            return True
        except ClientError as e:
            print(f"Failed to delete {key} from {bucket_name}: {e}")
            return False
    
    def get_signed_url(self, key: str, expiration: int = 3600) -> Optional[str]:
        """Generate a pre-signed URL for temporary access"""
        bucket_name = self.get_bucket_name()
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Failed to generate signed URL for {key}: {e}")
            return None
    
    def refresh_signed_url(self, key: str, expiration: int = 86400) -> Optional[str]:
        """Generate a fresh pre-signed URL for an existing image"""
        return self.get_signed_url(key, expiration)
    
    def get_image_metadata(self, key: str) -> Dict[str, Any]:
        """Get metadata for an image from S3"""
        bucket_name = self.get_bucket_name()
        
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=key)
            return {
                'success': True,
                'metadata': response.get('Metadata', {}),
                'size': response.get('ContentLength', 0),
                'last_modified': response.get('LastModified'),
                'etag': response.get('ETag', '').strip('"'),
                'content_type': response.get('ContentType', 'unknown')
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return {'success': False, 'error': 'Image not found'}
            else:
                return {'success': False, 'error': str(e)}
    
    def get_image_url(self, key: str) -> str:
        """Get the URL for an image (same logic as in upload_image)"""
        bucket_name = self.get_bucket_name()
        
        if self.cdn_domain:
            return f"https://{self.cdn_domain}/{key}"
        elif self.use_signed_urls:
            signed_url = self.get_signed_url(key, expiration=86400)  # 24 hours
            if signed_url:
                return signed_url
            # Fallback to direct URL
            return f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{key}"
        else:
            return f"https://{bucket_name}.s3.{self.region}.amazonaws.com/{key}"