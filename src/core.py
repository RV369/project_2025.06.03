from collections import Counter


def count_str(str, item):
    m = Counter([i.content for i in item])
    return m[str]
