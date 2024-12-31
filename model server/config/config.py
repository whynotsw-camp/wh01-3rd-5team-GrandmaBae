DATABASE_CONFIG = {
    "host": "your RDS host",
    "port": "#Your port",
    "user": "Your username",
    "password": "Your password",
    "database": "Your DB name",
}

YOLO_C_MODEL_PATH = "/home/ubuntu/project/models/best.pt"
YOLO_P_MODEL_PATH = "/home/ubuntu/project/models/yolov8s.pt"
RESNET_PRETRAINED = True

LIVE_URL = "https://www.lotteimall.com/main/viewMain.lotte#/main/tvschedule.lotte"
TV_URL = "https://www.lotteimall.com/display/viewDispShop.lotte?disp_no="

disp_numbers = {
    "top": [5157107, 5157108, 5157109, 5157111],
    "bottom": [5157113, 5157114],
    "onepiece": [5157112, 5157119],
    "outer": [5157110, 5157115, 5157116, 5157117, 5157118]
}

region_name = 'ap-northeast-2'
aws_access_key_id = 'access_key_id'
aws_secret_access_key = 'secret_access_key'
bucket_name = "s3-bucket-name"

cors_address = "web ip"