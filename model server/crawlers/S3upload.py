import requests
import boto3
from config.config import region_name, aws_access_key_id, aws_secret_access_key, bucket_name

# S3 연결 환경 변수 설정
s3 = boto3.client('s3', region_name = region_name, aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key)

# S3 버킷 이름
bucket_name = bucket_name

# AWS S3 업로드 함수 정의
def upload_to_s3(image_url, bucket_name, object_name):
    """
    이미지 URL을 다운로드하고 S3 버킷에 업로드합니다.
    :param image_url: 업로드할 이미지의 URL
    :param bucket_name: S3 버킷 이름
    :param object_name: S3에 저장될 객체 이름
    :return: 업로드 성공 여부 (True/False)
    """
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            print(f"이미지를 다운로드할 수 없습니다. 상태 코드: {response.status_code}")
            return False

        s3.put_object(Bucket=bucket_name, Key=object_name, Body=response.content)
        print(f"이미지가 성공적으로 업로드되었습니다: s3://{bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"S3 업로드 중 오류 발생: {e}")
        return False