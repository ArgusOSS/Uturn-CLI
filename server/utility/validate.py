import re

def validate_hash(hash):
    return bool(re.test(r"\b[0-9a-f]{5,40}\b", hash))

