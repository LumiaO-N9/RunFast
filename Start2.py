import pygame
import pygame.locals as locals
import random


def load_img(path):
    return pygame.image.load(path)


class Background(object):
    def __init__(self):
        self.img = load_img("./background.png")
        self.x1 = 0
        self.x2 = Background_WIDTH
        self.speed = bg_sp_speed
        self.first_flag = True

    def update(self):
        if self.x1 <= -Background_WIDTH:
            self.x1 = Background_WIDTH
        if self.x2 <= -Background_WIDTH:
            self.x2 = Background_WIDTH
        if not self.first_flag:
            self.x1 -= self.speed
            self.x2 -= self.speed
        self.first_flag = False

    def display(self):
        surface.blit(self.img, (self.x1, 0))
        surface.blit(self.img, (self.x2, 0))


class GameObject(object):
    def __init__(self):
        self.img = None
        self.width = None
        self.height = None
        self.x = None
        self.y = None
        self.is_alive = True

    def set_img(self, img_path):
        self.img = load_img(img_path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def update(self):
        pass

    def display(self):
        surface.blit(self.img,
                     (self.x - self.width / 2, self.y - self.height / 2))

    def isCrash(self, other):
        if abs(self.x - other.x) < self.width / 2 + other.width / 2 and abs(
                self.y - other.y) < self.height / 2 + other.height / 2:
            return True
        return False


class Player(GameObject):
    def __init__(self):
        super().__init__()
        super().set_img("./trem/run1.png")
        self.img1 = pygame.image.load("./shield.png")
        self.x = INIT_X_P
        self.y = INIT_Y_P
        self.move_index = 0
        self.move_img = []
        self.jump_index = 0
        self.jump_img = pygame.image.load('./trem/jump2.png')
        self.jump_speed = [i for i in range(1, 22)]
        self.speed_index = 0
        self.attribute1 = None
        self.attribute2 = None
        self.dan = 0
        self.time = 0
        self.down_flag = False
        self.backward_flag = False
        self.forward_flag = False
        for i in range(1, 13):
            self.move_img.append(load_img('./trem/run%d.png' % i))

    def getdun(self, other):
        self.attribute1 = other.attribute
        self.time = other.time

    def getgun(self, other):
        self.attribute2 = other.attribute
        self.dan += other.dan

    def isCrash(self, other):
        if abs(self.x -
               other.x) + 80 < self.width / 2 + other.width / 2 and abs(
                   self.y - other.y) < self.height / 2 + other.height / 2:
            return True
        return False

    def backward(self, b_speed):
        self.backward_flag = True
        self.forward_flag = False
        # self.forward_flag = False
        self.speed = b_speed
        self.x -= self.speed

    def forward(self):
        self.backward_flag = False
        self.forward_flag = True
        # self.forward_flag = False
        self.x += self.speed

    def jump(self):
        global is_jump
        if self.y > INIT_Y_P - 220 and not self.down_flag:
            self.y -= 21 - self.jump_speed[self.speed_index]
            self.img = self.jump_img
            self.speed_index += 1
        if self.speed_index == 20:
            self.down_flag = True
            self.speed_index = 0
        if self.down_flag and self.y < INIT_Y_P:
            self.y += self.jump_speed[self.speed_index]
            self.speed_index += 1
        if self.y >= INIT_Y_P:
            self.speed_index = 0
            self.down_flag = False
            is_jump = False
        for wal in barricades:
            if self.y + self.height / 2 >= wal.y - wal.height / 2 \
                    and self.x >= wal.x - wal.width / 2 and self.x <= wal.x + wal.width / 2:
                self.speed_index = 0
                self.y = wal.y - wal.height / 2
                self.down_flag = False
                is_jump = False

    def fire(self):
        if self.attribute2 == 2 and self.dan > 0:  # 判断是否有枪
            self.dan -= 1
            bullet = Bullet(self.x + self.width / 2, self.y, 5, 10)
            bullet.set_img("./bullet.png")
            player_bullets.append(bullet)

    def update(self):
        global is_jump
        if is_jump:
            self.jump()
            if self.backward_flag:
                self.forward_flag = True
                self.backward_flag = False
        else:
            if self.backward_flag and not self.forward_flag:
                self.backward(self.speed)
            elif self.forward_flag and not self.backward_flag:
                self.forward()
                if self.x >= INIT_X_P:
                    self.x = INIT_X_P
                    self.forward_flag = False
                    self.backward_flag = False
            self.y = INIT_Y_P
            if self.move_index >= len(self.move_img):
                self.move_index = 0
            self.img = self.move_img[self.move_index]
            if game_count % 2 == 0:
                self.move_index += 1

    def display(self):
        if self.time > 0:
            surface.blit(self.img1,
                         (self.x - self.width, self.y - self.height))
        super(Player, self).display()


class Bullet(GameObject):
    def __init__(self, x, y, x_speed, damage):
        super().__init__()
        self.x_speed = x_speed
        self.x = x
        self.y = y
        self.damage = damage

    def update(self):
        self.x += self.x_speed
        if (self.x - self.width / 2) > SURFACE_WIDTH:
            self.is_alive = False

    def display(self):
        if self.is_alive:
            super().display()
        else:
            self.x_speed = 0


class Provide(GameObject):
    def __init__(self):
        super().__init__()
        self.x = SURFACE_WIDTH
        self.y = None
        self.attribute = None

    def update(self):
        if self.is_alive:
            self.x -= bg_sp_speed
        if self.x + self.width / 2 <= 0:
            self.is_alive = False


class HUDUN(Provide):
    def __init__(self):
        super().__init__()
        super().set_img('./dun.png')
        self.attribute = 1
        self.time = 2
        self.y = 150

    def update(self):
        if self.is_alive:
            self.x -= bg_sp_speed
        if self.x + self.width / 2 <= 0:
            self.is_alive = False


class GUN(Provide):
    def __init__(self):
        super().__init__()
        super().set_img('./gun.png')
        self.attribute = 2
        self.dan = 3
        self.y = 200

    def update(self):
        if self.is_alive:
            self.x -= bg_sp_speed
        if self.x + self.width / 2 <= 0:
            self.is_alive = False


class Ninja(GameObject):
    def __init__(self):
        super().__init__()
        super().set_img("./Ninja/Ninja1.png")
        self.x = INIT_X_N
        self.y = INIT_Y_N
        self.move_index = 0
        self.move_img = []
        self.forward_flag = False
        self.backward_flag = False
        for i in range(1, 9):
            self.move_img.append(load_img('./Ninja/Ninja%d.png' % i))

    def forward(self):
        self.old_x = self.x
        self.forward_flag = True
        self.backward_flag = False
        self.speed = 3

    def backward(self):
        self.old_x = self.x
        self.backward_flag = True
        self.forward_flag = False
        self.speed = -3

    def update(self):
        if self.forward_flag:
            if self.x - self.old_x <= 200:
                self.x += self.speed
            else:
                self.forward_flag = False

        if self.backward_flag:
            if self.old_x - self.x <= 100:
                self.x += self.speed
            else:
                self.backward_flag = False

        if self.x <= INIT_X_N:
            self.x = INIT_X_N

        if self.move_index >= len(self.move_img):
            self.move_index = 0
        self.img = self.move_img[self.move_index]
        if game_count % 4 == 0:
            self.move_index += 1


class Sprite(GameObject):
    def __init__(self):
        super().__init__()
        super().set_img("./Sprite/sprite1.png")
        self.x = INIT_X_S
        self.y = INIT_Y_S
        self.speed = bg_sp_speed
        self.move_index = 0
        self.move_img = []
        self.life = 20
        for i in range(1, 9):
            self.move_img.append(load_img('./Sprite/sprite%d.png' % i))
        self.boom_index = 0
        self.boom_img = []
        for i in range(1, 7):
            self.boom_img.append(load_img('./boom/boom_%d.png' % i))

    def hurt(self, bullet):
        self.life -= bullet.damage

    def isCrash(self, other):
        if abs(self.x -
               other.x) + 80 < self.width / 2 + other.width / 2 and abs(
                   self.y - other.y) < self.height / 2 + other.height / 2:
            return True
        return False

    def update(self):
        if self.life > 0:
            self.x -= self.speed
            if self.x <= 0:
                self.is_alive = False
            if self.move_index >= len(self.move_img):
                self.move_index = 0
            self.img = self.move_img[self.move_index]
            if game_count % 4 == 0:
                self.move_index += 1
        else:
            self.x -= self.speed
            self.y = INIT_Y_S + 20
            if self.boom_index >= len(self.boom_img):
                self.is_alive = False
                self.boom_index = len(self.boom_img) - 1
            self.img = self.boom_img[self.boom_index]
            if game_count % 10 == 0:
                self.boom_index += 1


class Heart(GameObject):
    def __init__(self):
        super().__init__()
        super().set_img("./heart.png")
        self.x = INIT_X_S
        self.y = INIT_Y_S - 150
        self.speed = bg_sp_speed

    def update(self):
        self.x -= self.speed
        if self.x <= 0:
            self.is_alive = False


class Barricade(GameObject):
    def __init__(self):
        super().__init__()
        rand = random.randint(1, 4)
        super().set_img("./Barricade/barricade%d.png" % rand)
        self.x = INIT_X_S
        self.y = INIT_Y_S
        self.life = 1
        self.speed = bg_sp_speed
        self.boom_img = []
        self.boom_index = 0
        for i in range(1, 7):
            self.boom_img.append(load_img('./boom/boom_%d.png' % i))

    def update(self):
        if self.life > 0:
            self.x -= self.speed
            if self.x <= 0:
                self.is_alive = False
        else:
            self.x -= self.speed
            if self.boom_index >= len(self.boom_img):
                self.is_alive = False
                self.boom_index = len(self.boom_img) - 1
            self.img = self.boom_img[self.boom_index]
            if game_count % 5 == 0:
                self.boom_index += 1


def player_bullet_crash_enemy():
    global game_score
    for p_b in player_bullets:
        for sprite in sprites:
            if p_b.isCrash(sprite) and sprite.life > 0:
                if sprite.life > p_b.damage:  # 剩余生命值大于子弹威力
                    sprite.hurt(p_b)
                else:
                    game_score += random.randint(200, 250)
                    sprite.life = 0  # 剩余生命值小于或等于子弹威力
                p_b.is_alive = False


def player_bullet_crash_barricade():
    for p_b in player_bullets:
        for barricade in barricades:
            if p_b.isCrash(barricade):
                p_b.is_alive = False


def player_get_reward():
    for rd in guns:
        if rd.isCrash(player):
            if rd.is_alive:
                player.getgun(rd)
                rd.is_alive = False
    for rw in duns:
        if rw.isCrash(player):
            if rw.is_alive:
                player.getdun(rw)
                rw.is_alive = False


def player_crash_sprite():
    global game_score
    for sprite in sprites:
        if player.isCrash(sprite):
            # sprite.is_alive = False
            if sprite.life > 0 and player.time > 0:
                sprite.life = 0
                player.time -= 1
                game_score += random.randint(50, 100)
            elif sprite.life > 0:
                sprite.life = 0
                ninja.forward()


def player_crash_barricade():
    for barricade in barricades:
        if barricade.isCrash(player) and barricade.x > player.x:
            player.backward_flag = True
            player.backward(barricade.speed)


def ninja_crash_player():
    global is_game_over, is_game_win
    if ninja.isCrash(player):
        is_game_over = True


def sprite_crash_ninja():
    global game_score
    for sprite in sprites:
        if sprite.isCrash(ninja) and sprite.life > 0:
            game_score += random.randint(100, 150)
            sprite.life = 0


def barricade_crash_ninja():
    for barricade in barricades:
        if barricade.isCrash(ninja):
            barricade.life = 0


def player_crash_heart():
    for heart in hearts:
        if heart.isCrash(player):
            heart.is_alive = False
            ninja.backward()


# update
def sprite_barricade_update():
    global enemy_time
    need_remove_s = []
    need_remove_b = []
    for sprite in sprites:
        if not sprite.is_alive:
            need_remove_s.append(sprite)
        sprite.update()
    for sprite in need_remove_s:
        sprites.remove(sprite)
    for barricade in barricades:
        if not barricade.is_alive:
            need_remove_b.append(barricade)
        barricade.update()
    for barricade in need_remove_b:
        barricades.remove(barricade)
    if game_count % enemy_time == 0:
        enemy_time = random.randint(1, 4) * 70
        rand2 = random.randint(1, 2)
        if rand2 == 1:
            s = Sprite()
            sprites.append(s)
            rand2 = random.randint(1, 2)
        else:
            b = Barricade()
            barricades.append(b)
            rand2 = random.randint(1, 2)


def bullet_update():
    need_remove = []
    for p_b in player_bullets:
        if not p_b.is_alive:
            need_remove.append(p_b)
        p_b.update()
    for p_b in need_remove:
        player_bullets.remove(p_b)


'''
def award_update():
    global award_time
    need_remove = []
    for heart in hearts:
        if not heart.is_alive:
            need_remove.append(heart)
        heart.update()
    for heart in need_remove:
        hearts.remove(heart)
    if game_count % award_time == 0:
        award_time = random.randint(1, 4) * 200
        a = heart()
        hearts.append(a)
'''


def print_text(font, x, y, text, color=(255, 255, 255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x, y))


def reward_update():
    global award_time
    need_remove_d = []
    need_remove_g = []
    need_remove_h = []
    for heart in hearts:
        if not heart.is_alive:
            need_remove_h.append(heart)
        heart.update()
    for r_u in guns:
        if not r_u.is_alive:
            need_remove_g.append(r_u)
        r_u.update()
    for r_w in duns:
        if not r_w.is_alive:
            need_remove_d.append(r_w)
        r_w.update()
    for heart in need_remove_h:
        hearts.remove(heart)
    for r_u in need_remove_g:
        guns.remove(r_u)
    for r_w in need_remove_d:
        duns.remove(r_w)
    if game_count % award_time == 0:
        award_time = random.randint(1, 4) * 200
        rand = random.randint(1, 3)
        if rand == 1:
            a = Heart()
            hearts.append(a)
            # rand = random.randint(1, 3)
        elif rand == 2:
            g = GUN()
            guns.append(g)
            # rand = random.randint(1, 3)
        elif rand == 3:
            d = HUDUN()
            duns.append(d)
            # rand = random.randint(1, 3)


def init():
    global surface, background, clock, cat, group, player, ninja, sprite, font, game_score, bg_sp_speed
    bg_sp_speed = 8
    game_score = 0
    duns.clear()
    guns.clear()
    player_bullets.clear()
    sprites.clear()
    barricades.clear()
    hearts.clear()
    pygame.init()
    font = pygame.font.Font(None, 33)
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    clock = pygame.time.Clock()
    background = Background()
    player = Player()
    ninja = Ninja()
    '''
    cat = MySprite(surface)
    cat.load("sprite.png", 100, 100, 4)
    group = pygame.sprite.Group()
    group.add(cat)
    '''


def crash():
    if not is_game_over:
        player_crash_sprite()
        ninja_crash_player()
        sprite_crash_ninja()
        player_crash_heart()

        player_bullet_crash_enemy()
        player_get_reward()
        barricade_crash_ninja()
        player_crash_barricade()
        player_bullet_crash_barricade()


def update():
    crash()
    background.update()
    if not is_game_over:
        player.update()
        ninja.update()
        # sprite.update()
        sprite_barricade_update()
        # award_update()
        bullet_update()
        reward_update()


def display():
    global game_score
    background.display()
    if not is_game_over:
        player.display()
        ninja.display()
        # sprite.display()
        for sprite in sprites:
            sprite.display()
        for heart in hearts:
            heart.display()
        for barricade in barricades:
            barricade.display()
        for p_b in player_bullets:
            p_b.display()
        for rd in guns:
            rd.display()
        for rw in duns:
            rw.display()
        print_text(font, 0, 0, 'Your Bullet: %s' % player.dan, (255, 255, 255))
        print_text(font, 0, 33, 'Your Shield: %s' % player.time,
                   (200, 200, 200))
        print_text(font, 0, 66,
                   'Your Safe distance: %s' % abs(player.x - ninja.x),
                   (156, 156, 156))
        print_text(font, 0, 99, 'Your Score: %s' % game_score, (50, 50, 50))


def difficult():
    global game_score, bg_sp_speed
    '''
    if 500 <= game_score < 1000:
        bg_sp_speed += 1
    elif 1000 <= game_score < 1500:
        bg_sp_speed += 1
    elif 1500 <= game_score < 2000:
        bg_sp_speed += 1
    '''
    bg_sp_speed += game_score // 500


def eventListener():
    global is_jump, is_game_over, restart_flag
    for event in pygame.event.get():
        if event.type == locals.QUIT:
            exit()
        if event.type == locals.MOUSEBUTTONDOWN:
            left, wheel, right = pygame.mouse.get_pressed()
            if left == 1:
                player.fire()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE and not is_jump:
                is_jump = True
                player.jump()
            elif event.key == pygame.K_r and (is_game_over or is_game_win):
                restart_flag = True
                print('restart_flag is', restart_flag)


surface = None
background = None
SURFACE_WIDTH = 1200
Background_WIDTH = 2400
SURFACE_HEIGHT = 600
# player, ninja and sprite's  initial position
INIT_X_P = 650
INIT_Y_P = 380  # Player
P_space_N = 550  # the space between Player and Ninja
INIT_X_N = INIT_X_P - P_space_N
INIT_Y_N = 368  # Ninja
INIT_X_S = SURFACE_WIDTH  # sprite always born in the most right of surface
INIT_Y_S = 390  # Sprite

bg_sp_speed = 8  # background and sprite's speed
FPS = 50
clock = None
game_time = 0
player = None
ninja = None
# sprite = None
sprites = []
enemy_time = random.randint(1, 4) * 70
hearts = []
barricades = []
award_time = random.randint(1, 4) * 140
reward_time = random.randint(1, 6) * 25

duns = []
guns = []
player_bullets = []

game_count = 0
is_jump = False
is_game_start = False
is_game_over = False
is_game_win = False
restart_flag = False
game_score = 0
font = None

over_img = load_img("./gameover.png")
welcome_img = load_img("./interface.png")
success_img = load_img('./success.png')


def choose():
    global is_game_start
    while True:
        for event in pygame.event.get():
            if event.type == locals.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                else:
                    is_game_start = True
        surface.blit(welcome_img, (0, 0))
        pygame.display.update()
        if is_game_start:
            break


if __name__ == '__main__':
    while True:
        restart_flag = False
        init()
        choose()
        if is_game_start:
            while True:
                game_count += 1
                if game_count == 1000000:
                    game_count = 0
                eventListener()
                # pass_time = clock.tick(FPS)
                # print('pass_time', pass_time)
                # game_time += pass_time
                # ticks = pygame.time.get_ticks()
                update()
                display()
                if is_game_over:
                    surface.blit(over_img, (0, 0))
                if game_score > 1000:
                    is_game_win = True
                if is_game_win:
                    surface.blit(success_img, (0, 0))
                # group.update(ticks)
                # group.draw(surface)
                pygame.display.update()
                if restart_flag:
                    is_game_over = False
                    is_game_start = False
                    is_game_win = False
                    break
