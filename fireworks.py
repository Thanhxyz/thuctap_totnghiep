import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎆 Fireworks Happy New Year 🎆")

clock = pygame.time.Clock()

PARTICLE_SIZE = 4
GRAVITY = 0.15

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.life = 255
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-6, -1)

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.life -= 4

    def draw(self, surface):
        if self.life > 0:
            s = pygame.Surface(
                (PARTICLE_SIZE * 2, PARTICLE_SIZE * 2),
                pygame.SRCALPHA
            )

            # 🎆 PHÁO HOA (pygame.draw.circle)
            pygame.draw.circle(
                s,
                (*self.color, self.life),
                (PARTICLE_SIZE, PARTICLE_SIZE),
                PARTICLE_SIZE
            )

            surface.blit(s, (self.x, self.y))

particles = []

def create_firework():
    x = random.randint(100, WIDTH - 100)
    y = random.randint(100, HEIGHT // 2)
    color = (
        random.randint(150, 255),
        random.randint(150, 255),
        random.randint(150, 255)
    )
    for _ in range(60):
        particles.append(Particle(x, y, color))

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            create_firework()

    if random.random() < 0.03:
        create_firework()

    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0:
            particles.remove(p)

    pygame.display.flip()

pygame.quit()
sys.exit()
