import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np

# ResNet50 모델 초기화
def load_resnet_model():
    model = models.resnet50(pretrained=True)
    model = torch.nn.Sequential(*(list(model.children())[:-1]))  # 마지막 FC 레이어 제거
    model.eval()
    return model

# 이미지 전처리 및 벡터화 함수
def image_to_vector(image, model):
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    try:
        # numpy.ndarray인 경우 PIL.Image로 변환
        if isinstance(image, np.ndarray):
            if len(image.shape) != 3 or image.shape[2] != 3:
                raise ValueError("벡터화에 전달된 이미지가 올바르지 않은 형식입니다 (예: 흑백 이미지).")
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        image_tensor = preprocess(image).unsqueeze(0)
        with torch.no_grad():
            vector = model(image_tensor).squeeze().numpy()
        return vector
    except Exception as e:
        print(f"이미지 벡터화 실패: {e}")
        return None
