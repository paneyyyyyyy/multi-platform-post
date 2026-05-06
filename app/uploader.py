import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # 新增
from bs4 import BeautifulSoup
import time

def fetch_product_info(url):
    options = Options()
    # ✅ 雲端環境最強力穩定參數
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage") # 防止資源限制崩潰
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--remote-debugging-port=9222") # 增加通訊穩定性
    
    # 偽裝一般使用者，避免被旋轉拍賣阻擋
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    # 強制指定剛才安裝的 Chrome 位置
    options.binary_location = "/usr/bin/google-chrome" 

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # 設定頁面載入超時，避免無限等待
        driver.set_page_load_timeout(30)
        
        driver.get(url)
        # 等待標題出現
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ✅ 商品標題
        title_tag = soup.select_one("h1[data-testid='new-listing-details-page-desktop-text-title']")
        title = title_tag.text.strip() if title_tag else "商品名稱無法擷取"

        # ✅ 商品價格
        price_tag = soup.find("h2", string=lambda text: text and "NT$" in text)
        price = price_tag.text.strip() if price_tag else "價格無法擷取"

        # ✅ 圖片擷取
        image_section = soup.select_one("div.asm-fsg")
        if image_section:
            img_tags = image_section.select('img[src*="media.karousell.com/media/photos/products/"]')
            image_urls = list({
                img["src"]
                for img in img_tags if img.get("src")
            })
        else:
            image_urls = []

        # ✅ 商品描述文字
        description_tag = soup.select_one("div#FieldSetField-Container-field_description p")
        description = description_tag.text.strip() if description_tag else "請點商品連結查看詳情"

        # ✅ 商品額外資訊
        brand_tag = soup.find("p", string="品牌")
        brand = brand_tag.find_next("span").text.strip() if brand_tag else ""

        size_tag = soup.find("p", string="尺寸")
        size = size_tag.find_next("span").text.strip() if size_tag else ""

        full_description = f"{description}\n\n尺寸：{size}\n品牌：{brand}"

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
