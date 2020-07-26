import base64
from vm import Vm

def six():
    txt = open("./data/payload_6.txt", "r")
    txt_string = txt.read()
    txt_decode = base64.a85decode(txt_string, adobe=True)

    # vm = Vm(bytes.fromhex('50 48 c2 02 a8 4d 00 00 00 4f 02 50 09 c4 02 02 e1 01 4f 02 c1 22 1d 00 00 00 48 30 02 58 03 4f 02 b0 29 00 00 00 48 31 02 50 0c c3 02 aa 57 48 02 c1 21 3a 00 00 00 48 32 02 48 77 02 48 6f 02 48 72 02 48 6c 02 48 64 02 48 21 02 01 65 6f 33 34 2c'))
    vm = Vm(bytearray(txt_decode))
    vm.run()

six()