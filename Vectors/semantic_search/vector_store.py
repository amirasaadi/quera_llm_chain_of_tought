import hashlib
from collections.abc import Sequence

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from semantic_search.config import Settings


class SemanticSearchService:
    def __init__(self, settings: Settings) -> None:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )

        self._vector_store = Chroma(
            collection_name=settings.collection_name,
            embedding_function=embeddings,
            persist_directory=str(settings.chroma_directory),
        )

    @staticmethod
    def _create_document_id(text: str) -> str:
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()

    def sync_documents(
        self,
        texts: Sequence[str],
    ) -> None:
        """
        متن‌های Chroma را با لیست فعلی هماهنگ می‌کند.

        متن‌های جدید اضافه می‌شوند.
        متن‌های حذف‌شده پاک می‌شوند.
        متن‌های قبلی دوباره embedding نمی‌شوند.
        """

        desired_documents = {
            self._create_document_id(text): text
            for text in texts
        }

        stored_data = self._vector_store.get()

        existing_ids = set(
            stored_data.get("ids", [])
        )

        desired_ids = set(
            desired_documents.keys()
        )

        removed_ids = existing_ids - desired_ids

        if removed_ids:
            self._vector_store.delete(
                ids=list(removed_ids)
            )

        new_ids = desired_ids - existing_ids

        if not new_ids:
            return

        sorted_new_ids = sorted(new_ids)

        new_texts = [
            desired_documents[document_id]
            for document_id in sorted_new_ids
        ]

        self._vector_store.add_texts(
            texts=new_texts,
            ids=sorted_new_ids,
            metadatas=[
                {
                    "source": "educational_texts",
                    "document_id": document_id,
                }
                for document_id in sorted_new_ids
            ],
        )

    def search(
        self,
        query: str,
        k: int = 1,
    ) -> list[Document]:
        clean_query = query.strip()

        if not clean_query:
            return []

        return self._vector_store.similarity_search(
            query=clean_query,
            k=k,
        )