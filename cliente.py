import pygame as pg

SIZE = (1000, 1000)
CLOCK = pg.time.Clock()
FPS = 60

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