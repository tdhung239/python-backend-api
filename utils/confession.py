import re


def validate_content_null(content: str):
    alpha_regex = r'\s'
    if re.match(alpha_regex, content) or not content:
        return False
    return True
