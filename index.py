from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
import os


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def crawling_img(name):
    # driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element(By.NAME, "q")
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    #
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")  # 브라우저의 높이를 자바스크립트로 찾음
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤을 내림
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
            except:
                break
        last_height = new_height

    imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    dir = ".\idols" + "\\" + name

    createDirectory(dir) #폴더 생성
    count = 1
    for img in imgs:
        try:
            img.click()
            time.sleep(2)
            imgUrl = driver.find_element(
                By.XPATH,
                '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div[1]/div/div[3]/div/a/img').get_attribute(
                "src") # 크게 뜬 이미지 선택하여 "src" 속성을 받아옴
            path = "C:\\github-repository\\py-image-crawling\\idols\\" + name + "\\"
            urllib.request.urlretrieve(imgUrl, path + name + str(count) + ".jpg")
            count = count + 1
            if count >= 101:
                break
        except:
            pass
    driver.close()
idols = ["빅뱅 지드래곤 얼굴사진","빅뱅 태양 얼굴사진","빅뱅 대성 얼굴사진","위너 송민호 얼굴사진","위너 강승윤 얼굴사진","아이콘 비아이 얼굴사진","아이콘 바비 얼굴사진"]

for idol in idols:
    crawling_img(idol)

# 프로그램 실행 명령프롬프트: python index.py