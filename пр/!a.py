import pygame
import os
import sys

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
           image.set_colorkey('white')
        image.set_colorkey(colorkey)
    else:
        image = image
    return image

tile_images = {'wall': load_image('6.png'),
               'empty': load_image('7.png'),
               'podarok': load_image('11.png'),
               'coin': load_image('coin.png')}

player_image = load_image('8.png', -1)

tile_width = tile_height = 50

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y

    def move(self, x, y):
        global kol
        global level
        nx = x // 50 + self.x
        ny = y // 50 + self.y
        nx = (nx + level_x) % level_x
        ny = (ny + level_y) % level_y
        if not(-1 < nx < level_x and -1 < ny < level_y):
            return
        if level[ny][nx] != '#':
            self.rect = self.rect.move((nx-self.x)*50,
                                       (ny-self.y)*50)
            self.x = nx
            self.y = ny
            if level[ny][nx] == '*':
                kol += 1
                #level[ny][nx] = '.'
            if level[ny][nx] == '0':
                winer_screen()
            

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        
    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
    
    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
           
def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Для победы возьми монету.",
                  "Не попадайся врагам."]

    fon = pygame.transform.scale(load_image('9.png'), (width, width))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        
def winer_screen():
    intro_text = ["Победа!"]

    fon = pygame.transform.scale(load_image('9.png'), (width, width))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(50)

    
        
def loser_screen():
    intro_text = ['Game over']

    fon = pygame.transform.scale(load_image('9.png'), (width, width))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(50)

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
   
    max_width = max(map(len, level_map))
    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

def generate_level(level):
    new_player, x, y = None, None, None
    px = None
    py = None
    vr = [[-1,-1], [0,-1], [1,-1], [-1,0], [0,0], [1,0],
          [-1,1], [0,1], [1,1]]
    list_tiles = []
    for i in vr:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.' or (level[y][x] == '@'
                                          and i != [0,0]):
                    Tile('empty', x + i[0] * (len(level) - 1),
                         y + i[1] * (len(level[y]) - 1))
                elif level[y][x] == '#':
                    Tile('wall', x + i[0] * (len(level) - 1),
                         y + i[1] * (len(level[y]) - 1))
                elif level[y][x] == '*':
                    Tile('podarok', x + i[0] * (len(level) - 1),
                         y + i[1] * (len(level[y]) - 1))
                elif level[y][x] == '0':
                    Tile('coin', x + i[0] * (len(level) - 1),
                         y + i[1] * (len(level[y]) - 1))
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    px = x
                    py = y
    new_P = Player(px, py)
    return new_P, x, y

player = None
camera = Camera()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()
level = load_level(input('Название уровня => '))
player, level_x, level_y = generate_level(level)
running = True
fps = 50
all_sprites.draw(screen)
kol = 0
f = 0
while running:
    if kol == 1 and f == 0:
        loser_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if player.rect.x > 50:
                    player.move(-50, 0)
            elif event.key == pygame.K_RIGHT:
                if player.rect.x < width - 50:
                    player.move(50, 0)
            elif event.key == pygame.K_UP:
                if player.rect.y > 50:
                    player.move(0, -50)
            elif event.key == pygame.K_DOWN:
                if player.rect.y < height - 50:
                    player.move(0, 50)
    camera.update(player); 
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((0,0,0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()


