import socket
import os
from data.enums import file_save_directory, default_file_name, buffer


def _get_full_file_path(f_name):
    return file_save_directory / f_name


def _generate_file_name():
    f_name = default_file_name
    counter = 1
    while os.path.exists(_get_full_file_path(f_name)):
        f_name = f'sample ({counter}).wav'
        counter += 1

    return f_name


host = input('enter ip address: ')
port = int(input('enter port number: '))

# create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set timeout to make socket operations non-blocking
# see https://docs.python.org/3/library/socket.html#socket.socket.settimeout
s.settimeout(0.01)

# Bind the ip and port number to the socket
s.bind((host, port))

while True:
    file = None
    try:
        data, address = s.recvfrom(buffer)
        print(f'server received data from: {address}')

        file_name = _generate_file_name()

        file = open(_get_full_file_path(file_name), 'wb')

        while data:
            file.write(data)
            data, address = s.recvfrom(buffer)
        file.close()
    except socket.timeout:
        if file is not None:
            file.close()
