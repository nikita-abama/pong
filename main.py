import random
import pygame
import os
import sys

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
flag = 1
pygame.time.set_timer(pygame.USEREVENT, 3000)
size = width, height = 1500, 800
screen = pygame.display.set_mode(size)
running = True
pygame.display.set_caption('ПИНИОНГ :)')
all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
balls = pygame.sprite.Group()
Guns_sprites = pygame.sprite.Group()
b_sprites = pygame.sprite.Group()
Guns = {0: (width // 3 + 50, 200, 2, 3), 1: (width // 3 * 2 - 50, 200, -3, 2),
        2: (width // 3 + 50, height - 200, 3, -2), 3: (width // 3 * 2 - 50, height - 200, -2, -3)}
the_final = False
players = 0
vector = (0, 0)
counter = [5, 5, 5, 5, True, True, True, True, True, True, True, True, True]
pygame.mixer.music.load('backontrack.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
boom = pygame.mixer.Sound('39dc0d7451e490f.mp3')
start = pygame.mixer.Sound('sfx-5.mp3')
death = pygame.mixer.Sound('b18c8bb56694a7b.mp3')
finish = pygame.mixer.Sound('e377e9b8d135e68.mp3')
player = []
live_players = [1, 2, 3, 4]
pause = False
n = 1
previous_gun = 1
flags = [False, False, False, False, True, True, True, True]
mapp = ''
chose_map = False
ballss = 1


class Player(pygame.sprite.Sprite):
    def __init__(self, group, life=True, ver=False, lev=False):
        super().__init__(group)
        self.move = None
        self.life = life
        self.ver = ver
        self.lev = lev
        self.rect_x = 5
        self.rect_y = 5
        super().__init__(all_sprites)
        if self.life:
            if self.lev:
                if self.ver:
                    self.image = pygame.transform.scale(load_image("nlo_down.png", fil='player'), (125, 75))
                    self.rect = self.image.get_rect(centerx=width // 6 + width // 3, bottom=height - 50)
                else:
                    self.image = pygame.transform.scale(load_image("nlo_left.png", fil='player'), (75, 125))
                    self.rect = self.image.get_rect(centerx=width // 3 - 25, bottom=height // 2 + 75)
            else:
                if self.ver:
                    self.image = pygame.transform.scale(load_image("nlo_up.png", fil='player'), (125, 75))
                    self.rect = self.image.get_rect(centerx=width // 6 + width // 3, bottom=150)
                else:
                    self.image = pygame.transform.scale(load_image("nlo_right.png", fil='player'), (75, 125))
                    self.rect = self.image.get_rect(centerx=width // 3 * 2 + 25, bottom=height // 2 + 75)
        else:
            if self.ver:
                pass

    def update(self, *args):
        global flags
        if self.lev and self.ver:
            if flags[4]:
                self.rect = self.rect.move(0, 0)
            elif flags[0]:
                self.rect = self.rect.move(self.rect_x, 0)
            elif not flags[0]:
                self.rect = self.rect.move(-self.rect_x, 0)
        if not self.lev and self.ver:
            if flags[5]:
                self.rect = self.rect.move(0, 0)
            elif flags[1]:
                self.rect = self.rect.move(-self.rect_x, 0)
            elif not flags[1]:
                self.rect = self.rect.move(self.rect_x, 0)
        if self.lev and not self.ver:
            if flags[6]:
                self.rect = self.rect.move(0, 0)
            elif flags[2]:
                self.rect = self.rect.move(0, self.rect_y)
            elif not flags[2]:
                self.rect = self.rect.move(0, -self.rect_y)
        if not self.lev and not self.ver:
            if flags[7]:
                self.rect = self.rect.move(0, 0)
            elif flags[3]:
                self.rect = self.rect.move(0, -self.rect_y)
            elif not flags[3]:
                self.rect = self.rect.move(0, self.rect_y)
        if pygame.sprite.spritecollideany(self, Guns_sprites):
            if self.lev and self.ver:
                if flags[0]:
                    self.rect = self.rect.move(-self.rect_x, 0)
                elif not flags[0]:
                    self.rect = self.rect.move(self.rect_x, 0)
            if not self.lev and self.ver:
                if flags[1]:
                    self.rect = self.rect.move(self.rect_x, 0)
                elif not flags[1]:
                    self.rect = self.rect.move(-self.rect_x, 0)
            if self.lev and not self.ver:
                if flags[2]:
                    self.rect = self.rect.move(0, -self.rect_y)
                elif not flags[2]:
                    self.rect = self.rect.move(0, self.rect_y)
            if not self.lev and not self.ver:
                if flags[3]:
                    self.rect = self.rect.move(0, self.rect_y)
                elif not flags[3]:
                    self.rect = self.rect.move(0, -self.rect_y)

    def is_life(self):
        if self.life:
            return True
        else:
            return False


def create_players(col):
    ver = True
    lev_ver = True
    lev_gor = True
    for i in range(4):
        if col != 0:
            if ver:
                if lev_ver:
                    player.append(Player(horizontal_borders, True, True, True))
                    lev_ver = False
                else:
                    player.append(Player(horizontal_borders, True, True, False))
                    ver = False
            else:
                if lev_gor:
                    player.append(Player(vertical_borders, True, False, True))
                    lev_gor = False
                else:
                    player.append(Player(vertical_borders, True, False, False))
            col -= 1


def load_image(name, fil=None, colorkey=None):
    fullname = os.path.join('sprite', name)
    if fil is not None:
        fullname = os.path.join('sprite', fil, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y, vx, vy):
        super().__init__(all_sprites)
        self.add(balls)
        self.x = x
        self.y = y
        self.radius = radius
        self.image = pygame.transform.scale(load_image(str(n) + '.png', fil='ball'), (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.vx = vx
        self.vy = vy

    def update(self, *args):
        global the_final, vector, n
        if n == 30:
            n = 1
        self.image = pygame.transform.scale(load_image(str(n + 1) + '.png', fil='ball'), (40, 40))
        n += 1
        if args[0]:
            if vector != (0, 0):
                x = self.vx
                y = self.vy
                self.vx = vector[0]
                self.vy = vector[1]
                vector = (x, y)
        if pygame.sprite.spritecollideany(self, b_sprites):
            if pygame.sprite.spritecollideany(self, horizontal_borders):
                self.vy = -self.vy
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.vx = -self.vx
            boom.play()
        elif pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.rect[0] in range(pygame.sprite.spritecollideany(self, horizontal_borders).rect[0],
                                     pygame.sprite.spritecollideany(self, horizontal_borders).rect[2] // 3 +
                                     pygame.sprite.spritecollideany(self, horizontal_borders).rect[0]):
                self.vx -= 1
                self.vy = -self.vy
            elif self.rect[0] in range(
                    pygame.sprite.spritecollideany(self, horizontal_borders).rect[2] // 3 +
                    pygame.sprite.spritecollideany(self, horizontal_borders).rect[0],
                    pygame.sprite.spritecollideany(self, horizontal_borders).rect[2] // 3 * 2 +
                    pygame.sprite.spritecollideany(self, horizontal_borders).rect[0]):
                self.vy = -self.vy
                self.rect = self.rect.move(self.vx // 1, self.vy // 1)
            elif self.rect[0] in range(pygame.sprite.spritecollideany(self, horizontal_borders).rect[2] // 3 * 2 +
                                       pygame.sprite.spritecollideany(self, horizontal_borders).rect[0],
                                       pygame.sprite.spritecollideany(self, horizontal_borders).rect[0] +
                                       pygame.sprite.spritecollideany(self, horizontal_borders).rect[2]):
                self.vx += 1
                self.vy = -self.vy
            elif self.rect[1] in range(pygame.sprite.spritecollideany(self, horizontal_borders).rect[1],
                                       pygame.sprite.spritecollideany(self, horizontal_borders).rect[3] +
                                       pygame.sprite.spritecollideany(self, horizontal_borders).rect[1]):
                self.vx = -self.vx
                self.vy = -self.vy
                self.rect = self.rect.move(self.vx // 0.5, self.vy // 1)
            boom.play()
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            if self.rect[1] in range(pygame.sprite.spritecollideany(self, vertical_borders).rect[1],
                                     pygame.sprite.spritecollideany(self, vertical_borders).rect[3] // 3 +
                                     pygame.sprite.spritecollideany(self, vertical_borders).rect[1]):
                self.vy -= 1
                self.vx = -self.vx
            elif self.rect[1] in range(pygame.sprite.spritecollideany(self, vertical_borders).rect[3] // 3 +
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[1],
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[3] // 3 * 2 +
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[1]):
                self.vx = -self.vx
            elif self.rect[1] in range(pygame.sprite.spritecollideany(self, vertical_borders).rect[3] // 3 * 2 +
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[1],
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[3]):
                self.vy += 1
                self.vx = -self.vx
                self.vx = -self.vx
            elif self.rect[0] in range(pygame.sprite.spritecollideany(self, vertical_borders).rect[0],
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[2] +
                                       pygame.sprite.spritecollideany(self, vertical_borders).rect[0]):
                self.vx = -self.vx
                self.vy = -self.vy
                self.rect = self.rect.move(self.vx // 0.75, self.vy // 0.5)
            boom.play()
        if pygame.sprite.spritecollideany(self, Guns_sprites):
            self.vx = -self.vx
            self.vy = -self.vy
            boom.play()
        if self.rect[1] >= 700:
            for i in balls:
                if i == self.rect:
                    counter[0] -= 1
                    i.kill()
        elif self.rect[1] <= 100:
            for i in balls:
                if i == self.rect:
                    counter[1] -= 1
                    i.kill()
        elif self.rect[0] <= width // 3 - 50:
            for i in balls:
                if i == self.rect:
                    counter[2] -= 1
                    i.kill()
        elif self.rect[0] >= width // 3 * 2 + 50:
            for i in balls:
                if i == self.rect:
                    counter[3] -= 1
                    i.kill()
        elif pygame.sprite.spritecollideany(self, balls) != self.rect:
            for i in balls:
                if i == pygame.sprite.spritecollideany(self, balls):
                    vector = (self.vx, self.vy)
                    i.update(True)
                    break
            if vector != (0, 0):
                self.vx = vector[0]
                self.vy = vector[1]
            vector = (0, 0)
        c = 0
        for i in enumerate(counter):
            if counter[i[0]] < 1:
                c += 1
                if counter[0] == 0 and counter[4]:
                    Killer(horizontal_borders, condition=0)
                    counter[4] = False
                    if not the_final:
                        live_players[0] = 0
                    Border(width // 3, width // 3 * 2, height - 125)
                    Killer(Guns_sprites)
                    gunsmith()
                    if counter[8]:
                        pass
                        Killer(horizontal_borders, 0)
                        death.play()
                if counter[1] == 0 and counter[5]:
                    Killer(horizontal_borders, condition=1)
                    counter[5] = False
                    if not the_final:
                        live_players[1] = 0
                    Border(width // 3, width // 3 * 2, 125)
                    Killer(Guns_sprites)
                    gunsmith()
                    if counter[9]:
                        pass
                        Killer(horizontal_borders, 1)
                        death.play()
                if counter[2] == 0 and counter[6]:
                    Killer(vertical_borders, condition=0)
                    counter[6] = False
                    if not the_final:
                        live_players[2] = 0
                    Border(width // 3, width // 3, height - 125)
                    Killer(Guns_sprites)
                    gunsmith()
                    if counter[10]:
                        pass
                        Killer(vertical_borders, 0)
                        death.play()
                if counter[3] == 0 and counter[7]:
                    Killer(vertical_borders, condition=1)
                    counter[7] = False
                    if not the_final:
                        live_players[3] = 0
                    Border(width // 3 * 2, width // 3 * 2, height - 125)
                    Killer(Guns_sprites)
                    gunsmith()
                    if counter[11]:
                        pass
                        Killer(vertical_borders, 1)
                        death.play()
                if c == 7 and not counter[10] and counter[12]:
                    finish.play()
                    the_final = True
                    counter[12] = False
                elif c == 6 and counter[11] and counter[12]:
                    finish.play()
                    the_final = True
                    counter[12] = False
                elif c == 6 and counter[10] and counter[12]:
                    finish.play()
                    the_final = True
                    counter[12] = False
        self.rect = self.rect.move(self.vx // 1, self.vy // 1)


def shoot():
    global previous_gun
    number_gun = random.randint(0, 3)
    if previous_gun == number_gun:
        shoot()
    else:
        Ball(20, Guns[number_gun][0], Guns[number_gun][1], Guns[number_gun][2], Guns[number_gun][3])
        previous_gun = number_gun


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, x2, y2):
        super().__init__(all_sprites)
        self.add(b_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            if x1 == width // 3:
                self.image = pygame.transform.rotate(pygame.transform.scale(load_image('stena.png'), (550, 20)), 270)
                self.rect = self.image.get_rect(centerx=x1 - 10, bottom=y2)
            else:
                self.image = pygame.transform.rotate(pygame.transform.scale(load_image('stena.png'), (550, 20)), 90)
                self.rect = self.image.get_rect(centerx=x1 - 1, bottom=y2)

        else:
            self.add(horizontal_borders)
            if x1 == width // 3:
                self.image = pygame.transform.rotate(pygame.transform.scale(load_image('stena.png'), (500, 20)), 0)
                self.rect = self.image.get_rect(centerx=x1 * 1.5, bottom=y2 + 5)
            else:
                self.image = pygame.transform.rotate(pygame.transform.scale(load_image('stena.png'), (500, 20)), 180)
                self.rect = self.image.get_rect(centerx=x1 * 1.5, bottom=y2)


class Killer:
    def __init__(self, group, condition=None):
        if condition is not None:
            for r, i in enumerate(group):
                if r == condition:
                    i.kill()
        else:
            for i in group:
                i.kill()


class Gun(pygame.sprite.Sprite):
    def __init__(self, radius, filename, x, y, number):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(all_sprites)
        self.add(Guns_sprites)
        self.x = x
        self.y = y
        self.radius = radius

        self.image = pygame.transform.rotate(pygame.transform.scale(load_image(filename), (50, 60)), 225 + 90 * number)
        self.rect = self.image.get_rect(center=(x, y))


clock = pygame.time.Clock()


def gunsmith():
    Gun(20, 'gun.png', width // 3 - 15, 110, 0)
    Gun(20, 'gun.png', width // 3 - 15, height - 140, 1)
    Gun(20, 'gun.png', width // 3 * 2 + 5, 110, 3)
    Gun(20, 'gun.png', width // 3 * 2 + 5, height - 140, 2)


def players2():
    global chose_map, players
    chose_map = True
    players = 2


def players3():
    global chose_map, players
    chose_map = True
    players = 3


def players4():
    global chose_map, players
    chose_map = True
    players = 4


def instruct():
    screen.blit(pygame.font.Font('moon_shrift.ttf', 25).render("ИНСТРУКЦИЯ:", True, (0, 200, 100)),
                (width // 3 + 200, 200))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("Пинпонг, это многопользовательская игра",
                                                          True, (0, 200, 100)), (width // 3 + 100, 240))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("в которой вы играете за инопланетян,"
                                                          "и должны отбивать огоньки которые вылетают из пушек",
                                                          True, (0, 200, 100)), (width // 4, 260))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("если вы пропустите огонек то у вас"
                                                          " сгорит одна жизнь,",
                                                          True, (0, 200, 100)), (width // 3 + 50, 280))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("всего у каждого игрока их 5,",
                                                          True, (0, 200, 100)), (width // 3 + 150, 300))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("у кого последнего кончятся жизни тот и выйграет",
                                                          True, (0, 200, 100)), (width // 3 + 50, 320))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("Управление:",
                                                          True, (0, 200, 100)), (width // 3 + 213, 340))
    screen.blit(pygame.font.Font('shrift.ttf', 25).render("1 игрок: z, 2 игрок: m,"
                                                          " 1 игрок: c, 1 игрок: b",
                                                          True, (0, 200, 100)), (width // 3 + 50, 360))
    screen.blit(pygame.font.Font('shrift.ttf', 50).render('ВЫБЕРИТЕ КОЛИЧЕСТВО ИГРОКОВ:',
                                                          True, (0, 200, 100)), (width // 3, 400))
    screen.blit(pygame.font.Font('shrift.ttf', 20).render('для комфортной игры рекомендуем выключить залипание клавиш',
                                                          True, (0, 200, 100)), (10, 700))


gunsmith()
a = random.randint(0, 3)
ff = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if flag == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and player[0].is_life:
                    flags[0] = not flags[0]
                    flags[4] = False
                elif event.key == pygame.K_m and player[1].is_life:
                    flags[1] = not flags[1]
                    flags[5] = False
                elif event.key == pygame.K_c and players > 2:
                    if player[2].is_life:
                        flags[2] = not flags[2]
                        flags[6] = False
                elif event.key == pygame.K_b and players > 3:
                    if player[3].is_life:
                        flags[3] = not flags[3]
                        flags[7] = False
                horizontal_borders.update()
                vertical_borders.update()

        if chose_map and flag != 1 and flag != 2:
            screen.fill('black')
            screen.blit(pygame.transform.scale(load_image('fon.png', fil='maps'), (300, 250)),
                        (400, 300))
            screen.blit(pygame.transform.scale(load_image('fon_2.jpg', fil='maps'), (300, 250)),
                        (1000, 300))
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONUP and 400 <= event.pos[0] <= 700 and 250 \
                    <= event.pos[1] <= 550:
                mapp = 'fon.png'
                chose_map = False
                if players == 2:
                    counter = [5, 5, 0, 0, True, True, True, True, True, True, False, False, True]
                if players == 3:
                    counter = [5, 5, 5, 0, True, True, True, True, True, True, True, False, True]
                if players == 4:
                    counter = [5, 5, 5, 5, True, True, True, True, True, True, True, True, True]
                Killer(balls)
                Ball(20, Guns[a][0], Guns[a][1], Guns[a][2], Guns[a][3])
                flag = 2
                start.play()
                create_players(players)

            elif event.type == pygame.MOUSEBUTTONUP and 1000 <= event.pos[0] <= 1400 and 250 \
                    <= event.pos[1] <= 550:
                mapp = 'fon_2.jpg'
                chose_map = False
                if players == 2:
                    counter = [5, 5, 0, 0, True, True, True, True, True, True, False, False, True]
                if players == 3:
                    counter = [5, 5, 5, 0, True, True, True, True, True, True, True, False, True]
                if players == 4:
                    counter = [5, 5, 5, 5, True, True, True, True, True, True, True, True, True]
                Killer(balls)
                Ball(20, Guns[a][0], Guns[a][1], Guns[a][2], Guns[a][3])
                flag = 2
                start.play()
                create_players(players)

        if pause:
            screen.fill('black')
            while 1:
                event = pygame.event.wait()
                if event.type == pygame.MOUSEBUTTONUP and width // 4 - 270 <= event.pos[0] <= width // 4 and 330\
                        <= event.pos[1] <= 470:
                    live_players = [1, 2, 3, 4]
                    flag = 1
                    the_final = False
                    pause = False
                    chose_map = False
                    flags = [False, False, False, False, True, True, True, True]
                    Killer(all_sprites)
                    ballss = 1
                    gunsmith()
                    break

                elif event.type == pygame.MOUSEBUTTONUP and width // 4 + 195 <= event.pos[0] <= width // 4 + 535\
                        and 315 <= event.pos[1] <= 465:
                    pause = False
                    break

                elif event.type == pygame.MOUSEBUTTONUP and width // 3 + 615 <= event.pos[0] <= width // 3 + 885\
                        and 325 <= event.pos[1] <= 465:
                    live_players = [1, 2, 3, 4]
                    flag = False
                    the_final = False
                    pause = False
                    flags = [False, False, False, False, True, True, True, True]
                    chose_map = True
                    Killer(all_sprites)
                    ballss = 1
                    create_players(players)
                    gunsmith()
                    break

        if the_final:
            Killer(all_sprites)
            flag = False
            screen.blit(load_image(mapp, fil='maps'), (0, 0))
            screen.blit(pygame.font.Font('shrift.ttf', 150).render(f"ПОБЕДИЛ ИГРОК НОМЕР {sum(live_players)}",
                                                                   True, (250, 100, 100)), (0, 100))
            screen.blit(pygame.transform.scale(load_image('restart.png', fil='buttons'),
                                               (300, 180)), (width // 3 + 300, 310))
            screen.blit(pygame.transform.scale(load_image('home.png', fil='buttons'),
                                               (340, 200)), (width // 4, 300))
            sd = open('max_balls.txt', 'r')
            if ballss == int(sd.read()):
                screen.blit(pygame.font.Font('shrift.ttf', 50).render("Поздравляем вы побили свой рекорд!!!!!",
                                                                      True, (250, 100, 100)), (350, 500))
            else:
                screen.blit(pygame.font.Font('shrift.ttf', 50).render(f"К сожелению в этот раз вы не побили свой"
                                                                      f" рекорд(", True, (250, 100, 100)), (300, 500))
            sd.seek(0, 0)
            screen.blit(pygame.font.Font('shrift.ttf', 50).render("Ваш рекорд: " + sd.read(),
                                                                  True, (250, 100, 100)), (600, 600))
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONUP and width // 4 + 20 <= event.pos[0] <= width // 4 + 300 and 300 <= \
                    event.pos[1] <= 500:
                live_players = [1, 2, 3, 4]
                flag = 1
                flags = [False, False, False, False, True, True, True, True]
                ballss = 1
                counter = [5, 5, 5, 5, True, True, True, True, True, True, True, True, True]
                the_final = False
                Killer(all_sprites)
                gunsmith()

            if event.type == pygame.MOUSEBUTTONUP and width // 3 + 320 <= event.pos[0] <= width // 3 + 580 and 180 <= \
                    event.pos[1] <= 490:
                live_players = [1, 2, 3, 4]
                flag = False
                the_final = False
                pause = False
                ballss = 1
                flags = [False, False, False, False, True, True, True, True]
                counter = [5, 5, 5, 5, True, True, True, True, True, True, True, True, True]
                chose_map = True
                Killer(all_sprites)
                create_players(players)
                gunsmith()

        if event.type == pygame.USEREVENT and not the_final:
            shoot()
            ballss += 1

        if flag == 1:
            if event.type == pygame.MOUSEBUTTONUP and width // 3 + 230 <= event.pos[0] <= width // 3 + 330 and 500 <= \
                    event.pos[1] <= 650:
                flag = False
                players3()

            if event.type == pygame.MOUSEBUTTONUP and width // 4 + 50 <= event.pos[0] <= width // 4 + 150 and 500 <= \
                    event.pos[1] <= 650:
                players2()
                flag = False

            if event.type == pygame.MOUSEBUTTONUP and (width // 3 + 530 <= event.pos[0] <= width // 3 + 630) and 500\
                    <= event.pos[1] <= 650:
                players4()
                flag = False

            screen.fill('black')
            screen.blit(pygame.font.Font('shrift.ttf', 150).render("ПИНПОНГ", True, (250, 100, 255)),
                        (width // 3, 50))
            instruct()
            pygame.draw.rect(screen, (0, 0, 0), (width // 3 + 50, 450, 100, 100))
            pygame.draw.rect(screen, (0, 0, 0), (width // 3 + 250, 450, 100, 100))
            pygame.draw.rect(screen, (0, 0, 0), (width // 3 + 450, 450, 100, 100))
            screen.blit(pygame.transform.scale(load_image('2.png', fil='number'), (100, 150)),
                        (width // 4 + 50, 500))
            screen.blit(pygame.transform.scale(load_image('3.png', fil='number'), (100, 150)),
                        (width // 3 + 230, 500))
            screen.blit(pygame.transform.scale(load_image('4.png', fil='number'), (100, 150)),
                        (width // 3 + 530, 500))
            pygame.display.flip()
            Killer(balls)
            Ball(20, Guns[a][0], Guns[a][1], Guns[a][2], Guns[a][3])
        if flag == 2:
            if event.type == pygame.MOUSEBUTTONUP and 100 <= event.pos[0] <= 150 and 400 <= event.pos[1] <= 450:
                pause = True
    if flag == 2:
        screen.blit(load_image(mapp, fil='maps'), (0, 0))
        all_sprites.draw(screen)
        all_sprites.update(False)
        screen.blit(pygame.font.Font(None, 100).render(str(counter[0]), True, (255, 255, 255)),
                    (width // 3 - 50, height - 100))
        screen.blit(pygame.font.Font(None, 100).render(str(counter[1]), True, (0, 0, 255)),
                    (width - width // 3 - 20, 20))
        screen.blit(pygame.font.Font(None, 100).render(str(counter[2]), True, (255, 0, 0)),
                    (width // 3 - 90, height // 5 - 100))
        screen.blit(pygame.font.Font(None, 100).render(str(counter[3]), True, (0, 200, 100)),
                    (width // 3 * 2 + 50, height // 2 + 230))
        screen.blit(pygame.transform.scale(load_image('pause.jpg', fil='buttons'), (50, 50)), (100, 400))
        sd = open('max_balls.txt', 'r')
        screen.blit(pygame.font.Font('shrift.ttf', 100).render("Рекорд: " + sd.read(), True, (250, 100, 255)),
                    (100, 300))
        screen.blit(pygame.font.Font('shrift.ttf', 100).render("Счет: " + str(ballss), True, (250, 100, 255)),
                    (1100, 500))
        sd.seek(0, 0)
        if int(sd.read()) < ballss:
            with open('max_balls.txt', 'r') as sd:
                old_data = sd.read()

            new_data = old_data.replace(old_data, str(ballss))

            with open('max_balls.txt', 'w') as sd:
                sd.write(new_data)
        if pause:
            screen.fill('black')
            screen.blit(pygame.transform.scale(load_image('home.png', fil='buttons'),
                                               (340, 200)), (width // 4 - 300, 300))
            screen.blit(pygame.transform.scale(load_image('continue.png', fil='buttons'),
                                               (340, 150)), (width // 4 + 200, 320))
            screen.blit(pygame.transform.scale(load_image('restart.png', fil='buttons'),
                                               (300, 180)), (width // 3 + 600, 310))
            pygame.display.flip()
        pygame.display.flip()
        clock.tick(70)
        