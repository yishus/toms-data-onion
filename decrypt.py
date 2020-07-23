import base64
import ipaddress
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from key_wrap import key_unwrap


def start():
    txt = open("./data/payload.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    one = open("./decrypted/1.txt", "w")
    one.write(txt_decode.decode("UTF-8"))
    one.close()


def one():
    txt = open("./decrypted/payload_1.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    # Flip every second bit
    # XOR 01010101 = 85
    decoded = []
    for b in txt_decode:
        decoded.append(b ^ 85)

    # Move one bit to the right
    for i, b in enumerate(decoded):
        # Get last bit
        bit = b & 1
        decoded[i] = bit << 7 | b >> 1

    two = open("./decrypted/2.txt", "w")
    two.write(bytes(decoded).decode("utf8"))
    two.close()


def two():
    txt = open("./decrypted/payload_2.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    good_bits = []
    for b in txt_decode:
        parity = b & 1
        count = 0
        sig = format(b, "08b")[:-1]
        for bit in sig:
            if bit == "1":
                count += 1
        if count % 2 == parity:
            good_bits.extend(sig)

    decoded = []
    for b in range(int(len(good_bits) / 8)):
        byte = "".join(good_bits[b * 8 : (b + 1) * 8])
        decoded.append(chr(int(byte, 2)))
    three = open("./decrypted/3.txt", "w")
    three.write("".join(decoded))
    three.close()


def explore_three():
    txt = open("./decrypted/payload_3.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    key = []
    for i, c in enumerate("==[ Layer 4/6: "):
        key.append(ord(c) ^ txt_decode[i])

    # check where the = char starts
    start = 0
    while start < 60:
        char = chr(key[start] ^ txt_decode[start + 32])
        if char == "=":
            break
        start += 1

    idx = 15
    # fill up the keys from i = 15 till end of line
    # line is 60 char long
    while idx < 60 - 32 - start:
        key.append(ord("=") ^ txt_decode[32 + idx])
        idx += 1

    # let's look at first 28 chars decoded
    j = 0
    d = []
    while j < len(key):
        d.append(chr(txt_decode[j] ^ key[j]))
        j += 1

    print("".join(d))

    # it prints out ==[ Layer 4/6: Network Traff
    # We can guess that it will be ==[ Layer 4/6: Network Traffic ] for the first 32 chars
    # let's get the last 4 keys
    for i, c in enumerate("ic ]"):
        key.append(ord(c) ^ txt_decode[i + 28])


def three():
    txt = open("./decrypted/payload_3.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    key = []
    for i, c in enumerate("==[ Layer 4/6: Network Traffic ]"):
        key.append(ord(c) ^ txt_decode[i])

    key_len = len(key)
    decoded = []
    for i, byte in enumerate(txt_decode):
        key_pos = i % key_len
        decoded.append(chr(byte ^ key[key_pos]))
    four = open("./decrypted/4.txt", "w")
    four.write("".join(decoded))
    four.close()


def four():
    txt = open("./decrypted/payload_4.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    decoded = []

    start = 0

    while start < len(txt_decode):
        (size, source_ip, dest_ip, ipv4_valid) = ipv4_header(
            txt_decode[start : start + 20]
        )
        (dest_port, udp_valid) = udp_header(
            txt_decode[start + 20 : start + 28],
            txt_decode[start : start + 20],
            txt_decode[start + 28 : start + size],
        )

        if (
            source_ip == "10.1.1.10"
            and dest_ip == "10.1.1.200"
            and dest_port == 42069
            and ipv4_valid
            and udp_valid
        ):
            decoded.extend(txt_decode[start + 28 : start + size])

        start = start + size

    five = open("./decrypted/5.txt", "w")
    five.write(bytes(decoded).decode("utf8"))
    five.close()


def five():
    txt = open("./decrypted/payload_5.txt", "r")
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

def ipv4_header(bytes):
    size = bytes[2] << 8 | bytes[3]
    source_ip = str(
        ipaddress.IPv4Address(
            (bytes[12] << 24 | bytes[13] << 16 | bytes[14] << 8 | bytes[15])
        )
    )
    dest_ip = str(
        ipaddress.IPv4Address(
            (bytes[16] << 24 | bytes[17] << 16 | bytes[18] << 8 | bytes[19])
        )
    )
    sum = 0
    add_one = False
    for i in range(0, 20, 2):
        sum += bytes[i] << 8 | bytes[i + 1]
    while sum > 0xFFFF:
        v = sum & 0xFFFF
        carry = sum >> 16
        sum = v + carry
        if add_one:
            sum += 1
        add_one = True

    return (size, source_ip, dest_ip, sum == 0xFFFF)


def udp_header(bytes, ipv4_header_bytes, data):
    source_port = bytes[0] << 8 | bytes[1]
    dest_port = bytes[2] << 8 | bytes[3]
    length = bytes[4] << 8 | bytes[5]
    checksum = bytes[6] << 8 | bytes[7]

    source_ip_bytes_1 = ipv4_header_bytes[12] << 8 | ipv4_header_bytes[13]
    source_ip_bytes_2 = ipv4_header_bytes[14] << 8 | ipv4_header_bytes[15]
    dest_ip_bytes_1 = ipv4_header_bytes[16] << 8 | ipv4_header_bytes[17]
    dest_ip_bytes_2 = ipv4_header_bytes[18] << 8 | ipv4_header_bytes[19]

    sum = (
        source_ip_bytes_1
        + source_ip_bytes_2
        + dest_ip_bytes_1
        + dest_ip_bytes_2
        + 17
        + length
        + source_port
        + dest_port
        + length
        + checksum
    )

    data_size = len(data)
    for i in range(0, data_size, 2):
        if i + 1 == data_size:
            sum += data[i] << 8 | 0
        else:
            sum += data[i] << 8 | data[i + 1]

    while sum > 0xFFFF:
        v = sum & 0xFFFF
        carry = sum >> 16
        sum = v + carry

    return (dest_port, sum == 0xFFFF)


five()
