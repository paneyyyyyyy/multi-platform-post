import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def fetch_product_info(url):
    # ✅ 瀏覽器設定
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # ✅ chromedriver 路徑設定
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chromedriver_path = os.path.join(base_dir, "chromedriver.exe")
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1[data-testid='new-listing-details-page-desktop-text-title']"))
        )
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ✅ 商品標題
        title_tag = soup.select_one("h1[data-testid='new-listing-details-page-desktop-text-title']")
        title = title_tag.text.strip() if title_tag else "商品名稱無法擷取"

        # ✅ 商品價格
        price_tag = soup.find("h2", string=lambda text: text and "NT$" in text)

        price = price_tag.text.strip() if price_tag else "價格無法擷取"

        # ✅ 圖片擷取：穩定版本，不依賴 class
        image_section = soup.select_one("div.asm-fsg")  # 外層容器
        img_tags = image_section.select('img[src*="media.karousell.com/media/photos/products/"]')
        image_urls = list({
            img["src"]
            for img in img_tags if img.get("src")
        }) #[:3]


        # ✅ 商品描述文字（詳細說明）
        description_tag = soup.select_one("div#FieldSetField-Container-field_description p")
        description = description_tag.text.strip() if description_tag else "請點商品連結查看詳情"

        # ✅ 商品額外資訊：品牌、尺寸
        brand_tag = soup.find("p", string="品牌")
        brand = brand_tag.find_next("span").text.strip() if brand_tag else ""

        size_tag = soup.find("p", string="尺寸")
        size = size_tag.find_next("span").text.strip() if size_tag else ""

        # ✅ 組合商品描述
        full_description = f"{description}\n\n尺寸：{size}\n品牌：{brand}" if description else "請點商品連結查看詳情"

        return {
            "title": title,
            "price": price,
            "description": full_description,
            "image_urls": image_urls
        }

    except Exception as e:
        return {"error": f"擷取錯誤：{str(e)}"}
    finally:
        driver.quit()
