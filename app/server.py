import socket
import threading
import time

servers = []

class Server:
    def __init__(self, host, port):
        global servers
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serv_socket.bind(self.addr) 
            self.serv_socket.listen() 
        except:
            return print("\nError starting the server!\n")

        self.player1 = ['X', 'X', 'X', 'X', 'X']
        self.player2 = ['X', 'X', 'X', 'X', 'X']
        self.move = ['None', 'None']
        self.command = ''
        self.clients = []
        self.users = []
        self.turn = 0
        servers.append(self)

    
    def handle_client(self, client):
        while True:
            username = client.recv(1024).decode()
            if username in self.users:
                client.send('0'.encode())
            else :
                client.send('1'.encode())
                break
        self.users.insert(self.clients.index(client), username)
        print(f"Client {username} connected")

        client.send('0'.encode())
        while True:
            if len(self.users) == 2:
                client.send('2'.encode())
                break

        self.receive(client)


    def receive(self, client):
        time.sleep(1)
        self.broadcast(client, f'{self.users[self.clients.index(client)]}?')
        while True:
            try:
                data = client.recv(1024).decode()

                if data == 'quit':
                    client.send('exit'.encode())
                    raise

                self.move[self.clients.index(client)] = data

                if self.move[0] == 'rock' or self.move[0] == 'paper' or self.move[0] == 'scissor':
                    self.broadcast(self.clients[0], f'{self.users[0]}.moviment')
                if self.move[1] == 'rock' or self.move[1] == 'paper' or self.move[1] == 'scissor':
                    self.broadcast(self.clients[1], f'{self.users[1]}.moviment') 

                if not self.move[self.clients.index(client)]:
                    raise

                if len( self.clients) < 2:
                    client.send("exit".encode())
                    raise

                if  self.move[0] != 'None' and  self.move[1] != 'None':
                     self.jokenpo()
                     
            except: 
                print(f"Client { self.users[ self.clients.index(client)]} disconnected")
                self.users.remove( self.users[ self.clients.index(client)])
                if client in self.clients:
                    self.clients.remove(client)
                break


    def jokenpo(self):
        if self.move[0] == self.move[1]:
            self.turn += 1
        elif self.move[0] == 'rock':
            if self.move[1] == 'paper':
                self.player2[self.turn] = 'O'
                self.turn += 1
            elif self.move[1] == 'scissor':
                self.player1[self.turn] = 'O'
                self.turn += 1
        elif self.move[0] == 'paper':
            if self.move[1] == 'rock':
                self.player1[self.turn] = 'O'
                self.turn += 1
            elif self.move[1] == 'scissor':
                self.player2[self.turn] = 'O'
                self.turn += 1
        else:
            if self.move[1] == 'rock':
                self.player2[self.turn] = 'O'
                self.turn += 1
            elif self.move[1] == 'paper':
                self.player1[self.turn] = 'O'
                self.turn += 1

        self.broadcast(None, 'round')
        time.sleep(0.2)

        self.broadcast(self.clients[0], f'{self.move[0]}.move')
        self.broadcast(self.clients[1], f'{self.move[1]}.move')

        self.broadcast(None, '.false')
        time.sleep(2)
        self.broadcast(None, '.release')

        if self.player1[self.turn - 1] == 'O':
            self.broadcast(None, self.users[1])
        elif self.player2[self.turn - 1] == 'O':
            self.broadcast(None, self.users[0])

        self.move[0] = 'None'
        self.move[1] = 'None'

        time.sleep(0.2)

        if self.turn == 5 or self.player1.count('O') == 3 or self.player2.count('O') == 3:
            if self.player1.count('O') > self.player2.count('O'):
                self.broadcast(None, f'{self.users[0]} won')
            elif self.player1.count('O') < self.player2.count('O'):
                self.broadcast(None, f'{self.users[1]} won')
            else:
                self.broadcast(None, "Draw")
            self.turn = 0
            self.player1 = ['X', 'X', 'X', 'X', 'X']
            self.player2 = ['X', 'X', 'X', 'X', 'X']


    def broadcast(self, client, mensagem):
        for c in self.clients:
            if c != client:
                try:
                    c.send(mensagem.encode())
                except:
                    return
                
    def server_control(self):
        while True:
            self.command = input()
            print("="*50)
            print(self.serv_socket.getsockname())
            
            if self.command == "exit":
                if len(self.clients) > 0:
                    for client in self.clients:
                        client.send("exit".encode())
                while True:
                    if len(self.clients) == 0 or self.command == "exit":
                        time.sleep(1)
                        self.serv_socket.close()
                        break
                break

            elif self.command == "list":
                print(f"Clients Online: {len(self.clients)}")
                for i in range(len(self.clients)):
                    print(f"User:{self.users[i]}  Addr:{self.clients[i].getpeername()}")

            elif self.command == "ban":
                print(f"Clients Online: {len(self.clients)}")
                for i in range(len(self.clients)):
                    print(f"User: {i} - {self.users[i]}  Addr:{self.clients[i].getpeername()}")
                while True:
                    try:
                        user = int(input("Enter the number of user to ban: "))
                    except:
                        print("Invalid input")
                        continue
                    break
                if user in range(len(self.clients)):
                    self.clients[user].send("exit".encode())
                    print(f"User {self.users[user]} banned")
                else:
                    print("User not found")

            elif self.command == "help":
                print("Commands: list, exit, ban")
                print("list: List all clients connected to the server")
                print("exit: Close the server")
                print("ban: Ban a client from the server")


    def starting(self):       
        threading.Thread(target=self.server_control).start()

        print ("Server started, waiting for connections...\n")
        while True:
            try:
                client_socket, client_addr = self.serv_socket.accept() 
                if len(self.clients) < 2:
                    client_socket.send('1'.encode())
                else:
                    client_socket.send('0'.encode())
                    client_socket.close()
                    continue
            except:
                print("Server stopped")
                break
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=[client_socket]).start()


def main():
    global servers
    host = '26.97.160.140'

    for i in range(1):
        Server(host, 62000 + i)

    for i in range(len(servers)):
        threading.Thread(target=servers[i].starting).start()


if __name__ == "__main__":
    main()


        