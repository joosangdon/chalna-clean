# app/services/image_service.py

import cv2
import os
import numpy as np
import imagehash
from PIL import Image
import io
from app.core.config import settings
from fastapi import HTTPException, status

class ImageService:
    @staticmethod
    def analyze_image(contents: bytes, filename: str = "") -> dict:
        """단일 이미지 분석 (선명도 및 pHash 계산)"""
        # 1. OpenCV 이미지 변환
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 2. 선명도 계산 (Laplacian Variance)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        
        # 3. pHash 계산
        pil_image = Image.open(io.BytesIO(contents))
        phash_obj = imagehash.phash(pil_image)
        
        return {
            "filename": filename,
            "focus_score": round(blur_score, 2),
            "phash": str(phash_obj),
            "_phash_obj": phash_obj,  # 그룹핑 연산용 내부 객체
            "is_blurry": blur_score < settings.BLUR_THRESHOLD
        }

    @classmethod
    def group_photos(cls, files_data: list[tuple[str, bytes]]) -> dict:
        """
        여러 장의 사진 바이너리를 받아 유사한 사진끼리 그룹핑하고 Best 샷을 선별
        files_data: [(파일명, 바이너리), ...]
        """
        # 1. 각 이미지 개별 분석
        analyzed_list = []
        for filename, contents in files_data:
            info = cls.analyze_image(contents, filename)
            analyzed_list.append(info)

        # 2. 유사도 기반 그룹핑 알고리즘 (Hamming Distance <= settings.SIMILARITY_DISTANCE)
        groups = []
        visited = set()

        for i, item in enumerate(analyzed_list):
            if i in visited:
                continue

            current_group = [item]
            visited.add(i)

            for j in range(i + 1, len(analyzed_list)):
                if j in visited:
                    continue

                target = analyzed_list[j]
                # 두 이미지의 pHash 간 Hamming Distance 계산
                distance = item["_phash_obj"] - target["_phash_obj"]

                if distance <= settings.SIMILARITY_DISTANCE:
                    current_group.append(target)
                    visited.add(j)

            groups.append(current_group)

        # 3. 결과 정리 및 Best Photo 선정
        result_groups = []
        for group in groups:
            # 그룹 내에서 선명도(focus_score)가 가장 높은 사진 선별
            best = max(group, key=lambda x: x["focus_score"])
            
            # API 응답에서 내부 연산 객체(_phash_obj) 제거
            clean_members = []
            for m in group:
                member_copy = {k: v for k, v in m.items() if k != "_phash_obj"}
                clean_members.append(member_copy)

            result_groups.append({
                "group_size": len(clean_members),
                "best_photo": best["filename"],
                "photos": clean_members
            })

        return {
            "total_photos": len(files_data),
            "total_groups": len(result_groups),
            "groups": result_groups
        }
    @staticmethod
    def validate_image_file(filename: str, content_type: str, file_bytes: bytes) -> None:
        """업로드된 파일의 크기, 확장자, MIME 타입 및 손상 여부를 검증합니다."""
        # 1. 파일 크기 검증 (0바이트 및 최대 용량 초과 방어)
        file_size = len(file_bytes)
        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"빈 파일입니다: {filename}"
            )
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"파일 크기 초과 (최대 10MB): {filename} ({file_size / (1024*1024):.2f}MB)"
            )

        # 2. 파일 확장자 검증
        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"지원하지 않는 확장자입니다: {ext} (지원: {', '.join(settings.ALLOWED_EXTENSIONS)})"
            )

        # 3. MIME 타입 검증
        if content_type not in settings.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"유효하지 않은 미디어 타입입니다: {content_type}"
            )