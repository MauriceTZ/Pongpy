import pygame as pg
import socket
import threading
import json
import sys

print(sys.version)
SIZE_WINDOW = 900, 900
SERVER_ADDRESS = "152.173.154.202", 1234
PACKET_SIZE = 256
FPS = 60
CLOCK = pg.time.Clock()
RECT_SIZE = 40, 200
RECT_COLOR = 255, 255, 255
OPONENT_RECT_COLOR = 255, 0, 0
BACKGROUND_COLOR = 0, 0, 0
BALL_RADIUS = 50
BALL_COLOR = 0, 0, 255
LINE_COLOR = 0, 255, 0
TEXT_COLOR = 255, 255, 255

clientsocket = socket.socket()
clientsocket.connect(SERVER_ADDRESS)

# oponent_y_pos = 0
ball_pos = pg.Vector2(SIZE_WINDOW[0]/2, SIZE_WINDOW[1]/2)
rect = pg.Rect(0, 0, *RECT_SIZE)
points = 0
oponent_rect = pg.Rect(0, 0, *RECT_SIZE)
oponent_points = 0
end_thread = False

print("conectado al servidor, esperando oponente...")

pg.init()
pg.display.set_caption("Pongpy")
window = pg.display.set_mode(SIZE_WINDOW)
font = pg.font.SysFont("timesnewroman", 30)


while not (init_data := json.loads(clientsocket.recv(PACKET_SIZE))).get("status") == "OK":
    pass
rect = pg.Rect(init_data.get("rect"))

print("oponente conectado, partida iniciada")


def thread_recieve_data():
    global oponent_rect, ball_pos, BALL_RADIUS, points, oponent_points
    while not end_thread:
        try:
            data = json.loads(clientsocket.recv(PACKET_SIZE))
            oponent_rect = pg.Rect(*data.get("rect", oponent_rect))
            ball_pos = pg.Vector2(data.get("ball_pos", ball_pos))
            BALL_RADIUS = float(data.get("ball_radius", BALL_RADIUS))
            points = int(data.get("your_points", points))
            oponent_points = int(data.get("oponent_points", oponent_points))
        except json.JSONDecodeError:
            pass


threading.Thread(target=thread_recieve_data).start()

try:
    while True:
        window.fill(BACKGROUND_COLOR)
        for evento in pg.event.get():
            match evento.type:
                case pg.QUIT:
                    end_thread = True
                    pg.quit()
                    sys.exit()

        mouse_pos = pg.mouse.get_pos()
        rect.centery = mouse_pos[1]
        pg.draw.rect(window, RECT_COLOR, rect)
        pg.draw.rect(window, OPONENT_RECT_COLOR, oponent_rect)
        pg.draw.line(window, LINE_COLOR, window.get_rect().midtop,
                     window.get_rect().midbottom)
        pg.draw.circle(window, BALL_COLOR, ball_pos, BALL_RADIUS)
        po = font.render(f"Puntos oponente: {oponent_points}", False, TEXT_COLOR)
        window.blit(
            po,
            ((oponent_rect.centerx + 50)* 0.7, 10),
        )
        p = font.render(f"Puntos: {points}", False, TEXT_COLOR)
        window.blit(
            p,
            ((rect.centerx + 50) * 0.7, 10),
        )
        clientsocket.send(json.dumps({"rect": tuple(rect)}).encode())
        pg.display.update()
        CLOCK.tick(FPS)
except Exception as e:
    print(e)
finally:
    end_thread = True
