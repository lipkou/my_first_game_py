import pygame
from time import sleep, time
pygame.init()

#! sdfsdfdsfsd
#? sdfsdfsdf
#* dfsdf
#// хуй

GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
LIGHT_BLUE = (50, 50, 220)
RED = (200, 0, 0)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)



BG_COLOR = (0, 0, 60)
WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Surwaiwal_game(test)')
clock = pygame.time.Clock()

img_level_1 = pygame.image.load('images//level_1.jpg')
img_level_1 = pygame.transform.scale(img_level_1, (WIN_WIDTH, WIN_HEIGHT))


img_level_2 = pygame.image.load('images//level_2.jpg')
img_level_2 = pygame.transform.scale(img_level_2, (WIN_WIDTH, WIN_HEIGHT))

next_level_image = pygame.image.load('images//next_level_v2.jpg')
next_level_image = pygame.transform.scale(next_level_image, (WIN_WIDTH, WIN_HEIGHT))

win_image = pygame.image.load('images//win_image.png')
win_image = pygame.transform.scale(win_image, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load('music//fon_music.ogg')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)

music_win = pygame.mixer.Sound('music//you_win.wav')
music_gg = pygame.mixer.Sound('music//GG.ogg')
music_use = pygame.mixer.Sound('music//Button_use.ogg')
music_pick_up_coin = pygame.mixer.Sound('music//pick_up_coin.ogg')
music_button_use = pygame.mixer.Sound('music//Button_use.ogg')

gg_image = pygame.image.load('images//Gg_image.jpg')
gg_image = pygame.transform.scale(gg_image, (WIN_WIDTH, WIN_HEIGHT))

class Button():
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.txt = pygame.font.SysFont("Arial", 30).render(text, True, BLACK)
        self.color = BLUE

    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.txt, (self.rect.x + 50, self.rect.y + 20))

class Area():
    def __init__(self, x, y, width, height, color): #конструктор прямокутника
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
    def draw_rect(self): #робить прямокутник
        pygame.draw.rect(window, self.color, self.rect)

class Label(Area):
    def set_text(self, text): #настройка тексту
        self.font_40 = pygame.font.SysFont('Arial', 30)
        self.text = self.font_40.render(text, True, BLACK)
    def draw_label(self, shift_x, shift_y): #виведення тексту на екран
        self.draw_rect()
        window.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))

class Game_sprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Game_sprite):
    def __init__(self, x, y, width, height, image, speed_x, speed_y):
        super().__init__(x, y, width, height, image)
        self.speed_x = speed_x
        self.speed_y = speed_y

        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)

        self.direction = 'right'

    def update(self):
        if self.speed_x < 0 and self.rect.left > 0 or self.speed_x > 0 and self.rect.right < WIN_WIDTH:
            self.rect.x += self.speed_x
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for wall in walls_touched:
                self.rect.right = min(self.rect.right, wall.rect.left)
        if self.speed_x < 0:
            for wall in walls_touched:
                self.rect.left = max(self.rect.left, wall.rect.right)

        if self.speed_y < 0 and self.rect.top > 0 or self.speed_y > 0 and self.rect.bottom < WIN_HEIGHT:
            self.rect.y += self.speed_y
        walls_touched = pygame.sprite.spritecollide(self, walls, False)
        if self.speed_y < 0:
            for wall in walls_touched:
                self.rect.top = max(self.rect.top, wall.rect.bottom)
        if self.speed_y > 0:
            for wall in walls_touched:
                self.rect.bottom = min(self.rect.bottom, wall.rect.top)
    def fire(self):
        if self.direction == 'left':
            bullet = Bullet(self.rect.left, self.rect.centery, 10, 5, 'images//arrow.png', -28)
        elif self.direction == 'right':
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 5, 'images//arrow.png', 28)
        bullets.add(bullet)

