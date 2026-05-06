# 🛍️ Multi-Platform Poster 多平台商品貼文自動化系統

這是一個為電商商家量身打造的自動化工具。只需輸入商品網址，系統即可自動擷取資訊、下載圖片，並利用 AI 生成吸引人的行銷文案，大幅簡化跨平台商品上架的繁瑣流程。

---

## 🚀 功能特色

*   **🔗 商品網址自動解析**：支援旋轉拍賣 (Carousell)、蝦皮 (Shopee)、MOMO 等平台。
*   **🖼 圖片自動處理**：自動擷取商品原圖，確保內容呈現的高品質。
*   **✍️ AI 自動文案生成**：整合 LangChain 與 Ollama (Gemma:2b)，支援多種語氣切換（簡潔、可愛、專業）。
*   **✅ 雲端環境相容**：專為 GitHub Codespaces 優化，無需在本地電腦安裝環境即可隨時開發與測試。

---

## 🧱 專案架構

本系統採用模組化設計，確保資料擷取與內容生成的穩定性：

*   **前端介面 (`Streamlit`)**: 提供直觀的網頁操作控台，支援即時文案編輯與圖片預覽。
*   **資料擷取模組 (`Selenium` + `BeautifulSoup4`)**: 負責處理動態網頁解析，內建 Linux 無頭模式 (Headless) 以適應伺服器環境。
*   **文案生成引擎 (`Ollama` + `LangChain`)**: 利用地端大型語言模型確保文案生成的隱私與低延遲。
*   **自動化發佈模組 (開發中)**: 模擬 Web 操作流程，預計實現跨平台內容同步。

---

## 📅 開發路線圖 (Development Roadmap)

目前系統已完成核心的資料擷取與 AI 文案生成功能。針對社群平台自動發布功能，說明如下：

*   **[已完成]** 旋轉拍賣 (Carousell) 商品資訊擷取與圖片自動化下載。
*   **[已完成]** 結合地端 LLM 之自動化多語氣行銷文案生成。
*   **[規劃中] Facebook / Instagram 自動發文模組**：
    *   由於 Facebook 與 Instagram 官方 API 之權限申請流程較為嚴謹，且為確保模擬自動化發布行為之安全性與帳號權限穩定性，**目前自動發佈至 FB/IG 之模組仍在開發與調校階段**。
    *   短期計畫將優先支援「文案一鍵複製」與「圖片打包下載」功能，以輔助人工快速發文；中長期將持續優化對接 API 之自動化流程。

---

## 🛠 開啟與執行方式 (GitHub Codespaces)

### 1. 安裝系統依賴項目
在終端機 (Terminal) 安裝 Google Chrome 與執行所需的 Linux 函式庫：
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt-get update
sudo apt-get install -y ./google-chrome-stable_current_amd64.deb libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2t64
```

### 2. 初始化 Python 環境
```bash
pip install -r requirements.txt
pip install webdriver-manager langchain-community langchain-core
```

### 3. 配置 AI 引擎 (Ollama)

```bash
# 安裝 Ollama
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

# 啟動服務 (背景執行)
ollama serve > ollama.log 2>&1 &

# 下載預設模型 (Gemma:2b)
ollama pull gemma:2b
```

### 4. 啟動系統

```bash
python -m streamlit run app/main.py
```
⚠️ 注意事項
* **AI 模型啟動: 若 Codespaces 重啟，請重新執行 ollama serve & 以確保 API 服務正常。
* **防爬蟲機制: 系統會模擬 User-Agent 以降低被電商平台阻擋之機率。

### 📄 授權說明
本專案僅供學術研究與電商輔助測試使用，請遵守各平台的使用者協議與著作權法規。
