import hashlib
def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()