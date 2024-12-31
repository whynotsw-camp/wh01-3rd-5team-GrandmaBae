from ultralytics import YOLO
import cv2
import os

# COCO 모델 로드 (자동 다운로드)
coco_model = YOLO("yolov8s.pt")

def detect_person(image_path):
    results = coco_model(image_path)
    detections = results[0]
    image = cv2.imread(image_path)

    PERSON_CLASS_ID = 0
    person_boxes = []
    person_count = 0

    for box, cls in zip(detections.boxes.xyxy, detections.boxes.cls):
        if int(cls) == PERSON_CLASS_ID:
            person_count += 1
            x1, y1, x2, y2 = map(int, box)
            person_boxes.append((person_count, (x1, y1, x2, y2)))
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, str(person_count), (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return image, person_boxes

def crop_person(image_path, box, output_path):
    image = cv2.imread(image_path)
    x1, y1, x2, y2 = box
    cropped_image = image[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped_image)
