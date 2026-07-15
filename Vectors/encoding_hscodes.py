import os

import arabic_reshaper
from bidi.algorithm import get_display
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def rtl(text: str) -> str:
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

texts = [
    "هوش مصنوعی یکی از شاخه‌های علوم کامپیوتر است.",
    "یادگیری ماشین زیرمجموعه‌ای از هوش مصنوعی است.",
    "امروز هوا آفتابی است.",
]

vectors = embeddings.embed_documents(texts)

print(rtl(f"تعداد بردارها: {len(vectors)}"))
print(rtl(f"طول هر بردار: {len(vectors[0])}"))
print(vectors[0][:10])