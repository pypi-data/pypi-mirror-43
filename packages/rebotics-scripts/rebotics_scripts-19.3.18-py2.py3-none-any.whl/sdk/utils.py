import hashlib
from functools import partial


def hash_file(file, block_size=65536):
    hash_ = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hash_.update(buf)

    return hash_.hexdigest()
