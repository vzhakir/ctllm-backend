def evaluate_answer(user_answer: str, expected_answer: str) -> bool:
    """
    Ultra-simple evaluator; can be replaced with semantic scoring later.
    """
    if not user_answer or not expected_answer:
        return False

    return user_answer.lower().strip() in expected_answer.lower().strip()