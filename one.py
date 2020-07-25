import base64

def one():
    txt = open("./data/payload_1.txt", "r")
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