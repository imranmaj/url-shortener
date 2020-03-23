

def make_url_id(chars: str, length: int, n: int) -> str:
    """
    Returns a string of length length using given chars
        that is unique given a unique n
    """

    result = str()
    while n and len(result) < length:
        result = chars[n % len(chars)] + result
        n //= len(chars)
    result = (length - len(result)) * chars[0] + result
    return result