from Crypto.Cipher import DES3
import base64

def __pkcs5_pad(str):
    s = DES3.block_size
    return str + (s - len(str) % s) * chr(s - len(str) % s)

def __pkcs5_unpad(str):
    return str[0:-ord(str[-1])]

def encrypt(data, key):
    des3 = DES3.new(key, DES3.MODE_ECB)
    str = des3.encrypt(__pkcs5_pad(data))
    return base64.b64encode(str)

def decrypt(data, key):
    data = base64.b64decode(data)
    des3 = DES3.new(key, DES3.MODE_ECB)
    str = des3.decrypt(data);
    return __pkcs5_unpad(str);