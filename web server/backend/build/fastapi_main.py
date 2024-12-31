from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
import shutil
import cv2
import base64
import logging
from detect_person import detect_person

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # Flask 서버의 주소를 여기에 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads/"
OUTPUT_DIR = "outputs/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 사람 객체 인식 엔드포인트
@app.post("/detect/person/")
async def api_detect_person(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
     
    detected_path = os.path.join(OUTPUT_DIR, f"annotated_{file.filename}")
    annotated_image, person_boxes = detect_person(input_path)
    cv2.imwrite(detected_path, annotated_image)
    
    # 이미지를 Base64로 인코딩
    with open(detected_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    return {
        "message": "Person detection completed.",
        "annotated_image": encoded_image,
        "image_format": "base64",
        "boxes": [{"id": id, "coordinates": {"x1": box[0], "y1": box[1], "x2": box[2], "y2": box[3]}} for id, box in person_boxes],
    }


# 테스트용 이미지 경로
TEST_IMAGE_PATH = "../static/assets/YOLO/croppedTestImg.png"

@app.post("/detect-and-search/")
async def detect_and_search_clothes(
    file: UploadFile = File(...),
    person_box: str = Form(...)
):
    logging.debug(f"Received request: file={file.filename}, person_box={person_box}")
    # 업로드된 파일 저장
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print('파일 저장 완료했습니다.\n personBox 파싱 및 YOLO와 유사도 검사 과정을 거쳐 알맞은 형식에 맞게 response 합니다.')
    # person_box를 JSON 문자열로 파싱
    box_data = json.loads(person_box)
    print("API서버에서 받은 Box_data:", box_data)
    

    # AI 로직 구현 예정 우선의 형식만 맞춰서 테스트
    
    # 테스트용 응답
    with open(TEST_IMAGE_PATH, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    example_response = {
        "cropped_image": encoded_image,
        "products": [
            {
                "product_id": 12813721,
                "name": "Example Product 1",
                "price": 300000,
                "category": "상의",
                "images": [
                    "s3://shopping-sm/241218/12813721_0.jpg",
                    "s3://shopping-sm/241218/12813721_1.jpg",
                    "s3://shopping-sm/241218/12813721_2.jpg"
                ]
            },
            {
                "product_id": 12815985,
                "name": "Example Product 2",
                "price": 29.99,
                "category": "하의",
                "images": [
                    "s3://shopping-sm/241218/12815985_0.jpg",
                    "s3://shopping-sm/241218/12815985_1.jpg",
                    "s3://shopping-sm/241218/12815985_2.jpg"
                ]
            },
                        {
                "product_id": 12815985,
                "name": "Example Product 2",
                "price": 29.99,
                "category": "상의",
                "images": [
                    "s3://shopping-sm/241218/12815985_0.jpg",
                    "s3://shopping-sm/241218/12815985_1.jpg",
                    "s3://shopping-sm/241218/12815985_2.jpg"
                ]
            }
        ]
    }

    return JSONResponse(content=example_response)


# return {
#             "cropped_image": encoded_image,
#             "products": products
#         }

# products.append({
#                             "product_id": product_id,
#                             "name": product_info[0],
#                             "price": product_info[1],
#                             "category": product_info[2],
#                             "images": image_urls
#                         })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



    # x1, y1, x2, y2 = box_data["x1"], box_data["y1"], box_data["x2"], box_data["y2"]

    # 사람 이미지 크롭
    # cropped_dir = os.path.join(OUTPUT_DIR, "cropped")
    # os.makedirs(cropped_dir, exist_ok=True)
    # cropped_path = os.path.join(cropped_dir, f"cropped_person.jpg")
    # image = cv2.imread(input_path)
    # cropped_image = image[y1:y2, x1:x2]
    # cv2.imwrite(cropped_path, cropped_image)

    # # 의류 탐지
    # clothes_dir = os.path.join(OUTPUT_DIR, "clothes")
    # os.makedirs(clothes_dir, exist_ok=True)
    # cropped_objects, annotated_clothes = detect_clothes(cropped_path, clothes_dir)

    # # 유사도 검색 준비
    # vectors = fetch_vectors_from_postgresql(DB_CONFIG)
    # annoy_index, id_to_product = build_annoy_index(vectors, VECTOR_DIM)

    # # 각 의류 이미지에 대해 유사도 검색
    # results = []
    # for obj in cropped_objects:
    #     image_path = obj["path"]
    #     class_id = obj["class_id"]

    #     # 이미지 벡터화
    #     query_vector = image_to_vector(image_path, model)
    #     if query_vector is None:
    #         results.append({
    #             "class_id": class_id,
    #             "error": f"Failed to vectorize image: {image_path}"
    #         })
    #         continue

    #     # Annoy 유사도 검색
    #     similar_items = search_similar_vectors(annoy_index, id_to_product, query_vector)
    #     results.append({
    #         "class_id": class_id,
    #         "cropped_image_path": image_path,
    #         "similar_items": similar_items
    #     })


    # return {
    #     "message": "Detection and similarity search completed.",
    #     "annotated_image": f"http://<server_address>:<port>/files/{annotated_clothes}",
    #     "results": results
    # }