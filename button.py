import pygame
pygame.init()

GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
LIGHT_BLUE = (50, 50, 220)
RED = (200, 0, 0)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

class Button():
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.txt = pygame.font.SysFont("Arial", 30).render(text, True, BLACK)
        self.color = BLUE

    def show(self):
        pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.txt, (self.rect.x + 50, self.rect.y + 30))

btn1 = Button(150, 100, 200, 100, "Level 1")
btn2 = Button(150, 250, 200, 100, "Level 2")

game = True
level = 0
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if level == 0:
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if btn1.rect.collidepoint(x, y):
                    btn1.color = LIGHT_BLUE
                elif btn2.rect.collidepoint(x, y):
                    btn2.color = LIGHT_BLUE
                else:
                    btn1.color = BLUE
                    btn2.color = BLUE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.rect.collidepoint(x, y):
                    level = 1
                if btn2.rect.collidepoint(x, y):
                    level = 2

    if level == 0:
        window.fill(GREY)
        btn1.show()
        btn2.show()

    elif level == 1:
        window.fill(GREEN)
        # далі код 1 рівня гри

    elif level == 2:
        window.fill(BLUE)
        # далі код 2 рівня гри
    
    clock.tick(40)
    pygame.display.update()


