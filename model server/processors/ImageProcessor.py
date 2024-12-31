import requests
import cv2
from PIL import Image
import numpy as np
from processors.vectorize import image_to_vector
from io import BytesIO

def process_image(image, expected_category, detector, resnet_model):
    """
    이미지에서 사람 탐지 후 조건에 따라 의류를 탐지 및 벡터화합니다.
    :param image_url: 이미지 URL
    :param expected_category: 기대하는 의류 카테고리 (top, bottom, outer, onepiece)
    :param detector: Detector 클래스 인스턴스
    :param resnet_model: ResNet 모델 인스턴스
    :return: 이미지 벡터 리스트
    """

    # 클래스 ID와 카테고리 매핑
    CATEGORY_MAPPING = {
        0: 'top',
        1: 'bottom',
        2: 'outer',
        3: 'onepiece'
    }
    vectors = []

    try:
        if isinstance(image, np.ndarray):
            if len(image.shape) != 3 or image.shape[2] != 3:
                raise ValueError("이미지가 올바르지 않은 형식입니다 (예: 흑백 이미지).")
        else:
            # PIL.Image -> numpy.ndarray 변환
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # 사람 탐지 수행
        person_detections = detector.detect(image, model_filter=0, class_filter=0)

        if len(person_detections) == 0:
            # 1. 사람 0명: 원본 이미지에서 의류 탐지
            print("사람 없음. 원본 이미지에서 의류 탐지.")
            clothes_detections = detector.detect(image, model_filter=1)
            vectors.extend(
                _process_clothes_detections(image, clothes_detections, CATEGORY_MAPPING, expected_category, resnet_model)
            )

        elif len(person_detections) == 1:
            # 2. 사람 1명: 사람을 크롭하고 의류 탐지
            print("사람 1명. 사람 크롭 후 의류 탐지.")
            x1, y1, x2, y2 = person_detections[0][:4]
            cropped_person = image[y1:y2, x1:x2]
            clothes_detections = detector.detect(cropped_person, model_filter=1)
            vectors.extend(
                _process_clothes_detections(cropped_person, clothes_detections, CATEGORY_MAPPING, expected_category, resnet_model)
            )

        else:
            # 3. 사람 2명 이상: 원본 이미지 벡터화
            print("사람 2명 이상. 벡터화 생략.")
            return []

    except Exception as e:
        print(f"이미지 처리 중 오류 발생: {e}")

    return vectors


def _process_clothes_detections(image, clothes_detections, category_mapping, expected_category, resnet_model):
    """
    의류 탐지 결과에서 기대하는 카테고리와 일치하는 의류만 벡터화합니다.
    :param image: 원본 이미지
    :param clothes_detections: 의류 탐지 결과
    :param category_mapping: 클래스 ID와 카테고리 매핑
    :param expected_category: 기대하는 의류 카테고리
    :param resnet_model: ResNet 모델 인스턴스
    :return: 벡터 리스트
    """
    vectors = []

    for (x1, y1, x2, y2, class_id) in clothes_detections:
        detected_category = category_mapping.get(class_id, None)

        # 기대한 카테고리와 일치하는 경우만 처리
        if detected_category == expected_category:
            cropped_image = image[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
            if cropped_image.size > 0 and cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                try:
                    vector = image_to_vector(cropped_image, resnet_model)
                    if vector is not None:
                        vectors.append(vector)
                except Exception as ve:
                    print(f"크롭된 이미지 벡터화 실패: {ve}")
    return vectors

def download_image(image_url):
    """
    이미지 URL을 다운로드하여 PIL.Image 객체 반환
    """
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"이미지 다운로드 실패: {image_url}")
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")
        return None