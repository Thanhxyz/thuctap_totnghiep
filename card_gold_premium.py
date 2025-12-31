import pygame
import sys
import math
import random

# ================== CẤU HÌNH ==================
WIDTH, HEIGHT = 960, 640
FPS = 60

BLACK = (10, 10, 28)
DARK_BG = (18, 18, 40)
WHITE = (240, 240, 240)

GOLD_1 = (255, 215, 120)
GOLD_2 = (255, 180, 60)
GOLD_3 = (255, 240, 180)

PINK = (255, 150, 190)

GRAVITY = 0.18

NAME_TEXT = "NGUYỄN THỊ KIM"
WISH_1 = "Chúc em một năm mới thật nhiều niềm vui,"
WISH_2 = "bình an, hạnh phúc và luôn mỉm cười."

# ================== PHÁO HOA ==================
class Rocket:
    def __init__(self):
        self.x = random.randint(160, WIDTH - 160)
        self.y = HEIGHT
        self.vy = random.uniform(-12, -15)
        self.trail = []

    def update(self):
        self.trail.append((self.x, self.y))
        self.y += self.vy
        self.vy += GRAVITY

    def draw(self, screen):
        for i, t in enumerate(self.trail[-18:]):
            pygame.draw.circle(screen, GOLD_2, t, 2)
        pygame.draw.circle(screen, GOLD_1, (int(self.x), int(self.y)), 3)

    def ready(self):
        return self.vy >= 0


class Explosion:
    def __init__(self, x, y):
        self.parts = []
        color = random.choice([GOLD_1, GOLD_2, PINK, WHITE])
        for _ in range(90):
            a = random.uniform(0, math.pi * 2)
            s = random.uniform(2, 4)
            self.parts.append([
                x, y,
                math.cos(a) * s,
                math.sin(a) * s,
                color,
                random.randint(30, 55)
            ])

    def update(self):
        for p in self.parts:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += GRAVITY * 0.25
            p[5] -= 1
        self.parts = [p for p in self.parts if p[5] > 0]

    def draw(self, screen):
        for p in self.parts:
            pygame.draw.circle(screen, p[4], (int(p[0]), int(p[1])), 3)

# ================== HÀM VẼ CHỮ ÁNH KIM ==================
def draw_gold_text(screen, font, text, center, phase):
    base = font.render(text, True, GOLD_2)
    rect = base.get_rect(center=center)

    # Glow layer
    for r in range(6, 0, -2):
        glow = font.render(text, True, GOLD_1)
        glow.set_alpha(40)
        screen.blit(glow, glow.get_rect(center=center))

    # Gradient shimmer (giả lập)
    shimmer = int(120 + 120 * math.sin(phase))
    gold_dynamic = (255, shimmer, 120)

    top = font.render(text, True, GOLD_3)
    bottom = font.render(text, True, gold_dynamic)

    screen.blit(bottom, bottom.get_rect(center=(center[0], center[1] + 2)))
    screen.blit(top, top.get_rect(center=center))


# ================== MAIN ==================
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Thiệp Năm Mới Ánh Kim Premium")
    clock = pygame.time.Clock()

    try:
        title_font = pygame.font.Font("Roboto-Bold.ttf", 46)
        name_font = pygame.font.Font("Roboto-Bold.ttf", 60)
        text_font = pygame.font.Font("Roboto-Bold.ttf", 26)
    except:
        title_font = pygame.font.SysFont("Segoe UI", 46)
        name_font = pygame.font.SysFont("Segoe UI", 60)
        text_font = pygame.font.SysFont("Segoe UI", 26)

    rockets = []
    explosions = []
    timer = 0
    phase = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(DARK_BG)

        # ===== KHUNG THIỆP =====
        pygame.draw.rect(
            screen, GOLD_2,
            (70, 60, WIDTH - 140, HEIGHT - 120),
            2, border_radius=22
        )

        # ===== TITLE =====
        title = title_font.render("HAPPY NEW YEAR 2026", True, GOLD_1)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 130)))

        # ===== TÊN ÁNH KIM =====
        phase += 0.06
        draw_gold_text(
            screen,
            name_font,
            NAME_TEXT,
            (WIDTH // 2, 250),
            phase
        )

        # ===== LỜI CHÚC =====
        wish1 = text_font.render(WISH_1, True, WHITE)
        wish2 = text_font.render(WISH_2, True, WHITE)
        screen.blit(wish1, wish1.get_rect(center=(WIDTH // 2, 400)))
        screen.blit(wish2, wish2.get_rect(center=(WIDTH // 2, 430)))

        # ===== PHÁO HOA =====
        timer += 1
        if timer % 22 == 0:
            rockets.append(Rocket())

        for r in rockets[:]:
            r.update()
            r.draw(screen)
            if r.ready():
                explosions.append(Explosion(r.x, r.y))
                rockets.remove(r)

        for ex in explosions[:]:
            ex.update()
            ex.draw(screen)
            if not ex.parts:
                explosions.remove(ex)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
