import pygame
from random import randint
from math import sqrt

pygame.init()

screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Navezinha")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 40, True, False)
running = True

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.2)
list_proj = []
list_enemy = []
list_stars = []
list_hearts = []
speed_proj = 600
speed_player = 400
speed_enemy = 100
speed_stars = 700
speed_drop = 200
raio_proj = 5
raio_player = 30
raio_enemy = 20
raio_stars = 1
raio_heart = 8

delay_proj = 0
delay_reload = 0

life = [5]
level = [1]
xp = [0]
max_xp = screen.get_width() - 60
up_xp = [20]
reload_proj = 5
diff = 80
drop_heart = 0

cont_frame = 0
dt = 0

def proj():
    list_proj.append(pygame.Vector2(player_pos.x, player_pos.y))

def movProj():
    for i in list_proj:
        pygame.draw.circle(screen, (173, 216, 230), i, raio_proj)
        i.y -= speed_proj * dt

        if i.y < screen.get_height() / 8:
            list_proj.remove(i)

def enemy():
    list_enemy.append(pygame.Vector2(randint(raio_enemy, screen.get_width() - raio_enemy), -raio_enemy))

def movEnemy():
    for i in list_enemy:
        pygame.draw.circle(screen, (10, 10, 10), i, raio_enemy)

        nave = Sprites(i.x, i.y, 3, "navezinha.png")
        enemys.add(nave)

        i.y += speed_enemy * dt

        if i.y > screen.get_height() + raio_enemy:
            list_enemy.remove(i)
            life[0] -= 1

        for j in list_proj:
            if sqrt((j.y - i.y) ** 2) < raio_enemy + raio_proj and sqrt((j.x - i.x) ** 2) < raio_enemy + raio_proj:
                if randint(1, 100) <= 7:
                    hearts(i.x, i.y)
                list_enemy.remove(i)
                list_proj.remove(j)
                upLevel()

def stars():
    list_stars.append(pygame.Vector2(randint(0, screen.get_width()), -1))

def movStars():
    for i in list_stars:
        pygame.draw.circle(screen, "white", (i.x, i.y), raio_stars)
        i.y += speed_stars * dt

def hearts(x, y):
    list_hearts.append(pygame.Vector2(x, y))

def movHearts():
    for i in list_hearts:
        pygame.draw.circle(screen, (10, 10, 10), (i.x, i.y), raio_heart)

        heart = Sprites(i.x, i.y, 8, "coracao.png")
        drops.add(heart)

        i.y += speed_drop * dt

        if i.y > screen.get_height() + raio_heart:
            list_hearts.remove(i)
        if (sqrt((i.y - player_pos.y) ** 2)) < raio_player + raio_heart and (sqrt((i.x - player_pos.x) ** 2)) < raio_player + raio_heart:
            list_hearts.remove(i)
            if life[0] < 5:
                life[0] += 1

def upLevel():

    xp[0] += max_xp / up_xp[0]

    if xp[0] >= max_xp:
        xp[0] = 0
        level[0] += 1
        up_xp[0] *= 2

class Sprites(pygame.sprite.Sprite):

    def __init__ (self, x, y, r, i):
        pygame.sprite.Sprite.__init__ (self)

        self.image = pygame.image.load(i)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / r, self.image.get_height() / r))

        keys = pygame.key.get_pressed()
        if i == "player.png" and keys[pygame.K_LEFT]:
            self.image = pygame.transform.rotate(self.image, 3)
        if i == "player.png" and keys[pygame.K_RIGHT]:
            self.image = pygame.transform.rotate(self.image, 357)

        self.rect = self.image.get_rect()
        self.rect.topleft = x - self.image.get_width() // 2, y - self.image.get_height() // 2

while running:
    enemys = pygame.sprite.Group()
    drops = pygame.sprite.Group()
    players = pygame.sprite.Group()

    text_level = f'{level[0]}'
    text_level = font.render(text_level, True, 'white')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if life[0] == 0:
        running = False

    screen.fill((0, 0, 10))

    cont_frame += 1
    if cont_frame % 3 == 0 or cont_frame == 1:
        stars()
    
    movStars()

    if cont_frame % round(diff) == 0 or cont_frame == 1:
        enemy()
        diff -= 0.1

    movEnemy()

    movProj()

    movHearts()

    pygame.draw.circle(screen, (10, 10, 10), player_pos, raio_player)
    player = Sprites(player_pos.x, player_pos.y, 10, "player.png")
    players.add(player)

    players.draw(screen)
    players.update()
    enemys.draw(screen)
    enemys.update()
    drops.draw(screen)
    drops.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos.x >= raio_player:
        player_pos.x -= speed_player * dt
    if keys[pygame.K_RIGHT] and player_pos.x + raio_player <= screen.get_width():
        player_pos.x += speed_player * dt

    if keys[pygame.K_UP] and delay_proj == 0 and reload_proj > 0:
        proj()
        delay_proj += 1
        reload_proj -= 1
        delay_reload = 0
    elif not keys[pygame.K_UP] and reload_proj < 5 and delay_reload == 40:
        reload_proj += 1

    delay_reload += 1

    if delay_reload > 40:
        delay_reload = 0

    if delay_proj > 0:
        delay_proj += 1

        if delay_proj == 10:
            delay_proj = 0

    pygame.draw.rect(screen, (255, 192, 203), ((30, 10), (xp[0], 2)))

    pygame.draw.rect(screen, (50, 0, 0), ((30, 25), (300, 20)))
    pygame.draw.rect(screen, (100, 0, 0), ((30, 25), (life[0] * 60, 20)))

    pygame.draw.rect(screen, (173, 216, 230), ((30, 50), (reload_proj * 60, 5)))

    screen.blit(text_level, (screen.get_width() / 3 - 15, 18))
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
