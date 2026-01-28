"""
Sanggyeonrye Face Test - Image Crawler
For Teachable Machine training data

Usage: python index.py
       python index.py --gender female
       python index.py --gender male --count 100
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os
import ssl

# SSL 인증서 검증 비활성화 (이미지 다운로드 에러 방지)
ssl._create_default_https_context = ssl._create_unverified_context


def create_directory(directory):
    """디렉토리 생성"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"[FOLDER] Created: {directory}")
    except OSError as e:
        print(f"[ERROR] Failed to create folder: {e}")


def crawling_img(name, category, max_count=100):
    """
    Google 이미지 크롤링
    
    Args:
        name: 검색어 (예: "차은우 얼굴")
        category: 저장 폴더명 (예: "프리패스상", "문전박대상")
        max_count: 최대 이미지 수 (기본 100장)
    """
    print(f"\n[START] Crawling: {name} -> {category}")
    
    # Chrome 옵션 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=ko_KR")
    # options.add_argument("--headless")  # 백그라운드 실행 원하면 주석 해제
    
    # WebDriver 자동 관리 (Chrome 버전 자동 매칭)
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # Google 이미지 검색
        driver.get("https://www.google.co.kr/imghp?hl=ko")
        time.sleep(1)
        
        # 검색어 입력
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)
        
        # 스크롤하여 이미지 더 로드
        SCROLL_PAUSE_TIME = 1.5
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        scroll_count = 0
        max_scrolls = 10  # 최대 스크롤 횟수
        
        while scroll_count < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # "결과 더보기" 버튼 클릭 시도
                try:
                    more_btn = driver.find_element(By.CSS_SELECTOR, ".mye4qd")
                    if more_btn.is_displayed():
                        more_btn.click()
                        time.sleep(1)
                except:
                    break
            
            last_height = new_height
            scroll_count += 1
        
        # 이미지 요소 찾기 (2024+ Google Images selectors)
        selectors = ["img.YQ4gaf", "img.rg_i", ".rg_i.Q4LuWd", "[data-src]"]
        imgs = []
        
        for selector in selectors:
            imgs = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(imgs) > 0:
                print(f"[OK] Found {len(imgs)} images with '{selector}'")
                break
        
        if not imgs:
            print("[ERROR] No images found. Google page structure may have changed.")
            return
        
        # 저장 폴더 생성 (상대 경로)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(base_dir, "dataset", category)
        create_directory(save_dir)
        
        # 이미지 다운로드
        count = 0
        for i, img in enumerate(imgs):
            if count >= max_count:
                break
                
            try:
                # 이미지 클릭하여 고화질 버전 열기
                img.click()
                time.sleep(1.5)
                
                # Get image URL (try direct src first, then click for high-res)
                img_url = img.get_attribute("src")
                
                # Skip base64 or google internal images
                if not img_url or img_url.startswith("data:") or "google" in img_url or "gstatic" in img_url:
                    img.click()
                    time.sleep(1.5)
                    
                    # Try high-res selectors
                    hi_res_selectors = [
                        "img.sFlh5c.pT0Scc",
                        "img.sFlh5c",
                        "img.n3VNCb",
                        "img.iPVvYb",
                        "img[jsname='HiaYvf']",
                    ]
                    
                    for sel in hi_res_selectors:
                        try:
                            large_imgs = driver.find_elements(By.CSS_SELECTOR, sel)
                            for large_img in large_imgs:
                                url = large_img.get_attribute("src")
                                if url and url.startswith("http") and "google" not in url and "gstatic" not in url:
                                    img_url = url
                                    break
                            if img_url and img_url.startswith("http") and "google" not in img_url:
                                break
                        except:
                            continue
                
                if not img_url or not img_url.startswith("http") or "google" in img_url:
                    continue
                
                # 이미지 다운로드
                # 검색어에서 파일명에 사용할 수 없는 문자 제거
                safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip()
                safe_name = safe_name.replace(' ', '_')
                filename = f"{safe_name}_{count + 1}.jpg"
                filepath = os.path.join(save_dir, filename)
                
                urllib.request.urlretrieve(img_url, filepath)
                count += 1
                print(f"  [OK] [{count}/{max_count}] {filename}")
                
            except Exception as e:
                # 에러 무시하고 다음 이미지로
                continue
        
        print(f"[DONE] {name} -> {count} images saved")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        
    finally:
        driver.quit()


# ============================================
# 상견례 얼굴상 테스트 - 학습 데이터 수집
# ============================================

# 여자 연예인 리스트
FEMALE_FREEPASS = [
    "박보영 얼굴",
    "박은빈 얼굴",
    "김민주 아이즈원 얼굴",
    "미나 트와이스 얼굴",
    "카즈하 르세라핌 얼굴",
    "효정 오마이걸 얼굴",
]

FEMALE_MOONJEONBAKDAE = [
    "이채영 프로미스나인 얼굴",
    "미미 오마이걸 얼굴",
    "닝닝 에스파 얼굴",
    "채영 트와이스 얼굴",
    "제니 블랙핑크 얼굴",
]

# 남자 연예인 리스트
MALE_FREEPASS = [
    "진 BTS 얼굴",
    "임시완 얼굴",
    "송중기 얼굴",
    "박보검 얼굴",
    "차은우 얼굴",
]

MALE_MOONJEONBAKDAE = [
    "덱스 얼굴",
    "산 에이티즈 얼굴",
    "창균 몬스타엑스 얼굴",
    "연준 투바투 얼굴",
    "뷔 BTS 얼굴",
]


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='상견례 얼굴상 테스트 이미지 크롤러')
    parser.add_argument('--gender', choices=['male', 'female', 'all'], default='all',
                        help='크롤링할 성별 (male/female/all)')
    parser.add_argument('--count', type=int, default=50,
                        help='연예인당 이미지 수 (기본: 50)')
    args = parser.parse_args()
    
    print("=" * 50)
    print("[CRAWLER] Sanggyeonrye Face Test - Image Crawler")
    print("=" * 50)
    
    # 여자 연예인 크롤링
    if args.gender in ['female', 'all']:
        print("\n" + "=" * 50)
        print("[FEMALE] Starting image collection...")
        print("=" * 50)
        
        print("\n[FEMALE FREEPASS]")
        for celeb in FEMALE_FREEPASS:
            crawling_img(celeb, "female_freepass", max_count=args.count)
        
        print("\n[FEMALE MOONJEONBAKDAE]")
        for celeb in FEMALE_MOONJEONBAKDAE:
            crawling_img(celeb, "female_moonjeonbakdae", max_count=args.count)
    
    # 남자 연예인 크롤링
    if args.gender in ['male', 'all']:
        print("\n" + "=" * 50)
        print("[MALE] Starting image collection...")
        print("=" * 50)
        
        print("\n[MALE FREEPASS]")
        for celeb in MALE_FREEPASS:
            crawling_img(celeb, "male_freepass", max_count=args.count)
        
        print("\n[MALE MOONJEONBAKDAE]")
        for celeb in MALE_MOONJEONBAKDAE:
            crawling_img(celeb, "male_moonjeonbakdae", max_count=args.count)
    
    print("\n" + "=" * 50)
    print("[COMPLETE] Crawling finished!")
    print("[FOLDER] Save locations:")
    print("   ./dataset/female_freepass/")
    print("   ./dataset/female_moonjeonbakdae/")
    print("   ./dataset/male_freepass/")
    print("   ./dataset/male_moonjeonbakdae/")
    print("=" * 50)
