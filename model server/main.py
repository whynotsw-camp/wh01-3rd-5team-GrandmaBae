import logging
import uuid
from fastapi import FastAPI, UploadFile, File, Form
import json
import os
import shutil
import cv2
from processors.detector import Detector
from processors.vectorize import load_resnet_model, image_to_vector
from search.annoy_search import build_annoy_index, search_similar_vectors
from db.db import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware
import base64
from config.config import DATABASE_CONFIG, cors_address

logging.basicConfig(
    level=logging.DEBUG,  # 디버그 로그까지 출력
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

UPLOAD_DIR = "uploads/"
OUTPUT_DIR = "outputs/"

# 설정 정보
DB_CONFIG = DATABASE_CONFIG
VECTOR_DIM = 2048

model = load_resnet_model()
detector = Detector(
    model_path="models/best.pt",
    person_model_path="models/yolov8s.pt"
)
db_manager = DatabaseManager()

# 사람 객체 인식 엔드포인트
@app.post("/detect/person/")
async def api_detect_person(file: UploadFile = File(...)):
    try:
        # 요청 ID 생성
        request_id = str(uuid.uuid4())

        # 파일 저장 경로 설정 (request_id 포함)
        input_filename = f"input_{request_id}.jpg"
        annotated_filename = f"annotated_{request_id}.jpg"
        output_dir = os.path.join(UPLOAD_DIR, request_id)
        os.makedirs(output_dir, exist_ok=True)

        input_path = os.path.join(output_dir, input_filename)
        annotated_path = os.path.join(output_dir, annotated_filename)

        # 업로드 파일 저장
        with open(input_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 사람 객체 탐지 실행
        annotated_path, person_boxes = detector.detect_person(input_path, output_dir)

        # 주석 이미지 파일 확인
        if not os.path.exists(annotated_path):
            return {"error": "Annotated image not found."}

        # 주석 이미지 Base64 인코딩
        with open(annotated_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # 응답 반환
        return {
            "message": "Person detection completed.",
            "request_id": request_id,
            "annotated_image": encoded_image,
            "image_format": "base64",
            "boxes": [{"id": id, "coordinates": {"x1": box[0], "y1": box[1], "x2": box[2], "y2": box[3]}} for id, box in
                      enumerate(person_boxes)],
        }
    except Exception as e:
        return {"error": str(e)}


# 의류 객체 탐지 후 데이터베이스 검색
@app.post("/detect-and-search/")
async  def detect_and_search_clothes(
        file: UploadFile = File(...),
        person_box: str = Form(...)
):
    try:
        logging.debug(f"Received request: file={file.filename}, person_box={person_box}")

        # 요청 ID 생성
        request_id = str(uuid.uuid4())

        # 파일 저장 경로 설정 (요청 ID 포함)
        input_filename = f"input_{request_id}.jpg"
        cropped_person_filename = f"cropped_person_{request_id}.jpg"
        output_dir = os.path.join(UPLOAD_DIR, request_id)
        os.makedirs(output_dir, exist_ok=True)

        input_path = os.path.join(output_dir, input_filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # person_box 파싱
        box_data = json.loads(person_box)
        x1, y1, x2, y2 = box_data["x1"], box_data["y1"], box_data["x2"], box_data["y2"]

        # 이미지 크롭
        image = cv2.imread(input_path)
        if image is None:
            return {"error": f"Cannot read image: {input_path}"}

        cropped_person_path = os.path.join(output_dir, cropped_person_filename)
        cropped_person_path = detector.crop_image(image, (x1, y1, x2, y2), cropped_person_path)
        if cropped_person_path is None:
            return {"error": "Failed to crop person image. Invalid coordinates."}

        # 의류 객체 탐지
        cropped_objects = detector.detect_clothes(cropped_person_path, output_dir)
        logging.debug(f"Cropped objects detected: {cropped_objects}")

        # Annoy 검색 준비
        with db_manager as db:
            vectors = db.fetch_vectors()
            annoy_index, id_to_product = build_annoy_index(vectors, VECTOR_DIM)

            # 유사도 검색 및 상품 정보 조회
            unique_products = {}
            for obj in cropped_objects:
                image_path = obj["path"]
                obj_image = cv2.imread(image_path)

                query_vector = image_to_vector(obj_image, model)
                logging.debug(f"Query vector: {query_vector}")
                if query_vector is None:
                    continue

                similar_items = search_similar_vectors(annoy_index, id_to_product, query_vector, 20)
                logging.debug(f"Similar items for object {obj['path']}: {similar_items}")

                for item in similar_items:
                    product_id = item["product_id"]
                    distance = item['distance']

                    # product_type 조회
                    query_product_type = """
                        SELECT DISTINCT product_type
                        FROM vector_info
                        WHERE product_id = %s
                    """
                    db.cursor.execute(query_product_type, (product_id,))
                    result = db.cursor.fetchone()
                    product_type = result[0] if result else None

                    # 상품 정보 초기화
                    product_info = None
                    image_urls = []

                    # 상품 정보 조회
                    if product_type == "live":
                        query_live_product = """
                            SELECT DISTINCT product_name, product_price, product_category
                            FROM live_product_info
                            WHERE product_id = %s
                        """
                        db.cursor.execute(query_live_product, (product_id,))
                        product_data = db.cursor.fetchone()

                        if product_data:
                            product_info = {
                                "name" : product_data[0],
                                "price" : product_data[1],
                                "category" : product_data[2]
                            }

                    elif product_type == "outlet":
                        query_tv_product = """
                            SELECT DISTINCT tv_name, tv_price, tv_category
                            FROM tv_product_info
                            WHERE tv_id = %s
                        """
                        db.cursor.execute(query_tv_product, (product_id,))
                        product_data = db.cursor.fetchone()

                        if product_data:
                            product_info = {
                                "name" : product_data[0],
                                "price" : product_data[1],
                                "category" : product_data[2]
                            }

                    # 이미지 정보 조회
                    query_images = """
                        SELECT DISTINCT s3_url
                        FROM vector_info
                        WHERE product_id = %s
                    """

                    db.cursor.execute(query_images, (product_id,))
                    image_urls = [row[0] for row in db.cursor.fetchall()]

                    # 중복 제거
                    if product_id not in unique_products and product_info:
                        unique_products[product_id] = {
                            "product_id": product_id,
                            "name": product_info.get("name", "N/A"),
                            "price": product_info.get("price", "N/A"),
                            "category": product_info.get("category", "N/A"),
                            "images": image_urls,
                            "type" : product_type,
                            "distance" : distance
                        }

        # 정렬 : 유사도 순으로 정렬
        sorted_products = sorted(
            unique_products.values(),
            key=lambda x: x['distance']
        )

        # 크롭된 이미지 Base64 인코딩
        with open(cropped_person_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # 응답 데이터 생성
        return {
            "cropped_image": encoded_image,
            "products": sorted_products
        }

    except Exception as e:
        logging.error(f"Error in /detect-and-search/: {e}")
        return {"error": str(e)}