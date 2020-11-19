import pygame, random

pygame.init()

WIDTH = 600
HEIGHT = 700
clock = pygame.time.Clock()
ilosc=0

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird!")


class Bird:
    def __init__(self):
        self.x = WIDTH // 5
        self.y = HEIGHT // 2
        self.r = 15
        self.color = (255, 0, 0)
        self.g = 0.5
        self.vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.r)

    def update(self):
        self.y += self.vel
        self.vel += self.g

    def touchedGround(self):
        if self.y + self.r >= HEIGHT or self.y - self.r <=0 :
            return True

    def skok(self):
        if self.vel > 20:
            self.vel = -5
            print("tera")
        else:
            self.vel = -10


class Box:
    speed=5
    def __init__(self):
        self.x = WIDTH + 10
        self.y = 0
        self.space = 200
        self.height = random.randint(10, HEIGHT - self.space - 10)
        self.width = 30
        self.color = (0, 255, 0)
        self.vel = self.speed

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, self.color, (self.x, self.y + self.space + self.height, self.width, HEIGHT))

    def update(self):
        self.x -= self.vel


def checkIfNeedToAddBox(lista):
    if lista[-1].x<=WIDTH-300:
        lista.append(Box())
def checkIfNeedToDeleteBox(lista):
    if lista[0].x<-30:
        del lista[0]
        return 1

def przegrana(bird,boxes):
    print("przegrana")
    bird.g = 0
    bird.vel = 0
    for i in boxes:
        i.vel = 0


bird = Bird()

boxes=[]
boxes.append(Box())

run = True

while run:
    clock.tick(60)

    # KONTROLA EVENTOW
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.skok()

    if checkIfNeedToDeleteBox(boxes):
        ilosc += 1
        if ilosc == 10 and Box.speed <= 7:
            Box.speed += 1
            for i in boxes:
                i.vel = Box.speed
            ilosc = 0

    # kolizja
    b1 = boxes[0]
    if ((b1.x <= bird.x + bird.r) and (b1.x + b1.width > bird.x-bird.r)) or bird.touchedGround():
        if bird.touchedGround() or (bird.y-bird.r < b1.height) or (bird.y+bird.r > b1.height + b1.space) :
            przegrana(bird, boxes)
            run=False

    # rysowanie box i bird
    for i in boxes:
        i.draw()
        i.update()

    bird.draw(win)
    bird.update()

    checkIfNeedToAddBox(boxes)

    pygame.display.update()
    win.fill((0, 0, 0))

    if not run:
        pygame.time.wait(2000)

pygame.quit()
