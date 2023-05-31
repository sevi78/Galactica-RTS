import pygame

if __name__ == '__main__':
    coords, koeff = [], 1
    with open('../../../../Galactica3.02_running/trash/points.txt', 'r', encoding='UTF8') as file:
        data = file.read().split(', ')
    for i in data:
        x, y = i[1:-1].split(';')
        print(x, y)
        x = float(x.replace(',', '.')) + 250
        y = float(y.replace(',', '.')) * -1 + 250
        coords.append([x, y])
    print(coords)
    pygame.init()
    pygame.display.set_caption('ZOOM')
    size = width, height = 501, 501
    screen, fps, running, clock = pygame.display.set_mode(size), 60, True, pygame.time.Clock()
    pygame.draw.polygon(screen, pygame.Color('white'), coords, 1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION or event.type == pygame.WINDOWLEAVE or \
                    event.type == pygame.WINDOWEXPOSED:
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                koeff = 1.4
            if event.type == pygame.MOUSEWHEEL:
                koeff = 0.9
            for elem in coords:
                elem[0], elem[1] = (elem[0] - 250) * koeff + 250, (elem[1] - 250) * koeff + 250
            screen.fill((0, 0, 0))
            pygame.draw.polygon(screen, pygame.Color('white'), coords, width=1)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()