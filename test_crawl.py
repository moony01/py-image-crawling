# -*- coding: utf-8 -*-
"""
Test script - crawl 5 images only
Updated selectors for 2024+ Google Images
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

ssl._create_default_https_context = ssl._create_unverified_context

def test_crawl(name, max_count=5):
    print(f"\n[START] Crawling: {name}")
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=ko_KR")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        # Go to Google Images
        driver.get("https://www.google.co.kr/imghp?hl=ko")
        time.sleep(2)
        
        # Search
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Scroll to load more images
        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(2)
        
        # Try multiple selectors (2024+ Google Images)
        selectors_to_try = [
            "img.YQ4gaf",           # New Google selector
            "img.rg_i",             # Old selector
            "div[data-id] img",     # Data-id container
            "img[data-src]",        # With data-src
            "img.Q4LuWd",           # Old class
            "div.eA0Zlc img",       # Image container
        ]
        
        imgs = []
        used_selector = None
        
        for selector in selectors_to_try:
            try:
                imgs = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(imgs) > 0:
                    used_selector = selector
                    print(f"[OK] Found {len(imgs)} images with selector: {selector}")
                    break
            except:
                continue
        
        if not imgs:
            print("[ERROR] No images found with any selector")
            print("[DEBUG] Trying to find any img tags...")
            all_imgs = driver.find_elements(By.TAG_NAME, "img")
            print(f"[DEBUG] Total img tags on page: {len(all_imgs)}")
            
            # Filter large images (likely result images)
            for img in all_imgs:
                try:
                    width = img.get_attribute("width")
                    height = img.get_attribute("height")
                    if width and height:
                        if int(width) > 100 and int(height) > 100:
                            imgs.append(img)
                except:
                    pass
            
            if imgs:
                print(f"[OK] Found {len(imgs)} large images by size filtering")
            else:
                return
        
        # Create test folder
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(base_dir, "dataset", "test")
        os.makedirs(save_dir, exist_ok=True)
        print(f"[INFO] Save to: {save_dir}")
        
        count = 0
        for i, img in enumerate(imgs):
            if count >= max_count:
                break
            
            try:
                # Get image source directly first (thumbnail)
                img_url = img.get_attribute("src")
                
                # Skip base64 or small images
                if not img_url or img_url.startswith("data:") or "google" in img_url:
                    # Try clicking for high-res
                    img.click()
                    time.sleep(2)
                    
                    # Find high-res image
                    hi_res_selectors = [
                        "img.sFlh5c.pT0Scc",
                        "img.sFlh5c",
                        "img.n3VNCb",
                        "img.iPVvYb",
                        "img[jsname='HiaYvf']",
                        "img[jsname='kn3ccd']",
                    ]
                    
                    for sel in hi_res_selectors:
                        try:
                            large_imgs = driver.find_elements(By.CSS_SELECTOR, sel)
                            for large_img in large_imgs:
                                url = large_img.get_attribute("src")
                                if url and url.startswith("http") and "google" not in url and "gstatic" not in url:
                                    img_url = url
                                    break
                            if img_url and img_url.startswith("http"):
                                break
                        except:
                            continue
                
                if not img_url or not img_url.startswith("http"):
                    print(f"  [SKIP] No valid URL for image {i}")
                    continue
                
                # Download
                filename = f"test_{count + 1}.jpg"
                filepath = os.path.join(save_dir, filename)
                
                # Add headers to avoid 403
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                
                urllib.request.urlretrieve(img_url, filepath)
                count += 1
                print(f"  [OK] Downloaded: {filename}")
                
            except Exception as e:
                print(f"  [ERROR] Image {i}: {str(e)[:50]}")
                continue
        
        print(f"\n[DONE] Total {count} images saved to {save_dir}")
        
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_crawl("cha eunwoo face", max_count=5)
