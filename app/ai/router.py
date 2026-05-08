from typing import Tuple, Optional

ROUTING_TABLE = {
    # High-quality tasks -> Claude
    "chapter_gen":      ("anthropic", "claude-3-5-sonnet-20240620", 0.85),
    "quality_setting":  ("anthropic", "claude-3-5-sonnet-20240620", 0.3),
    "quality_character":("anthropic", "claude-3-5-sonnet-20240620", 0.3),
    "quality_plot":     ("anthropic", "claude-3-5-sonnet-20240620", 0.3),
    "quality_style":    ("anthropic", "claude-3-5-sonnet-20240620", 0.3),
    "simulation":       ("anthropic", "claude-3-5-sonnet-20240620", 0.9),
    "outline_chapter":  ("anthropic", "claude-3-5-sonnet-20240620", 0.7),

    # Low-cost tasks -> DeepSeek
    "summary":          ("deepseek", "deepseek-chat", 0.3),
    "event_extract":    ("deepseek", "deepseek-chat", 0.2),
    "quality_basic":    ("deepseek", "deepseek-chat", 0.2),
    "tag_extract":      ("deepseek", "deepseek-chat", 0.2),

    # Creative tasks
    "topic_brainstorm": ("anthropic", "claude-3-5-sonnet-20240620", 1.0),
    "world_gen":        ("anthropic", "claude-3-5-sonnet-20240620", 0.8),
    "character_gen":    ("anthropic", "claude-3-5-sonnet-20240620", 0.85),

    # Embedding
    "embedding":        ("bge", "bge-m3", None),
}

def get_route(module: str) -> Tuple[str, str, Optional[float]]:
    return ROUTING_TABLE.get(module, ("anthropic", "claude-3-5-sonnet-20240620", 0.7))
