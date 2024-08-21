import pygame as pg
import socket

SIZE = (1000, 1000)
CLOCK = pg.time.Clock()
FPS = 60

SERVER_ADDRESS = socket.gethostname(), 6969
clientsocket = socket.socket()
clientsocket.connect(SERVER_ADDRESS)
print("HOLA", clientsocket)

pg.init()
pg.display.set_caption("Pongpy")
pg.display.set_mode(SIZE)

while True:
    for evento in pg.event.get():
        match evento.type:
            case pg.QUIT:
                pg.quit()
                exit()

    pg.display.update()
    CLOCK.tick(FPS)
