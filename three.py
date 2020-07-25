import base64

def explore_three():
    txt = open("./data/payload_3.txt", "r")
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
    txt = open("./data/payload_3.txt", "r")
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