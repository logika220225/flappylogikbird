import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
clock = pygame.time.Clock()

bird_rect = pygame.Rect(50, 300, 30, 30)
tube_rect = pygame.Rect(35, 100, 30, 100)
gravity = 0.5
bird_movement = 0

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

    bird_movement += gravity
    bird_rect.y += bird_movement

    if bird_rect.colliderect(tube_rect):
        print("Game Over!")
        running = False

    if bird_rect.top <= 0 or bird_rect.bottom >= 600:
        running = False

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), bird_rect)
    pygame.draw.rect(screen, (50,50,50), tube_rect)
    pygame.display.update()