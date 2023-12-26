import socket
from threading import Thread
from rsa import RSA


class Server:
    
    def __init__(this, IP, PORT):
        this.IP = IP
        this.PORT = PORT
        this.rsa = RSA()

    def start(this):

        # Настройка сокета
        this.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.sock.bind((this.IP, this.PORT))
        print(f"[*] Server bind from: {this.IP}:{this.PORT}")
        this.sock.listen(1)

        # Подключение 
        conn, adrr = this.sock.accept()
        print(f"[*] Connect user: {adrr}")
        this.conn = conn
        
        # Обмен ключами
        print(f"[*] Your keys: e = {this.rsa.e}; d = {this.rsa.d}; n = {this.rsa.n}")
        myKeys = this.rsa.getYourKeys()
        sendKey = str(myKeys[0]) + " " + str(myKeys[1])
        this.conn.send(sendKey.encode())

        keys = (this.conn.recv(1024)).decode()
        e, n = [int(i) for i in keys.split()]
        this.rsa.setTargetKeys(e, n)
        print(f"[*] Users keys: e = {e}; n = {n}")

        # Начало переписки
        print(f"[*] Chat started")
        this.isStart = True
        this.senderThread =  Thread(target=this.sender).start()
        this.writerThread = Thread(target=this.writer).start()
    
    def __del__(this):
        print('[*] Chat stoped')
        this.sock.close()

    def sender(this):
        while this.isStart:
            message = input()
            message = str(this.rsa.encodeString(message))[1:-1]
            this.conn.send(message.encode())
                

    def writer(this):
        while this.isStart:
            data = this.conn.recv(1024)
            if data:
                data = data.decode()
                data = this.rsa.decodeString([int(i) for i in data.replace(',', '').split()])
                print(f"[user]: {data}") 

if __name__ == '__main__':
    s = Server('127.0.0.1', 4006)
    s.start()