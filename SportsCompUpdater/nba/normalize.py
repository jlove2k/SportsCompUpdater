from __future__ import annotations

import re
import unicodedata


SUFFIX_RE = re.compile(r"\b(jr|sr|ii|iii|iv|v)\.?\b", re.IGNORECASE)
NON_NAME_RE = re.compile(r"[^a-z0-9 ]+")


def normalize_name(name: str) -> str:
    text = unicodedata.normalize("NFKD", name)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.lower().replace("'", "")
    text = SUFFIX_RE.sub("", text)
    text = NON_NAME_RE.sub(" ", text)
    return " ".join(text.split())

