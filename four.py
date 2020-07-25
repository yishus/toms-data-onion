import base64
import ipaddress

def four():
    txt = open("./data/payload_4.txt", "r")
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