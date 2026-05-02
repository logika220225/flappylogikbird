import pygame
import random
from audio import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

bird = pygame.Rect(100, 300, 30, 30)
bird_move = 0
gravity = 0.5
score = 0
status = "PLAY"

tubes = []
SPAWN_EVENT = pygame.USEREVENT
pygame.time.set_timer(SPAWN_EVENT, 1500)

rec = AudioRecorder()
rec.start()
LIMIT = 0.03
cooldown = 0

running = True
while running:
    clock.tick(60)
    vol = rec.get_volume()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWN_EVENT and status == "PLAY":
            h = random.randint(100, 350)
            tubes.append(pygame.Rect(800, 0, 50, h))
            tubes.append(pygame.Rect(800, h + 180, 50, 600))
        if event.type == pygame.KEYDOWN and status == "FAIL":
            if event.key == pygame.K_SPACE:
                status = "PLAY"
                tubes.clear()
                bird.y, bird_move, score = 300, 0, 0

    screen.fill((135, 206, 235))

    if status == "PLAY":
        if cooldown > 0: cooldown -= 1
        if vol > LIMIT and cooldown == 0:
            bird_move = -7
            cooldown = 15

        bird_move += gravity
        bird.y += bird_move
        pygame.draw.rect(screen, (255, 255, 0), bird)

        for t in tubes[:]:
            t.x -= 4
            pygame.draw.rect(screen, (0, 150, 0), t)
            if bird.colliderect(t): status = "FAIL"
            if t.x < -50: tubes.remove(t)
            if t.x == 100 and t.y == 0: score += 1

        if bird.top <= 0 or bird.bottom >= 600: status = "FAIL"

        bar_h = int(vol * 1500)
        pygame.draw.rect(screen, (255, 0, 0), (760, 580 - bar_h, 20, bar_h))
        pygame.draw.line(screen, (0, 0, 0), (755, 580 - int(LIMIT*1500)), (785, 580 - int(LIMIT*1500)), 2)

        score_img = font.render(f"Очки: {score}", True, (0, 0, 0))
        screen.blit(score_img, (20, 20))

    else:
        msg = font.render("ГРА ЗАКІНЧЕНА", True, (200, 0, 0))
        screen.blit(msg, (300, 200))
        
        if score >= 20: medal = "Золота 🥇"
        elif score >= 10: medal = "Срібна 🥈"
        else: medal = "Бронзова 🥉"
        
        med_img = font.render(f"Ваша медаль: {medal}", True, (0, 0, 0))
        screen.blit(med_img, (280, 260))
        screen.blit(font.render("Пробіл - ще раз", True, (50, 50, 50)), (300, 350))

    pygame.display.update()

rec.stop()
pygame.quit()