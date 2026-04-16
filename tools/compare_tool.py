import re

def compare_cost(billed, retrieved_text):
    """
    Compare billed cost with actual cost from RAG result
    """

    # 🔥 get ALL numbers
    numbers = re.findall(r'\d+', retrieved_text)

    if not numbers:
        return {
            "actual_cost": None,
            "difference": None,
            "overcharged": None
        }

    # 🔥 take LAST number (cost is always last)
    actual = int(numbers[-1])

    diff = billed - actual

    return {
        "actual_cost": actual,
        "difference": diff,
        "overcharged": diff > 0
    }
