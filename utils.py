import hashlib
import string
from bson import Binary
import uuid

def uuid_to_binary(uuid_string):
    return Binary(uuid.UUID(uuid_string).bytes, subtype=4)

def base62_encode(num):
    base = string.digits + string.ascii_letters
    if num == 0:
        return base[0]
    arr = []
    while num:
        num, rem = divmod(num, len(base))
        arr.append(base[rem])
    arr.reverse()
    return ''.join(arr)

def generate_short_url(uuid_str,length=8):
    hash_object = hashlib.md5(uuid_str.encode())
    large_int = int(hash_object.hexdigest(), 16)
    short_url = base62_encode(large_int)
    return short_url[:length]


# import string
# import random
# import re

# def generate_short_code(length=6):
#     """Generate a random short code of specified length"""
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))

# def is_valid_url(url):
#     """Check if the provided URL is valid using a regex pattern"""
#     url_regex = re.compile(
#         r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
#     )
#     return re.match(url_regex, url) is not None
