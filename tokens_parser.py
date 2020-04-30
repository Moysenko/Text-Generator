import re
import string


def get_tokens(data, regex=None):
    if regex:
        return re.findall(regex, data)

    tokens = re.findall(f"([-\w]+|[{string.punctuation}])", data)
    return tokens