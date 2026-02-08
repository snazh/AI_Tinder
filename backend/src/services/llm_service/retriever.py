from app.data import DOCS

def search(query: str, limit: int = 5):
    """
    Тупой поиск: возвращает документы, где встречается query
    """
    results = [d for d in DOCS if query.lower() in d.lower()]
    return results[:limit]
