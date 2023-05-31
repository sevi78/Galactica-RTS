import pygame as pg
from pygame.math import Vector2


class Planet(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((40, 40), pg.SRCALPHA)
        pg.draw.circle(self.image, pg.Color('dodgerblue'), (20, 20), 20)
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)
        self.offset = Vector2(200, 0)
        self.angle = 0

    def orbit(self):
        self.angle -= 2
        # Add the rotated offset vector to the pos vector to get the rect.center.
        self.rect.center = self.pos + self.offset.rotate(self.angle)

    def update(self):
        self.angle -= 2
        # Add the rotated offset vector to the pos vector to get the rect.center.
        self.rect.center = self.pos + self.offset.rotate(self.angle)


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    screen_rect = screen.get_rect()
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    planet = Planet(screen_rect.center, all_sprites)
    yellow = pg.Color('yellow')

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        all_sprites.update()
        screen.fill((30, 30, 30))
        pg.draw.circle(screen, yellow, screen_rect.center, 60)
        all_sprites.draw(screen)

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()