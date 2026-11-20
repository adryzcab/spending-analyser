def resolve_answer(answer: str, current: str, categories: list[str]) -> str | None:
    """Turn a typed answer into a category.
    
    Empty input keeps the current category. Matching ignores case.
    Returns None is the answer isn't a known category.
    """
    answer = answer.strip()
    if answer == "":
        return current
    for category in categories:
        if category.lower() == answer.lower():
            return category
    return None