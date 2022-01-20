from unicodedata import name
import os
import socket

def main():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname) + ':8000'
    print(local_ip)
    os.system('python3 manage.py runserver ' + local_ip)


if __name__ == '__main__':
    main()
