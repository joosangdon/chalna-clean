# 📸 찰나정리 (ChalnaClean)

> **찰나의 순간 중 베스트만 남기는, 가장 안전한 AI 사진 정리 웹 서비스**

---

## 📌 프로젝트 소개
연사 촬영으로 쌓인 유사 사진, 초점이 나가 흔들린 사진, 저화질 복사본 사진을 AI 알고리즘으로 자동 분류하여 사용자가 쉽게 정제할 수 있도록 돕는 웹 서비스입니다.

## 🛡️ 핵심 보안 및 기능 방향
- **Privacy-First:** 사용자 사진 데이터를 서버 DB에 저장하지 않고, 메모리 기반 처리 후 즉시 파기하여 개인정보 유출을 방지합니다.
- **화질 감지:** OpenCV(Laplacian Variance) 기반의 블러/흔들림 감지
- **중복 그룹핑:** Perceptual Hashing (pHash) 기반 유사도 측정 및 90~95% 이상 중복 사진 추천 삭제
- **시큐어 코딩:** 파일 업로드 취약점 방어 (Magic Byte 검증, 파일명 UUID화 등)

## 🛠 Tech Stack (예정)
- **Frontend:** Next.js, TypeScript, Tailwind CSS
- **Backend:** Python (FastAPI), OpenCV, ImageHash
