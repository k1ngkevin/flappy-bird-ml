import pygame
import random


pygame.init()
width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0


def create_pipe():
    gap_y = random.randint(150, 500)
    gap_size = 200
    pipe_x = width
    pipe_width = 60
    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, gap_y)
    bottom_pipe = pygame.Rect(
        pipe_x, gap_y + gap_size, pipe_width, height - (gap_y + gap_size))
    return {
        "top": top_pipe,
        "bottom": bottom_pipe,
        "scored": False,
    }


pipes = []
pipe_timer = 0
pipe_spawn_time = 1.5
pipe_speed = 300

bird_pos = pygame.math.Vector2(width / 2, height / 2)
gravity = 0.5
bird_velocity_y = 0
jump_force = -8

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#70C5CE")

    pipe_timer += dt
    if (pipe_timer >= pipe_spawn_time):
        pipes.append(create_pipe())
        pipe_timer = 0

    for pipe_pair in pipes:
        pipe_pair["top"].x -= pipe_speed * dt
        pipe_pair["bottom"].x -= pipe_speed * dt

    pipes = [
        pipe_pair for pipe_pair in pipes
        if pipe_pair["top"].right > 0
    ]

    for pipe_pair in pipes:
        pygame.draw.rect(screen, "green", pipe_pair["top"])
        pygame.draw.rect(screen, "green", pipe_pair["bottom"])

    bird_pos.y += bird_velocity_y
    bird_velocity_y += gravity

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird_velocity_y = jump_force

    pygame.draw.circle(screen, "yellow", bird_pos, 30)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
