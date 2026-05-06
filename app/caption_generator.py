# caption_generator.py

from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLanguageModel
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

llm: BaseLanguageModel = Ollama(model="gemma:2b")

template = """
你是一位擅長撰寫社群行銷文案的寫手，請根據以下資訊產出一段貼文文案，語氣為「{tone}」：

商品名稱：{title}
價格：{price}
描述：{description}

請用繁體中文撰寫，貼文長度約 30～60 字，吸引人、自然、真實。
"""

prompt = PromptTemplate(
    input_variables=["title", "price", "description", "tone"],
    template=template
)

def generate_caption(title, price, description, selected_tones):
    chain = LLMChain(llm=llm, prompt=prompt)
    results = {}
    for tone in selected_tones:
        try:
            response = chain.run({
                "title": title,
                "price": price,
                "description": description,
                "tone": tone
            })
            results[tone] = response.strip()
        except Exception as e:
            results[tone] = f"[產生失敗：{str(e)}]"
    return results
