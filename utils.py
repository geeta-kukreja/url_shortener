import hashlib
import re
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

def validate_custom_short_code(short_code):
    return bool(re.match(r'^[0-9a-zA-Z]{6,10}$', short_code))
