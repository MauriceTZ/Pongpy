import socket
import pygame as pg
import threading
import json
import time
import random
import math

SIZE_WINDOW = 900, 900
SERVER_ADDRESS = "", 1234
PACKET_SIZE = 256
FPS = 60
CLOCK = pg.time.Clock()
RECT_SIZE = 40, 200
BALL_RADIUS = 50
BALL_INITIAL_VELOCITY_MAGNITUDE = 300
WINDOW_RECT = pg.Rect(0, 0, *SIZE_WINDOW)

serversocket = socket.socket()
serversocket.bind(SERVER_ADDRESS)
serversocket.listen()

end_thread = False

print("esperando jugadores...")


class Cliente:
    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket
        self.rect = pg.Rect(0, 0, *RECT_SIZE)
        self.points = 0


class Ball:
    def __init__(self) -> None:
        self.position = pg.Vector2(SIZE_WINDOW[0]/2, SIZE_WINDOW[1]/2)
        angle = math.radians(random.randint(25, 70))
        self.velocity = pg.Vector2(
            math.sin(angle), math.cos(angle)) * BALL_INITIAL_VELOCITY_MAGNITUDE
        self.rect = pg.Rect(0, 0, BALL_RADIUS*2, BALL_RADIUS*2)
        self.rect.center = self.position


clientes: list[Cliente] = []
ball = Ball()

# Esperar a los clientes
for i in range(2):
    socketclient, _ = serversocket.accept()
    clientes.append(Cliente(socketclient))
    print(f"jugador {i} conectado: {socketclient}")

clientes[1].rect.right = WINDOW_RECT.right


def thread_client_recieve(cliente: Cliente):
    while not end_thread:
        try:
            for packet in cliente.socket.recv(PACKET_SIZE).decode().split("\n"):
                data = json.loads(packet)
                cliente.rect.top = pg.Rect(data.get("rect", cliente.rect)).top
        except json.JSONDecodeError:
            pass


def cambio_random():
    global BALL_RADIUS
    if random.randint(0, 30) == 15:
        ball.velocity *= 0.80
        BALL_RADIUS *= 0.70


print("partida iniciada")

try:
    clientes[0].socket.send(json.dumps(
        {"status": "OK", "rect": tuple(clientes[0].rect)}).encode())
    threading.Thread(target=thread_client_recieve, args=(clientes[0],)).start()

    clientes[1].socket.send(json.dumps(
        {"status": "OK", "rect": tuple(clientes[1].rect)}).encode())
    threading.Thread(target=thread_client_recieve, args=(clientes[1],)).start()

    time.sleep(1)
    # es para que la bola no salga a la chucha al inicio (el get_time() toma el tiempo entre
    # las dos ultimas llamadas de tick(FPS))
    CLOCK.tick(FPS)
    CLOCK.tick(FPS)
    while True:
        ball.rect.center = ball.position
        ball.rect.size = 2 * BALL_RADIUS, 2 * BALL_RADIUS

        if ball.rect.left <= WINDOW_RECT.left or ball.rect.right >= WINDOW_RECT.right:
            ball.velocity.x *= -1
            if ball.rect.left <= WINDOW_RECT.left:
                clientes[1].points += 1
            else:
                clientes[0].points += 1

        if ball.rect.top <= WINDOW_RECT.top or ball.rect.bottom >= WINDOW_RECT.bottom:
            ball.velocity.y *= -1

        ball.rect = ball.rect.clamp(WINDOW_RECT)

        if ball.rect.colliderect(clientes[0].rect):
            ball.velocity.x = abs(ball.velocity.x)
            ball.velocity.x += 15
            ball.velocity.y += random.choice((-100, 100))
            cambio_random()

        if ball.rect.colliderect(clientes[1].rect):
            ball.velocity.x = -abs(ball.velocity.x)
            ball.velocity.x -= 15
            ball.velocity.y += random.choice((-100, 100))
            cambio_random()

        ball.position += ball.velocity * CLOCK.get_time() * 0.001

        clientes[0].socket.send((json.dumps({"rect": tuple(clientes[1].rect),
                                            "ball_pos": tuple(ball.position),
                                            "ball_radius": BALL_RADIUS,
                                            "your_points": clientes[0].points,
                                            "oponent_points": clientes[1].points}) + "\n").encode())
        clientes[1].socket.send((json.dumps({"rect": tuple(clientes[0].rect),
                                            "ball_pos": tuple(ball.position),
                                            "ball_radius": BALL_RADIUS,
                                            "your_points": clientes[1].points,
                                            "oponent_points": clientes[0].points}) + "\n").encode())
        CLOCK.tick(FPS)
except Exception as e:
    print(e)
finally:
    end_thread = True
