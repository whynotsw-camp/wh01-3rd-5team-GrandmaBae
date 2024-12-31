import boto3
from botocore.exceptions import ClientError
import logging
from urllib.parse import urlparse
# S3 객체에 대한 임시 인증 정보가 포함된 presigned URL로 반환

class S3Manager:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str, region_name: str, bucket_name: str):
        self.s3_client = boto3.client('s3',
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      region_name=region_name)
        self.bucket_name = bucket_name
        self.logger = logging.getLogger(__name__)
    
    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                                                            Params={'Bucket': self.bucket_name,
                                                                    'Key': object_name},
                                                            ExpiresIn=expiration)
        except ClientError as e:
            self.logger.error(f"Error generating presigned URL: {e}")
            return None
        return response

    def get_image_url(self, s3_path: str) -> str: # s3_path 입력값: "s3://shopping-sm/241218/12813721_0.jpg"
        parsed_url = urlparse(s3_path)
        object_name = parsed_url.path.lstrip('/') # 241218/12813721_0.jpg
        url = self.generate_presigned_url(object_name)
        if url is None:
            self.logger.warning(f"Failed to generate presigned URL for path: {s3_path}")
            return f"https://{self.bucket_name}.s3.amazonaws.com/{object_name}"
        return url