class Enemy(Game_sprite):
    def __init__(self, x, y, width, height, image, speed, direction, min_coord, max_coord):
        super().__init__(x, y, width, height, image)
        self.speed = speed
        self.min_coord = min_coord
        self.max_coord = max_coord
        self.direction = direction
        self.image_r = self.image
        self.image_l = pygame.transform.flip(self.image, True, False)
    def update(self):
        if self.direction == 'left' or self.direction == 'right':
            if self.rect.right >= self.max_coord:
                self.image = self.image_l
                self.direction = 'left'
            elif self.rect.left <= self.min_coord:
                self.image = self.image_r
                self.direction = 'right'
            
            if self.direction == 'left':
                self.rect.x -= self.speed
            elif self.direction == 'right':
                self.rect.x += self.speed
            
        elif self.direction == 'up' or self.direction == 'down':
            if self.rect.top <= self.min_coord:
                self.direction = 'down'
            elif self.rect.bottom >= self.max_coord:
                self.direction = 'up'
            
            if self.direction == 'up':
                self.rect.y -= self.speed
            if self.direction == 'down':
                self.rect.y += self.speed    

class Bullet(Game_sprite):
    def __init__(self, x, y, width, height, image, speed):
        super().__init__(x, y, width, height, image)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= WIN_WIDTH or self.rect.left <= 0:
            self.kill()

btn1 = Button(100, 100, 200, 100, "Level 1")
btn2 = Button(400, 100, 200, 100, "Level 2")
menu = Button(250, 400, 170, 70, "Menu")


enemys = pygame.sprite.Group()
bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()


arrow = Game_sprite(350, 300, 80, 100, 'images//arrow.png')

music_shot = pygame.mixer.Sound('music//shot.ogg')

stat_menu = 0
level = 0
start_level_0 = 0
start_level_1 = 0
start_level_2 = 0
time_sleep_st = 0
time_sleep_end = 0

