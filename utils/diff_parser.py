def combine_diffs(diffs: dict) -> str:
    """
    Combine multiple file diffs into a single string.
    Args:
        diffs: Dictionary of {filename: diff_string}
    Returns:
        A single formatted diff string
    """
    parts = []
    for filename, diff in diffs.items():
        parts.append(f"=== FILE: {filename} ===\n{diff}\n")
    return "\n".join(parts)


def truncate_diff(diff_text: str, max_chars: int = 8000) -> str:
    """
    Truncate long diffs to avoid hitting LLM token limits.
    Prioritizes the beginning and end of the diff.
    """
    if len(diff_text) <= max_chars:
        return diff_text

    # Take first 70% and last 30% to preserve context
    first_part = diff_text[:int(max_chars * 0.7)]
    last_part = diff_text[-int(max_chars * 0.3):]
    return f"{first_part}\n\n--- TRUNCATED ---\n\n{last_part}"
