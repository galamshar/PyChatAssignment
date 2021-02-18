import socket
import pickle
import threading
import datetime

from Database.dbrepository import DbRepo


class ThreadedServer(object):
    connections = []
    history = []
    dbrepo = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.dbrepo = DbRepo()
        self.listen()

    def listen(self):
        self.sock.listen(5)
        print('Awaiting connection to port...')
        while True:
            client, address = self.sock.accept()
            print(f"Client {address[0]} was connected")
            type(self).connections.append(client)
            threading.Thread(target=self.listen_client, args=(client, address)).start()

    def listen_client(self, conn, address):
        conn.send(b"Hello! Please, entry your login: ")
        login = conn.recv(1024).decode()
        user = self.dbrepo.getUser(login)
        if user is None:
            conn.send(b"Oh, you are first at our server.\nPlease, entry your password: ")
            passwd = conn.recv(1024).decode()
            self.dbrepo.createUser(login, passwd)
            conn.send(b"Welcome!")
        else:
            while True:
                conn.send(b"Please, entry your password: ")
                passwd = conn.recv(1024).decode()
                if user[2] == passwd:
                    conn.send(b"Welcome!")
                    break
                else:
                    conn.send(b"Wrong password")
        for line in type(self).history:
            conn.send(line.encode())
        conn.send(b"End")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print("Data was got")
                line = f"{datetime.datetime.now()} {login}: {data.decode()}"
                type(self).history.append(f"> {line}\n")
                for con in type(self).connections:
                    con.send(line.encode())
                self.dbrepo.createMessage(data.decode(), user[0])
            except ConnectionResetError:
                type(self).connections.remove(conn)
                conn.close()
                break
        print('Connection with', address[0], 'was closed')


if __name__ == "__main__":
    PORT = 5100
    thr = threading.Thread(target=ThreadedServer, args=('', PORT), daemon=True)
    thr.start()
    while True:
        msg = input("Enter your message: ")
        if msg == 'stop':
            break
