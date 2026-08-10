import cv2
import imagehash
from PIL import Image

def analyze_photo(image_path):
    # 1. 초점/흔들림(블러) 수치 측정 (Laplacian Variance)
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # 2. 유사도 판별용 pHash 수치 추출
    pil_image = Image.open(image_path)
    phash_val = imagehash.phash(pil_image)
    
    print(f"[{image_path}]")
    print(f" - 선명도(Focus Score): {blur_score:.2f}")
    print(f" - pHash 수치: {phash_val}")
    print("-" * 40)
    return phash_val

# 준비한 사진 파일명으로 테스트
hash1 = analyze_photo("test1.jpg")
hash2 = analyze_photo("test2.jpg")

# 두 사진 간의 유사도(거리) 계산
hamming_distance = hash1 - hash2
print(f"두 사진의 차이점(Hamming Distance): {hamming_distance}")
if hamming_distance <= 5:
    print("=> 💡 결과: 90% 이상 중복/유사 사진입니다!")
else:
    print("=> 💡 결과: 서로 다른 사진입니다.")