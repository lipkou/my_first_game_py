import pygame
pygame.init()

#! sdfsdfdsfsd
#? sdfsdfsdf
#* dfsdf
#// хуй


BLACK = (0, 0, 0)


BG_COLOR = (0, 0, 60)
WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 40

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Surwaiwal_game(test)')
clock = pygame.time.Clock()

BG_IMAGE = pygame.image.load('images//BG_IMAGE.jpg')
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIN_WIDTH, WIN_HEIGHT))

win_image = pygame.image.load('images//BG_IMAGE(2).jpg')
win_image = pygame.transform.scale(win_image, (WIN_WIDTH, WIN_HEIGHT))

pygame.mixer.music.load('music//fon_music(2).ogg')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
music_win = pygame.mixer.Sound('music//fon_music.ogg')

pygame.mixer.music.load('music//fon_music(2).ogg')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)
music_gg = pygame.mixer.Sound('music//GG.ogg')


gg_image = pygame.image.load('images//Gg_image.jpg')
gg_image = pygame.transform.scale(gg_image, (WIN_WIDTH, WIN_HEIGHT))

class Button():
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.txt = pygame.font.SysFont("Arial", 30).render(text, True, BLACK)
        self.color = BLUE

    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.txt, (self.rect.x + 50, self.rect.y + 30))

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
            bullet = Bullet(self.rect.left, self.rect.centery, 10, 5, 'images//arrow.png', -40)
        elif self.direction == 'right':
            bullet = Bullet(self.rect.right, self.rect.centery, 10, 5, 'images//arrow.png', 40)
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

enemys = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player(100, 50, 75, 80, 'images//hunter.png', 0, 0)
warior = Enemy(400, 300, 90, 90, 'images//warior.png', 8, 'left', 420, 700)
warior2 = Enemy(600, 98, 90, 90, 'images//warior.png', 5, 'right', 330, 700)
enemys.add(warior)
enemys.add(warior2)

walls = pygame.sprite.Group()
walls.add(Game_sprite(0, 190, 120, 30, 'images//wall.png'))
walls.add(Game_sprite(120, 190, 120, 30, 'images//wall.png'))
walls.add(Game_sprite(240, 190, 170, 30, 'images//wall.png'))
walls.add(Game_sprite(310, 110, 30, 250, 'images//wall.png'))
walls.add(Game_sprite(240, 360, 180, 30, 'images//wall.png'))
walls.add(Game_sprite(580, 190, 120, 30, 'images//wall.png'))
walls.add(Game_sprite(120, 360, 120, 30, 'images//wall.png'))

coin = Game_sprite(240,  280, 50, 50, 'images//coin.png')
arrow = Game_sprite(350, 300, 80, 100, 'images//arrow.png')

music_shot = pygame.mixer.Sound('music//shot.ogg')

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
        


    if play:
        window.blit(BG_IMAGE, (0, 0))
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
            play = False
            window.blit(win_image, (0, 0))
            pygame.mixer.music.stop()
            music_win.play()

        if pygame.sprite.spritecollide(player, enemys, False):
            play = False
            window.blit(gg_image, (0, 0))
            pygame.mixer.music.stop()
            music_gg.play()

        pygame.sprite.groupcollide(bullets, walls, True, False)
        pygame.sprite.groupcollide(bullets, enemys, True, True)
        
    clock.tick(FPS)
    pygame.display.update()