import pygame
import os
import random

FPS = 60
WIDTH = 500
HEIGHT = 650
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
location = [0, 1, 2, 3, 4]
record = []
times = 0
score = 0
shoot_times = 0
coin = 0

#遊戲初始化 and 創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('病毒入侵')

# 載入圖片
coin_img = pygame.image.load(os.path.join('img', 'coin.png')).convert()
coin_mini_img = pygame.transform.scale(coin_img, (30,30))
coin_mini_img.set_colorkey(BLACK)
start_img = pygame.image.load(os.path.join('img', 'button_start.png')).convert()
store_img = pygame.image.load(os.path.join('img', 'button_store.png')).convert()
exit_img = pygame.image.load(os.path.join('img', 'button_exit.png')).convert()
bullet_button_img = pygame.image.load(os.path.join('img', 'button_bullet.png')).convert()
bullet_button_img.set_colorkey(WHITE)
store_img.set_colorkey(WHITE)
start_img.set_colorkey(WHITE)
exit_img.set_colorkey(WHITE)
ship_img = pygame.image.load(os.path.join('img', 'spaceship.ico')).convert()
ship_mini_img = pygame.transform.scale(ship_img, (30,23))
ship_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join('img', 'bullet.png')).convert()
bg_img = pygame.transform.scale(pygame.image.load(os.path.join('img', 'background.png')).convert(),(WIDTH,HEIGHT))
expl_anime = {}
expl_anime['lg'] = []
expl_anime['sm'] = []
expl_anime['player'] = []
treasure_imgs = {}
treasure_imgs['heart'] = pygame.image.load(os.path.join('img', 'heart.png')).convert()
treasure_imgs['bullet'] = pygame.image.load(os.path.join('img', 'bullet1.png')).convert()
bullet_mini_img = pygame.transform.scale(treasure_imgs['bullet'], (30,30))
bullet_mini_img.set_colorkey(WHITE)
virus_group = []
for i in range(3):
    virus_img = pygame.image.load(os.path.join('img', f'virus{i}.png')).convert()
    virus_group.append(virus_img)
