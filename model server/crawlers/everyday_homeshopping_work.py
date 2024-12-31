from crawler import HomeShoppingCrawler
from config.config import LIVE_URL, TV_URL, disp_numbers, YOLO_C_MODEL_PATH, YOLO_P_MODEL_PATH, bucket_name
from processors.category_classifier import classify_main_category
from processors.ImageProcessor import process_image, download_image
from processors.vectorize import image_to_vector, load_resnet_model
from processors.detector import Detector
from db.db import DatabaseManager
import time
import cv2
import numpy as np

detector = Detector(YOLO_C_MODEL_PATH, YOLO_P_MODEL_PATH)
model = load_resnet_model()
crawler = HomeShoppingCrawler()

try:

    now = time.localtime()
    ymd = time.strftime('%y%m%d', now)

    # 페이지 로드
    crawler.open_schedule_page(LIVE_URL)

    # 상품 리스트 추출
    product_list = crawler.extract_product_list()
    vec_id = 0

    with DatabaseManager() as db_manager:
        for product in product_list:
            # 상품 정보 추출
            product_info = crawler.extract_product_info(product)

            if product_info and product_info['product_url'] != 'URL 없음':
                # 카테고리 추출
                category = crawler.extract_category(product_info['product_url'])

                # 대표 이미지 및 추가 이미지 URL 생성
                product_image_url, additional_image_urls, start_index = crawler.extract_image_urls(product_info['product_id'], bucket_name, ymd)

                # 카테고리 처리
                categories_split = category.split(' -> ') if category != "카테고리 없음" else []
                main_category = categories_split[0] if len(categories_split) > 0 else "대분류 없음"
                sub_category = categories_split[1] if len(categories_split) > 1 else "중분류 없음"
                detail_category = categories_split[2] if len(categories_split) > 2 else "소분류 없음"

                main_category = classify_main_category(sub_category, detail_category)
                product_info['main_category'] = main_category

                if not main_category:
                    continue

                # PostgreSQL 데이터 삽입
                db_manager.insert_live_product_info(product_info)

                # 메인 이미지 벡터화
                main_image = download_image(product_image_url)
                if main_image:
                    main_image_cv = cv2.cvtColor(np.array(main_image), cv2.COLOR_RGB2BGR)
                    main_image_vector = image_to_vector(main_image_cv, model)
                    main_crop_vector = process_image(main_image_cv, main_category, detector, model)

                # 대표 이미지 삽입 : start_index
                if main_image_vector is not None and main_image_vector.size > 0:
                    vec_id += 1
                    main_s3_url = f"s3://{bucket_name}/{ymd}/{product_info['product_id']}_0.jpg"
                    db_manager.insert_vectors(vec_id, product_info['product_id'], 'live',
                                            main_image_vector, main_s3_url, 0)
                    if main_crop_vector:
                        for vector in main_crop_vector:
                            vec_id += 1
                            db_manager.insert_vectors(vec_id, product_info['product_id'], 'live',
                                            vector, main_s3_url, 0)

                if additional_image_urls:
                    # 추가 이미지 벡터화 및 삽입
                    for i, img_url in enumerate(additional_image_urls, start=start_index):
                        additional_image = download_image(img_url)
                        additional_image_vectors = []
                        additional_s3_url = f"s3://{bucket_name}/{ymd}/{product_info['product_id']}_{i}.jpg"

                        if additional_image:
                            additional_image_cv = cv2.cvtColor(np.array(additional_image), cv2.COLOR_RGB2BGR)
                            additional_image_vectors.append(image_to_vector(additional_image_cv, model))
                            additional_image_vectors.extend(process_image(additional_image_cv, main_category, detector, model))

                            for vector in additional_image_vectors:
                                vec_id += 1
                                db_manager.insert_vectors(vec_id, product_info['product_id'], 'live',
                                                vector, additional_s3_url, i)

finally:
    crawler.close()

crawler = HomeShoppingCrawler()
try:
    for category, disp_list in disp_numbers.items():
        category_id = list(disp_numbers.keys()).index(category)
        for disp_no in disp_list:
            url = f"{TV_URL}{disp_no}"

            crawler.open_tv_page(url)

            # 상품 리스트 추출
            tv_product_list = crawler.extract_tv_product_list()

            with DatabaseManager() as db_manager:
                for product in tv_product_list:
                    # 상품 정보 추출
                    tv_product_info = crawler.extract_tv_product_info(product)

                    if tv_product_info and tv_product_info["product_url"] != 'URL 없음':
                        # 대표 이미지 및 추가 이미지 URL 생성
                        product_image_url, additional_image_urls, start_index = crawler.extract_image_urls(tv_product_info['product_id'], bucket_name, ymd)
                        tv_product_info['main_category'] = category

                        # PostgreSQL 데이터 삽입
                        db_manager.insert_tv_product_info(tv_product_info)

                        # 메인 이미지 벡터화
                        tv_main_image = download_image(product_image_url)
                        if tv_main_image:
                            tv_main_image_cv = cv2.cvtColor(np.array(tv_main_image), cv2.COLOR_RGB2BGR)
                            tv_main_image_vector = image_to_vector(tv_main_image_cv, model)
                            tv_main_crop_vector = process_image(tv_main_image_cv, main_category, detector, model)

                        # 대표 이미지 삽입 : start_index
                        if tv_main_image_vector is not None and tv_main_image_vector.size > 0:
                            vec_id += 1
                            main_s3_url = f"s3://{bucket_name}/{ymd}/{tv_product_info['product_id']}_0.jpg"
                            db_manager.insert_vectors(vec_id, tv_product_info['product_id'], 'outlet', tv_main_image_vector, main_s3_url, 0)
                            if tv_main_crop_vector:
                                for vector in tv_main_crop_vector:
                                    vec_id += 1
                                    db_manager.insert_vectors(vec_id, tv_product_info['product_id'], 'outlet', vector, main_s3_url, 0)

                        if additional_image_urls:
                            # 추가 이미지 벡터화 및 삽입
                            for i, img_url in enumerate(additional_image_urls, start=start_index):
                                additional_image = download_image(img_url)
                                additional_image_vectors = []
                                additional_s3_url = f"s3://{bucket_name}/{ymd}/{tv_product_info['product_id']}_{i}.jpg"

                                if additional_image:
                                    additional_image_cv = cv2.cvtColor(np.array(additional_image), cv2.COLOR_RGB2BGR)
                                    additional_image_vectors.append(image_to_vector(additional_image_cv, model))
                                    additional_image_vectors.extend(process_image(additional_image_cv, main_category, detector, model))

                                    for vector in additional_image_vectors:
                                        vec_id += 1
                                        db_manager.insert_vectors(vec_id, tv_product_info['product_id'], 'outlet', vector, additional_s3_url, i)

finally:
    crawler.close()