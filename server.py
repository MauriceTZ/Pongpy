import socket

SERVER_ADDRESS = socket.gethostname(), 6969
serversocket = socket.socket()
serversocket.bind(SERVER_ADDRESS)
serversocket.listen()


while True:
    (clientsocket, address) = serversocket.accept()
    print(clientsocket)
    clientsocket.close()
