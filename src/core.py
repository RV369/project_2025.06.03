async def count_str(string: str, items: list) -> int:
    """Подсчитывает частоту слов"""
    m = 0
    for post in items:
        m += post.content.count(string)
    return m
