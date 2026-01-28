"""
상견례 얼굴상 테스트 - 이미지 크롤러
Teachable Machine 학습용 이미지 수집

사용법: python index.py
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
            print(f"📁 폴더 생성: {directory}")
    except OSError as e:
        print(f"❌ 폴더 생성 실패: {e}")


def crawling_img(name, category, max_count=100):
    """
    Google 이미지 크롤링
    
    Args:
        name: 검색어 (예: "차은우 얼굴")
        category: 저장 폴더명 (예: "프리패스상", "문전박대상")
        max_count: 최대 이미지 수 (기본 100장)
    """
    print(f"\n🔍 크롤링 시작: {name} → {category}")
    
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
        
        # 이미지 요소 찾기 (여러 셀렉터 시도)
        selectors = [".rg_i.Q4LuWd", "img.rg_i", "[data-src]"]
        imgs = []
        
        for selector in selectors:
            imgs = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(imgs) > 0:
                print(f"✅ 셀렉터 '{selector}'로 {len(imgs)}개 이미지 발견")
                break
        
        if not imgs:
            print("❌ 이미지를 찾을 수 없습니다. Google 페이지 구조가 변경되었을 수 있습니다.")
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
                
                # 고화질 이미지 URL 추출 (여러 XPath 시도)
                xpaths = [
                    '//img[contains(@class, "sFlh5c")]',
                    '//img[contains(@class, "n3VNCb")]',
                    '//img[contains(@class, "iPVvYb")]',
                    '//*[@id="Sva75c"]//img[@src and @alt]'
                ]
                
                img_url = None
                for xpath in xpaths:
                    try:
                        large_img = driver.find_element(By.XPATH, xpath)
                        img_url = large_img.get_attribute("src")
                        if img_url and img_url.startswith("http") and "google" not in img_url:
                            break
                    except:
                        continue
                
                if not img_url or not img_url.startswith("http"):
                    continue
                
                # 이미지 다운로드
                # 검색어에서 파일명에 사용할 수 없는 문자 제거
                safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).strip()
                safe_name = safe_name.replace(' ', '_')
                filename = f"{safe_name}_{count + 1}.jpg"
                filepath = os.path.join(save_dir, filename)
                
                urllib.request.urlretrieve(img_url, filepath)
                count += 1
                print(f"  📥 [{count}/{max_count}] {filename}")
                
            except Exception as e:
                # 에러 무시하고 다음 이미지로
                continue
        
        print(f"✅ 완료: {name} → {count}장 저장됨")
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        
    finally:
        driver.quit()


# ============================================
# 상견례 얼굴상 테스트 - 학습 데이터 수집
# ============================================

if __name__ == "__main__":
    
    # 프리패스상 (호감형) 연예인 리스트
    freepass_celebrities = [
        "차은우 얼굴",
        "원빈 얼굴",
        "송중기 얼굴",
        "박보검 얼굴",
        "송혜교 얼굴",
        "수지 얼굴",
        "아이유 얼굴",
        "김태희 얼굴",
    ]
    
    # 문전박대상 (밈으로 유명한) 연예인 리스트
    # 주의: 실제 비호감이 아니라 밈으로 유명해진 케이스들
    moonjeonbakdae_celebrities = [
        "이채영 프로미스나인 얼굴",
        # 추가 필요시 여기에 추가
    ]
    
    print("=" * 50)
    print("🎭 상견례 얼굴상 테스트 - 이미지 크롤러")
    print("=" * 50)
    
    # 프리패스상 이미지 수집
    print("\n👍 [프리패스상] 이미지 수집 시작...")
    for celeb in freepass_celebrities:
        crawling_img(celeb, "프리패스상", max_count=50)
    
    # 문전박대상 이미지 수집
    print("\n👎 [문전박대상] 이미지 수집 시작...")
    for celeb in moonjeonbakdae_celebrities:
        crawling_img(celeb, "문전박대상", max_count=50)
    
    print("\n" + "=" * 50)
    print("✅ 크롤링 완료!")
    print(f"📁 저장 위치: ./dataset/프리패스상/, ./dataset/문전박대상/")
    print("=" * 50)
