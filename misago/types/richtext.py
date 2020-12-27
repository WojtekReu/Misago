from typing import Any, List, Dict

# Mypy bugs are preventing proper typing for richtext:
# 1. literals are ignored in dict type matching
# 2. recursive types unsupported

RichTextBlock = Dict[str, Any]
RichText = List[RichTextBlock]
