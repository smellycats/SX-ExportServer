# -*- coding: utf-8 -*-

# ip地址转整数
def ip2int(ip):
    return struct.unpack('!I', socket.inet_aton(ip))[0]
