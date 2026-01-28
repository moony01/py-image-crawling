# 🖼️ 이미지 크롤러 (Teachable Machine 학습용)

Google 이미지 검색 결과를 크롤링하여 Teachable Machine 학습 데이터를 수집합니다.

## 📦 설치

```bash
pip install -r requirements.txt
```

## 🚀 사용법

### 기본 실행 (상견례 테스트용)

```bash
python index.py
```

실행하면 자동으로:

- `./dataset/프리패스상/` - 호감형 연예인 이미지
- `./dataset/문전박대상/` - 밈으로 유명한 연예인 이미지

### 커스텀 사용

```python
from index import crawling_img

# 단일 검색어 크롤링
crawling_img("검색어", "저장폴더명", max_count=50)

# 예시
crawling_img("차은우 얼굴", "프리패스상", max_count=100)
```

## 📁 결과물 구조

```
py-image-crawling/
├── dataset/
│   ├── 프리패스상/
│   │   ├── 차은우_얼굴_1.jpg
│   │   ├── 차은우_얼굴_2.jpg
│   │   └── ...
│   └── 문전박대상/
│       ├── 이채영_프로미스나인_얼굴_1.jpg
│       └── ...
├── index.py
├── requirements.txt
└── README.md
```

## ⚙️ 설정

### 연예인 리스트 수정

`index.py` 파일의 리스트를 수정하세요:

```python
# 프리패스상
freepass_celebrities = [
    "차은우 얼굴",
    "원빈 얼굴",
    # 추가...
]

# 문전박대상
moonjeonbakdae_celebrities = [
    "이채영 프로미스나인 얼굴",
    # 추가...
]
```

### 이미지 개수 조정

```python
crawling_img(celeb, "프리패스상", max_count=100)  # 100장으로 변경
```

## ⚠️ 주의사항

1. **크롬 브라우저** 필요 (자동으로 WebDriver 다운로드됨)
2. **인터넷 연결** 필요
3. Google 정책에 따라 **셀렉터가 변경**될 수 있음
4. 학습용 목적으로만 사용 권장

## 🔧 문제 해결

### Chrome 버전 에러

```bash
pip install --upgrade webdriver-manager
```

### 이미지가 안 받아지는 경우

- Google 페이지 구조 변경 가능성
- `index.py`의 CSS 셀렉터/XPath 업데이트 필요

## 📝 라이센스

MIT License