play = True
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.speed_x = 10
                player.image = player.image_r
                player.direction = 'right'
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.speed_x = -10
                player.image = player.image_l
                player.direction = 'left'
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.speed_y = -10
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.speed_y = 10
            if event.key == pygame.K_SPACE:
                player.fire()
                music_shot.play()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.speed_x = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.speed_x = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.speed_y = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.speed_y = 0

        #стартове меню
        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn1.rect.collidepoint(x, y):
                    btn1.color = LIGHT_BLUE
                elif btn2.rect.collidepoint(x, y):
                    btn2.color = LIGHT_BLUE
                elif menu.rect.collidepoint(x, y):
                    menu.color = LIGHT_BLUE
                else:
                    btn1.color = BLUE
                    btn2.color = BLUE
                    menu.color = BLUE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.rect.collidepoint(x, y):
                    level = 1
                    music_button_use.play()

                if btn2.rect.collidepoint(x, y):
                    level = 2
                    music_button_use.play()

                if menu.rect.collidepoint(x, y):
                    if stat_menu == 0:
                        stat_menu = 1
                    else:
                        stat_menu = 0
                    print('stat_menu:', stat_menu)
                    music_button_use.play()

    # загрузка главного меню (всі елементи)
    if level == 0: 
        if start_level_0 == 0:
            player = Player(315, 250, 75, 80, 'images//hunter.png', 0, 0)
            start_level_0 = 1
        
        if stat_menu == 1:
            pass

        window.fill(GREY)
        btn1.show()
        btn2.show()
        menu.show()
        player.reset()
        player.update()
        bullets.draw(window)
        bullets.update()



    elif level == 1: 
        # загрузка 1 ур
        if start_level_1 == 0:
            player = Player(100, 50, 75, 80, 'images//hunter.png', 0, 0)
            play = True
            window.blit(img_level_1, (0, 0))
            enemys.empty()
            enemys.add(Enemy(400, 300, 90, 90, 'images//warior.png', 8, 'left', 420, 700))
            enemys.add(Enemy(600, 98, 90, 90, 'images//warior.png', 5, 'right', 330, 700))
            walls.empty()
            walls.add(Game_sprite(0, 190, 120, 30, 'images//wall.png'))
            walls.add(Game_sprite(120, 190, 120, 30, 'images//wall.png'))
            walls.add(Game_sprite(240, 190, 170, 30, 'images//wall.png'))
            walls.add(Game_sprite(310, 110, 30, 250, 'images//wall.png'))
            walls.add(Game_sprite(240, 360, 180, 30, 'images//wall.png'))
            walls.add(Game_sprite(580, 190, 120, 30, 'images//wall.png'))
            walls.add(Game_sprite(120, 360, 120, 30, 'images//wall.png'))
            coin = Game_sprite(240,  280, 50, 50, 'images//coin.png')
            start_level_1 = 1

        
        if play:
            window.blit(img_level_1, (0, 0))
            player.reset()
            player.update()
            enemys.draw(window)
            enemys.update()
            walls.draw(window)
            coin.reset()
            bullets.draw(window)
            bullets.update()

            if pygame.sprite.collide_rect(player, coin):
                play = False
                level = 2
                pygame.mixer.music.stop()
                music_pick_up_coin.play()
                time_sleep_end = time() + 1.5
                time_sleep_st = time()
                window.blit(next_level_image, (0, 0))
                pygame.display.update()
                while not time_sleep_st >= time_sleep_end:
                    time_sleep_st = time()
                    if time_sleep_st >= time_sleep_end:
                        music_pick_up_coin.stop()

                
            if pygame.sprite.spritecollide(player, enemys, False):
                play = False
                window.blit(gg_image, (0, 0))
                pygame.mixer.music.stop()
                music_gg.play()

            pygame.sprite.groupcollide(bullets, walls, True, False)
            pygame.sprite.groupcollide(bullets, enemys, True, True)

    elif level == 2:
        
        # загрузка 2 ур
        if start_level_2 == 0:
            pygame.mixer.music.load('music//fon_music(2).ogg')
            pygame.mixer.music.play()
            player = Player(620, 400, 75, 80, 'images//hunter.png', 0, 0)
            play = True
            enemys.empty()
            enemys.add(Enemy(10, 5, 90, 90, 'images//warior_L2.png', 8, 'right', 0, 400))
            enemys.add(Enemy(0, 405, 90, 90, 'images//warior_L2.png', 10, 'right', 0, 560))
            walls.empty()
            walls.add(Game_sprite(560, 100, 30, 400, 'images//wall.png'))
            walls.add(Game_sprite(400, 0, 30, 260, 'images//wall.png'))
            walls.add(Game_sprite(280, 230, 150, 30, 'images//wall.png'))
            walls.add(Game_sprite(280, 230, 30, 150, 'images//wall.png'))
            walls.add(Game_sprite(140, 370, 290, 30, 'images//wall.png'))
            walls.add(Game_sprite(140, 100, 30, 150, 'images//wall.png'))
            walls.add(Game_sprite(0, 220, 140, 30, 'images//wall.png'))
            walls.add(Game_sprite(140, 100, 170, 30, 'images//wall.png'))

            coin = Game_sprite(50,  140, 50, 50, 'images//coin.png')
            start_level_2 = 1
        

        if time_sleep_st >= time_sleep_end:
            music_pick_up_coin.stop()
            if play:
                window.blit(img_level_2, (0, 0))
                player.reset()
                player.update()
                enemys.draw(window)
                enemys.update()
                walls.draw(window)
                coin.reset()
                bullets.draw(window)
                bullets.update()
                
                #arrow.reset()

                if pygame.sprite.collide_rect(player, coin):
                    window.blit(win_image, (0, 0))
                    play = False
                    level = 3
                    pygame.mixer.music.stop()
                    music_win.play()
                    




                if pygame.sprite.spritecollide(player, enemys, False):
                    play = False
                    window.blit(gg_image, (0, 0))
                    pygame.mixer.music.stop()
                    music_gg.play()

                pygame.sprite.groupcollide(bullets, walls, True, False)
                pygame.sprite.groupcollide(bullets, enemys, True, True)
        else:
            time_sleep_st = int(time())


        
    clock.tick(FPS)
    pygame.display.update()