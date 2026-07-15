from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

vector_db = Chroma.from_texts(
    texts=["متن ۱", "متن ۲", "متن ۱۰۰۰..."], 
    embedding=embeddings,
    collection_name="my_course_collection"
)

results = vector_db.similarity_search("سوال کاربر", k=2)