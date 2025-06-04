from collections import Counter


async def count_str(string: str, item: list) -> int:
    """Подсчитывает частоту слов"""
    return Counter([i.content for i in item])[string]
