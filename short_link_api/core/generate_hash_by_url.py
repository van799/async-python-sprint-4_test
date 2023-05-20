import base64
import time
from urllib.parse import quote


class Helper:
    @staticmethod
    def generate_hash(url, username, time_now=time.time()):
        str_to_hash = f"{username}+{url}+{str(time_now)}"
        hash_b = str(hash(str_to_hash)).encode('utf-8')
        quote_hash_b = quote(base64.urlsafe_b64encode(hash_b).decode('utf-8'))
        return quote_hash_b.replace('%', '')


result = Helper.generate_hash('ya.ru', 'lexx')
print(result)
