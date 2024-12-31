# config.py
# 유지보수성 향상, 개발/테스트/프로덕션 환경에 따라 환경 분리
# 네트워크
SECRET_KEY = 'your-secret-key'
API_SERVER_URL = "http://3.38.245.145:8000" #"http://127.0.0.1:8000"  # localhost 사용
WEB_SERVER_URL = "http://192.168.101.59:5000" # 테스트용 서버
WEB_SERVER_URL = "http://127.0.0.1:5000" # 로컬 개발용 서버

# 전역 변수
VIDEO_PATH = 'assets/videos/시연영상1_파란옥순_아울렛.mp4'

# S3
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
AWS_REGION = 'ap-northeast-2'
S3_BUCKET_NAME = 's3-bucket=name'