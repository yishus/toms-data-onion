import base64

def start():
    txt = open("./data/payload.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    one = open("./decrypted/1.txt", "w")
    one.write(txt_decode.decode("UTF-8"))
    one.close()