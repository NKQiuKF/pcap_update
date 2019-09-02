# coding=utf-8
import re


def addr2int(value):
    """
    IP to Int
    Note: socket.inet_ntop not available everywhere
    (Reference: https://docs.python.org/2/library/socket.html#socket.inet_ntop)
    """
    _ = value.split('.')
    return (long(_[0]) << 24) + (long(_[1]) << 16) + (long(_[2]) << 8) + long(_[3])


def int2addr(value):
    """
    Int to IP
    """
    return '.'.join(str(value >> n & 0xff) for n in (24, 16, 8, 0))


def make_mask(bits):
    return 0xffffffff ^ (1 << 32 - bits) - 1


def compress_ipv6(address):
    zeros = re.findall("(?:0000:)+", address)
    if zeros:
        address = address.replace(sorted(zeros, key=lambda _: len(_))[-1], ":", 1)
        address = re.sub(r"(\A|:)0+(\w)", "\g<1>\g<2>", address)
        if address == ":1":
            address = "::1"
    return address


def inet_ntoa6(packed_ip):
    _ = packed_ip.encode("hex")
    return compress_ipv6(':'.join(_[i:i + 4] for i in xrange(0, len(_), 4)))
