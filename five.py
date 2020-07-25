import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from key_wrap import key_unwrap

def five():
    txt = open("./data/payload_5.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    kek = txt_decode[0:32]
    iv = txt_decode[32:40]
    wrapped_key = txt_decode[40:80]
    iv_payload = txt_decode[80:96]
    payload = txt_decode[96:]

    key = key_unwrap(kek, wrapped_key, iv)

    backend = default_backend()
    cipher = Cipher(algorithms.AES(b''.join(key)), modes.CBC(iv_payload), backend=backend)
    decryptor = cipher.decryptor()
    decoded = decryptor.update(payload) + decryptor.finalize()

    six = open("./decrypted/6.txt", "w")
    six.write(bytes(decoded).decode("utf8"))
    six.close()