import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    google_api_key: str
    chroma_directory: Path
    collection_name: str = "educational_texts"
    embedding_model: str = "gemini-embedding-001"


def load_settings() -> Settings:
    load_dotenv(
        PROJECT_ROOT / ".env",
        override=True,
    )

    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY در فایل .env پیدا نشد."
        )

    return Settings(
        google_api_key=google_api_key,
        chroma_directory=PROJECT_ROOT / "Vectors" / "chroma_db",
    )