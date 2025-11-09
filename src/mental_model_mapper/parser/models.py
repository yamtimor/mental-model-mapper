from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Tuple, Optional

# Enums
class Source(str, Enum):
    """
    Where a document came from.
    - LOCAL: Local files
    - NOTION: Notion export / API (later)
    - WEB: Crawled HTML (later)
    - API: Any external API (later)
    """
    LOCAL = "local"
    NOTION = "notion"
    WEB = "web"
    API = "api"

# Document level
@dataclass(frozen=True)
class DocumentMeta:
    """
    Stable, author-time info about the document itself.
    Keep this small; it's carried everywhere.
    - source: Where the document came from
    - extension: The extension of the document
    - title: The title of the document
    - creation_date: The date the document was created
    - tags: The tags of the document
    """
    source: Source
    extension: str
    title: Optional[str] = None
    creation_date: Optional[datetime] = None
    tags: Tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class Document:
    """
    A cleaned text unit ready for downstream processing.
    - id: stable identifier (e.g., sha1 of URI or URI+mtime)
    - uri: locator (absolute path or URL). Keep immutable once set.
    - text: normalized plaintext/markdown
    - meta: DocumentMeta (source, ext, title, etc.)
    """
    id: str
    uri: str
    text: str
    meta: DocumentMeta

# Chunk level
@dataclass(frozen=True)
class ChunkMeta:
    """
    Context about a chunk within its parent document.
    - doc_id: The id of the document
    - order: 0-based order in the document
    - start_char: The start character of the chunk
    - end_char: The end character of the chunk
    - heading: The nearest Markdown/section heading if available
    - tokens: The optional token count (fill later if you measure)
    """
    doc_id: str
    order: int
    start_char: int
    end_char: int
    heading: Optional[str] = None
    tokens: Optional[int] = None

@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    meta: ChunkMeta

# Loader/parse observability
@dataclass(frozen=True)
class ParseStats:
    """
    Lightweight stats for loaders; useful in logs/tests.
    - bytes_read: The number of bytes read
    - chars_before_clean: The number of characters before cleaning
    - chars_after_clean: The number of characters after cleaning
    - files_count: The number of files read
    """
    bytes_read: int
    chars_before_clean: int
    chars_after_clean: int
    files_count: int = 1

__all__ = [
    "Source",
    "DocumentMeta",
    "Document",
    "ChunkMeta",
    "Chunk",
    "ParseStats",
]