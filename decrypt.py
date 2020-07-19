import base64


def start():
    txt = open("./payload.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    one = open("./1.txt", "w")
    one.write(txt_decode.decode("UTF-8"))
    one.close()


def one():
    txt = open("./payload_1.txt", "r")
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

    two = open("./2.txt", "w")
    two.write(bytes(decoded).decode("utf8"))
    two.close()


one()
