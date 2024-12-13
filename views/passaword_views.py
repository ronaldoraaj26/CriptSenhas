import string,secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet

class FernetHasher:
    RANDOM_STRING_CHARGS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)



    @classmethod
    def get_randon_string(cls, length=25):
        string = ''
        for i in range(length):
           string = string + secrets.choice(cls.RANDOM_STRING_CHARGS)

        return string

    @classmethod
    def create_key(cls, archive=False):
        value = cls.get_randon_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        file = 'key.key'
        while Path(cls.KEY_DIR / file).exists():
            file = f'key_{cls.get_randon_string(length=5)}.key'

        with open(cls.KEY_DIR / file, 'wb') as arq:
            arq.write(key)

        return cls.KEY_DIR / file   


print(FernetHasher.create_key(archive=True))            



