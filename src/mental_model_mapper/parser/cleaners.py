from __future__ import annotations
import re

try:
    from ftfy import fix_text
except ImportError:
    ftfy = None

_WS_RUN = re.compile(fr"[ \t]+(?=\n)|[ \t]+{2,}")
_BLANKS = re.compile(r"\n{3,}")

def basic_clean(text: str) -> str:
    # normalize newlines first
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # unicode fixes (if available)
    if ftfy is not None:
        text = fix_text(text)
    # trim per-line and collapse whitespace
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = _WS_RUN.sub(lambda m: "" if m.group(0).endswith("\n") else " ", text)
    # collapse blank lines into a single blank line
    text = _BLANKS.sub("\n\n", text)
    return text.strip()