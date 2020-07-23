from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def key_unwrap(kek, ciphertext, iv):
    n = len(ciphertext) // 8 - 1
    a = ciphertext[:8]
    r = [None]
    for i in range(1, n + 1):
        r.append(ciphertext[i*8:(i + 1)*8])

    for j in range(5, -1, -1):
        for i in range(n, 0, -1):
            t = n*j+i
            b = AES_decrypt(kek, xor(a, t) + r[i])
            a  = msb(64, b)
            r[i] = lsb(64, b)

    if a != iv:
        raise ValueError("Integrity Check Failed.")

    return r[1:]
    

def AES_decrypt(key, b):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    return decryptor.update(b) + decryptor.finalize()

def msb(j, W):
    j //= 8
    return W[0:j]

def lsb(j, W):
    j //= 8
    return W[len(W) - j:]

def xor(arr, i):
    l = len(arr)
    r = int.from_bytes(arr, byteorder='big') ^ i
    return int.to_bytes(r, byteorder='big', length=l)