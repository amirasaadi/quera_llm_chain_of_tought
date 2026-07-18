import streamlit as st

from semantic_search.config import load_settings
from semantic_search.documents import TEXTS
from semantic_search.ui import (
    configure_page,
    render_documents,
    render_search,
)
from semantic_search.vector_store import SemanticSearchService


@st.cache_resource
def get_search_service(
    texts: tuple[str, ...],
) -> SemanticSearchService:
    settings = load_settings()

    service = SemanticSearchService(
        settings=settings
    )

    service.sync_documents(
        texts=texts
    )

    return service


def main() -> None:
    configure_page()

    st.title("جست‌وجوی معنایی متن‌ها")

    try:
        search_service = get_search_service(TEXTS)

    except Exception as error:
        st.error(
            "اتصال به Gemini یا Chroma ناموفق بود."
        )
        st.code(str(error))
        st.stop()

    texts_column, search_column = st.columns(
        [1, 1],
        gap="large",
    )

    with texts_column:
        render_documents(TEXTS)

    with search_column:
        render_search(search_service)


if __name__ == "__main__":
    main()