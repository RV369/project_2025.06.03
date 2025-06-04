async def count_str(string: str, item: list) -> int:
    """Подсчитывает частоту слов"""
    m = 0
    for post in item:
        m += post.content.count(string)
    return m
