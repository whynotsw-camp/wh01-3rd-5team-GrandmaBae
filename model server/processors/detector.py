from ultralytics import YOLO
import cv2
import os


class Detector:
    def __init__(self, model_path, person_model_path):
        self.clothes_model = YOLO(model_path)       # 의류 탐지 모델
        self.person_model = YOLO(person_model_path)  # 사람 탐지 모델

    def detect(self, image_path, model_filter=0, class_filter=None):
        """
        이미지에서 객체를 탐지합니다.
        :param image_path: 이미지 경로
        :param model_filter: 0이면 사람 모델, 1이면 의류 모델
        :param class_filter: 특정 클래스 ID만 필터링 (None이면 전체 탐지)
        :return: 탐지된 객체 리스트 [(x1, y1, x2, y2, class_id)]
        """
        model = self.person_model if model_filter == 0 else self.clothes_model
        results = model(image_path)[0]
        detections = []

        for box, cls in zip(results.boxes.xyxy, results.boxes.cls):
            class_id = int(cls)
            if class_filter is None or class_id == class_filter:
                x1, y1, x2, y2 = map(int, box)
                detections.append((x1, y1, x2, y2, class_id))
        return detections

    @staticmethod
    def crop_image(image, box, output_path):
        """
        이미지에서 특정 영역을 크롭합니다.
        :param image: 원본 이미지
        :param box: (x1, y1, x2, y2) 좌표
        :param output_path: 크롭된 이미지 저장 경로
        """
        x1, y1, x2, y2 = box
        height, width = image.shape[:2]

        # 경계 검증: 이미지 크기 내로 좌표 제한
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)

        cropped_image = image[y1:y2, x1:x2]
        if cropped_image.size == 0:  # 크롭된 이미지가 비어있을 경우 처리
            print(f"Warning: Invalid crop coordinates {box}. Skipping.")
            return None
        cv2.imwrite(output_path, cropped_image)
        return output_path

    def detect_person(self, image_path, output_dir):
        """
        사람을 탐지하고 바운딩 박스를 그립니다.
        :return: (주석이 추가된 이미지 경로, 사람 바운딩 박스 리스트)
        """
        results = self.person_model(image_path)[0]
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")

        person_boxes = []
        for idx, (box, cls) in enumerate(zip(results.boxes.xyxy, results.boxes.cls)):
            if int(cls) == 0:  # COCO 기준 사람 클래스
                x1, y1, x2, y2 = map(int, box)
                person_boxes.append((x1, y1, x2, y2))
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(image, f"Person {idx + 1}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        output_path = os.path.join(output_dir, "annotated_person.jpg")
        cv2.imwrite(output_path, image)
        return output_path, person_boxes

    def detect_clothes(self, image_path, output_dir):
        """
        의류를 탐지하고 각 객체를 크롭합니다.
        :return: (크롭된 의류 이미지 리스트, 주석이 추가된 이미지 경로)
        """
        results = self.clothes_model(image_path)[0]
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")

        cropped_images = []
        for i, (box, cls) in enumerate(zip(results.boxes.xyxy, results.boxes.cls)):
            x1, y1, x2, y2 = map(int, box)
            class_id = int(cls)

            # 크롭된 이미지 저장
            cropped_path = os.path.join(output_dir, f"class_{class_id}_object_{i}.jpg")
            cropped_result = self.crop_image(image, (x1, y1, x2, y2), cropped_path)
            if cropped_result:
                cropped_images.append({"class_id": class_id, "path": cropped_result})

        return cropped_images
