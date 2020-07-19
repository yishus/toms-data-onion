import base64


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


def three():
    txt = open("./decrypted/payload_3.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)


three()