for i in range(9):
    expl_img = pygame.image.load(os.path.join('img', f'expl{i}.png')).convert()
    player_expl_img = pygame.image.load(os.path.join('img', f'player_expl{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    player_expl_img.set_colorkey(BLACK)
    expl_anime['lg'].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anime['sm'].append(pygame.transform.scale(expl_img,(50,50)))
    expl_anime['player'].append(player_expl_img)
icon_img = virus_group[0]
icon_img.set_colorkey(BLACK)
pygame.display.set_icon(icon_img)

font_name = os.path.join("GenSenRounded-B.ttc")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ship_img, (52,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.health = 3
        self.speedx = 6

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx

        elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.health <= 0:
            self.kill()

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Block(pygame.sprite.Sprite):
    def __init__(self, num):
        pygame.sprite.Sprite.__init__(self)
        no = random.randint(0,2)
        self.image = pygame.transform.scale(virus_group[no],(100, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 48
        self.rect.x = num * 100
        self.rect.bottom = -100
        self.speedy = 10
    def update(self):
        self.rect.y += self.speedy
        global score
        if self.rect.top > HEIGHT:
            score += 2
            print(score)
            self.kill()
            produce_block()
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (15, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Treasure(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['heart', 'bullet'])
        self.image = pygame.transform.scale(treasure_imgs[self.type], (40,40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.center = center
        self.speedy = 4
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anime[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anime[self.size]):
                self.kill()
            else:
                self.image = expl_anime[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Button(pygame.sprite.Sprite):
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
       
def draw_text(surf, text, size, x, y, bg):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.bottom = y
    if bg:
        pygame.draw.rect(screen, (170,170,170), text_rect)
    surf.blit(text_surface, text_rect)

def produce_block():
    k = random.randint(0,4)
    while k in record:
        k += 1
        if k == 5:
            k = 0
    record.append(k)
    print(record)
    if len(record) == 4:
        for i in record:
            block = Block(i)
            all_sprites.add(block)
            blocks.add(block)
        record[0:5] = []
class shoottimes(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img = img
        self.img_rect = self.img.get_rect()
        self.img_rect.left = x
        self.img_rect.bottom = y + 2
    def draw(self, surface, time, size, bg):
        self.surf = surface
        self.size = size
        self.font = pygame.font.Font(font_name, self.size)
        self.surface = self.font.render('x' + str(time), True, WHITE)
        self.rect = self.surface.get_rect()
        self.rect.left = self.img_rect.left + 30
        self.rect.bottom = self.img_rect.bottom
        if bg:
            pygame.draw.rect(screen, (170,170,170), self.rect)
        self.surf.blit(self.surface, self.rect)
        self.surf.blit(self.img, self.img_rect)
        
    def update(self, time):
        self.kill()
        self.surface = self.font.render('x' + str(time), True, WHITE)
        self.surf.blit(self.img, self.img_rect)
        self.surf.blit(self.surface, self.rect)
        

def draw_health(surf, hp, img, x, y):
    for i in range(hp):
        img_rect = img.get_rect()
        img_rect.x = x - 37*i
        img_rect.bottom = y 
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(bg_img, (0, 0))
    draw_text(screen, '病毒入侵', 64, WIDTH/2, 250, True)
    draw_text(screen, '← →移動飛船 空白鍵發射子彈', 30, WIDTH/2, 400,True)
    show_coin = shoottimes(coin_mini_img, WIDTH-100, 35)
    shoot_time = shoottimes(bullet_mini_img, WIDTH-100, 70)
    show_coin.draw(screen, coin, 26,True)
    shoot_time.draw(screen,shoot_times, 26, True)
    start_button = Button(50, 500, start_img, 0.2)
    store_button = Button(300, 500, store_img, 0.2)
    waiting = True
    while waiting:
        global show_init
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if start_button.draw(screen):
            show_init = 1
            waiting = False
        if store_button.draw(screen):
            show_init = 2
            waiting = False
        pygame.display.update()

def draw_game():
    global show_init
    global coin
    global score
    global shoot_times
    waiting = True
    player = Player()
    all_sprites.add(player)
    if len(blocks) != 4:
        for i in range(4):
            produce_block()
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and shoot_times > 0:
                    player.shoot()
                    shoot_times -= 1


        # 更新遊戲
        all_sprites.update()
        #判斷寶物 玩家碰撞
        hits_treasure = pygame.sprite.spritecollide(player, treasures, True, pygame.sprite.collide_rect)
        for hit in hits_treasure:
            if hit.type == 'bullet':
                shoot_times += 1
            elif hit.type == 'heart':
                player.health += 1

        #判斷方塊 子彈碰撞
        hits_bullet = pygame.sprite.groupcollide(blocks, bullets, True, True)
        for hit in hits_bullet:
            score += 1
            expl = Explosion(hit.rect.center, 'lg')
            if random.random() > 0.5:
                trea = Treasure(hit.rect.center)
                all_sprites.add(trea)
                treasures.add(trea)
            all_sprites.add(expl)
            produce_block()
        #判斷方塊 玩家碰撞
        hits_player = pygame.sprite.spritecollide(player, blocks, True, pygame.sprite.collide_rect)
        for hit in hits_player:
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            player.health -= 1
            produce_block()
            if player.health <= 0:
                player_death = Explosion(player.rect.center, 'player')
                all_sprites.add(player_death)

        if player.health <= 0 and not(player_death.alive()):
            coin += score
            show_init = 0
            score = 0
            waiting = False
        # 畫面顯示
        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, str(score), 30, WIDTH/2, 36, False)
        draw_health(screen, player.health, ship_mini_img, WIDTH - 35, 32)
        shoot_time = shoottimes(bullet_mini_img, 10, 35)
        shoot_time.draw(screen, shoot_times,26, True)
        pygame.display.update()
store_sprites = pygame.sprite.Group()
def draw_store():
    global shoot_times
    global coin
    screen.blit(bg_img, (0, 0))
    draw_text(screen, '商店', 64, WIDTH/2, 100, True)
    show_coin = shoottimes(coin_mini_img, WIDTH-100, 35)
    shoot_time = shoottimes(bullet_mini_img, WIDTH-100, 70)
    show_coin.draw(screen, coin, 26,True)
    shoot_time.draw(screen,shoot_times, 26, True)
    shoottimes_button = Button(100, HEIGHT/4, bullet_button_img, 0.4)
    exit_store_button = Button(WIDTH-200, 550, exit_img, 0.2)
    waiting = True
    while waiting:
        global show_init
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if shoottimes_button.draw(screen):
            if coin >= 10:
                shoot_times+=1
                coin-=10
                screen.blit(bg_img, (0, 0))
                draw_text(screen, '商店', 64, WIDTH/2, 100, True)
                show_coin = shoottimes(coin_mini_img, WIDTH-100, 35)
                shoot_time = shoottimes(bullet_mini_img, WIDTH-100, 70)
                show_coin.draw(screen, coin, 26,True)
                shoot_time.draw(screen,shoot_times, 26, True)
        if exit_store_button.draw(screen):
            show_init = 0
            waiting = False
        pygame.display.update()

show_init = 0
running = True
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
treasures = pygame.sprite.Group()
# 遊戲迴圈
while running:
    while show_init == 2:
        draw_store()
    while show_init == 0:
        draw_init()
    while show_init == 1:
        draw_game()
        

pygame.quit()