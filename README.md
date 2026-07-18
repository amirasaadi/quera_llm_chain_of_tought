# LLM Quera exercises

This repository contains exercises and small projects about large language
models, chain-of-thought techniques, embeddings, and vector search.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key for the vector-search examples

## Setup

Clone the repository and install the locked dependencies:

```bash
uv sync
```

Create `.env` in the repository root with:

```dotenv
GOOGLE_API_KEY=your_google_api_key
```

Do not commit `.env` or share your API key.

## Semantic-search app

The Streamlit application embeds a small collection of Persian documents with
Gemini, stores the vectors in Chroma, and returns the document closest to a
search query.

Run it from the repository root:

```bash
uv run streamlit run Vectors/semantic_search_app.py
```

Then open the local URL printed by Streamlit, normally
<http://localhost:8501>.

The example documents are defined in
`Vectors/semantic_search/data/trf.xlsx`. Encode column C (`شرح`) and store
column B (`کد تعرفه`) as result metadata before starting the app:

```bash
uv run python Vectors/encode_tariffs.py --reset
```

The encoder prints progress after every successful batch and writes a
checkpoint into `Vectors/chroma_db/`. If it is interrupted, run it again
without `--reset` to continue from the last completed batch:

```bash
uv run python Vectors/encode_tariffs.py
```

The default batch and delay settings are paced for a quota of 100 embedded
items per minute. You can adjust them with `--batch-size` and `--delay` to
match the active limits shown for your project in Google AI Studio.

Chroma's generated local database is stored in `Vectors/chroma_db/`.

## Standalone embedding example

To generate embeddings and print their dimensions:

```bash
uv run python Vectors/encoding_hscodes.py
```

## Repository structure

```text
.
├── Chain_of_tought/              # Chain-of-thought experiment notebooks
├── Vectors/
│   ├── encoding_hscodes.py       # Standalone embedding example
│   ├── semantic_search_app.py    # Streamlit entry point
│   └── semantic_search/          # Search configuration, UI, and vector store
├── pyproject.toml                # Project metadata and dependencies
└── uv.lock                       # Locked dependency versions
```

## Notes

- The first app run may take longer while dependencies, embeddings, and the
  local vector database are initialized.
- Using the Gemini API may consume quota or incur charges on your Google
  account.
- Jupyter notebooks may require an editor with notebook support, such as
  JupyterLab or VS Code.
