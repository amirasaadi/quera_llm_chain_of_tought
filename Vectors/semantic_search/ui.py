from collections.abc import Sequence

import streamlit as st

from semantic_search.vector_store import SemanticSearchService


def configure_page() -> None:
    st.set_page_config(
        page_title="جست‌وجوی معنایی",
        layout="wide",
    )

    st.markdown(
        """
        <style>
            html,
            body,
            [data-testid="stAppViewContainer"] {
                direction: rtl;
                text-align: right;
            }

            textarea,
            input {
                direction: rtl !important;
                text-align: right !important;
            }

            [data-testid="stMarkdownContainer"] {
                direction: rtl;
                text-align: right;
            }

            [data-testid="stForm"] {
                direction: rtl;
                text-align: right;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_documents(
    texts: Sequence[str],
) -> None:
    st.subheader("متن‌های موجود")

    for index, text in enumerate(texts, start=1):
        with st.container(border=True):
            st.caption(f"متن {index}")
            st.write(text)


def render_search(
    search_service: SemanticSearchService,
) -> None:
    st.subheader("جست‌وجوی معنایی")

    with st.form("semantic_search_form"):
        query = st.text_area(
            label="عبارت موردنظر را وارد کنید",
            placeholder="مثلاً: کامپیوترهای هوشمند",
            height=140,
        )

        submitted = st.form_submit_button(
            label="جست‌وجو",
            use_container_width=True,
        )

    if not submitted:
        return

    clean_query = query.strip()

    if not clean_query:
        st.warning("یک عبارت وارد کنید.")
        return

    try:
        with st.spinner("در حال جست‌وجو..."):
            results = search_service.search(
                query=clean_query,
                k=1,
            )

    except Exception as error:
        st.error("جست‌وجو ناموفق بود.")
        st.code(str(error))
        return

    if not results:
        st.warning("متنی پیدا نشد.")
        return

    closest_document = results[0]

    with st.container(border=True):
        st.markdown("**نزدیک‌ترین متن**")
        st.write(closest_document.page_content)