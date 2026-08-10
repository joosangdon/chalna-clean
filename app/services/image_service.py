# app/services/image_service.py

import cv2
import numpy as np
import imagehash
from PIL import Image
import io
from app.core.config import settings

class ImageService:
    @staticmethod
    def analyze_image(contents: bytes) -> dict:
        """
        이미지 바이너리(bytes)를 전달받아 In-Memory 상에서 OpenCV 선명도 및 pHash를 계산합니다.
        """
        # 1. OpenCV 이미지 변환
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 2. 선명도(Focus Score) 계산
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        
        # 3. pHash 계산
        pil_image = Image.open(io.BytesIO(contents))
        phash_val = str(imagehash.phash(pil_image))
        
        # 4. 결과 반환
        return {
            "focus_score": round(blur_score, 2),
            "phash": phash_val,
            "is_blurry": blur_score < settings.BLUR_THRESHOLD
        }