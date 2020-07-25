import base64

def two():
    txt = open("./data/payload_2.txt", "r")
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