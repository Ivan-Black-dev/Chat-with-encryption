import socket
from threading import Thread
from rsa import RSA

class Client:

    def __init__(this, IP, PORT):
        this.IP = IP
        this.PORT = PORT
        this.rsa = RSA()

    def start(this):

        # Настройка сокета
        this.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Подключение
        this.sock.connect((this.IP, this.PORT))
        print(f'[*] Connected to {this.IP}:{this.PORT}')
        
        # Обмен ключами
        keys = (this.sock.recv(1024)).decode()
        e, n = [int(i) for i in keys.split()]
        print(f"[*] Your keys: e = {this.rsa.e}; d = {this.rsa.d}; n = {this.rsa.n}")
        print(f"[*] Users keys: e = {e}; n = {n}")
        this.rsa.setTargetKeys(e, n)

        myKeys = this.rsa.getYourKeys()
        sendKey = str(myKeys[0]) + " " + str(myKeys[1])
        this.sock.send(sendKey.encode())

        this.senderThread =  Thread(target=this.sender)
        this.writerThread = Thread(target=this.writer)
        this.senderThread.start()
        this.writerThread.start()

    def sender(this):
        while True:
            message = input()
            message = str(this.rsa.encodeString(message))[1:-1]
            this.sock.send(message.encode())

    def writer(this):
        while True:
            data = this.sock.recv(1024)
            if data:
                data = data.decode()
                data = this.rsa.decodeString([int(i) for i in data.replace(',', '').split()])
                print(f"[user]: {data}")

    
if __name__ == '__main__':
    c = Client('194.226.139.101', 4006)
    c.start()