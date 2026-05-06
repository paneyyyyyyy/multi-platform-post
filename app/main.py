# app/main.py

import streamlit as st
import datetime
from uploader import fetch_product_info
from caption_generator import generate_caption

# ✅ 頁面設定
st.set_page_config(page_title="Multi-Platform Poster", layout="centered")

# ✅ 初始化 session_state
if "product_data" not in st.session_state:
    st.session_state.product_data = None

if "generated_caption" not in st.session_state:
    st.session_state.generated_caption = None

if "cached_url" not in st.session_state:
    st.session_state.cached_url = None

# ✅ UI
st.title("🛍️ 旋轉多平台貼文系統")
st.markdown("請輸入旋轉商品網址，系統將自動擷取商品資訊與圖片。")

product_url = st.text_input("🔗 商品網址", placeholder="請貼上旋轉商品頁連結")

# ✅ 當輸入網址變動時，重新擷取資料
if product_url and (st.session_state.cached_url != product_url):
    with st.spinner("🔍 正在擷取商品資訊..."):
        data = fetch_product_info(product_url)
        st.session_state.product_data = data
        st.session_state.cached_url = product_url
        st.session_state.generated_caption = None  # 清除舊文案

# ✅ 顯示擷取結果
data = st.session_state.product_data

if data:
    if "error" in data:
        st.error(data["error"])
    else:
        title = data.get("title", "無法擷取")
        price = data.get("price", "無法擷取")
        description = data.get("description", "無法擷取")
        image_urls = data.get("image_urls", [])


        # ✅ 使用者選擇要使用的圖片
        selected_images = []

        if image_urls:
            st.markdown("📸 **請選擇要使用的圖片（可多選）**")
            # 圖片兩兩一列
            for i in range(0, len(image_urls), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(image_urls):
                        with cols[j]:
                            img_url = image_urls[i + j]
                            if st.checkbox("", key=f"img_{i+j}"):
                                selected_images.append(img_url)
                            st.image(img_url, width=250)

            if not selected_images:
                st.warning("⚠️ 尚未選擇圖片，文案生成後不會附上圖片。")
        else:
            st.warning("（尚未擷取到商品圖片）")
                
        # ✅ 顯示資訊
        st.markdown(f"📌 **商品名稱：** {title}")
        st.markdown(f"💰 **價格：** {price}")
        st.markdown(f"📝 **描述：** {description}")

        # ✅ 文案生成區塊
        st.markdown("----")
        st.subheader("✍️ 自動生成文案")

        available_tones = ["活潑", "簡潔", "專業", "可愛"]
        selected_tones = st.multiselect("請選擇要產生的語氣風格", available_tones)

        if st.button("產生文案"):
            with st.spinner("正在使用本地模型生成文案..."):
                captions = generate_caption(title, price, description, selected_tones)
                st.session_state.generated_caption = captions

        if st.session_state.generated_caption:
            st.markdown("### 📋 文案結果（可編輯）")
            for tone, text in st.session_state.generated_caption.items():
                st.text_area(f"🎨 {tone}風格文案：", value=text, height=250)


        # ✅ 發佈設定區塊
        st.markdown("----")
        st.subheader("📤 發佈設定")
        platforms = st.multiselect("請選擇要發佈的平台", ["Facebook", "Instagram", "旋轉拍賣"])
        time_input = st.time_input("預約發文時間", value=datetime.time(14, 0))

        if st.button("📬 發佈貼文"):
            st.success("✅ 模擬發文成功！")
