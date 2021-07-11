import socket
from data.enums import buffer


host = input('enter ip address: ')
port = int(input('enter port number: '))

address = (host, port)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, 0))
s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def send_file():
    file_name = input('insert path to a file: ')
    f = open(file_name, "rb")
    data = f.read(buffer)

    print('sending data...')
    while data:
        if s.sendto(data, address):
            data = f.read(buffer)

    f.close()


send_file()

while True:
    if input('Exit? (y/n)') == 'y':
        s.close()
        break
    send_file()
