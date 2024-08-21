import socket


SERVER_ADDRESS = socket.gethostname(), 6969
serversocket = socket.socket()
serversocket.bind(SERVER_ADDRESS)
serversocket.listen()
print("esperando conexiones...")

while True:
    (clientsocket, address) = serversocket.accept()
    print("recibido:", clientsocket.recv(100).decode())
    clientsocket.close()

