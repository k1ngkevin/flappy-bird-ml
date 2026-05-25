import pygame
import random

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 50)
width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

class Bird:
    def __init__(self):
        self.pos = pygame.math.Vector2(width / 2, height / 2)
        self.velocity = 0
        self.radius = 30
        self.alive = True
    
    def jump(self):
        self.velocity = jump_force
    
    def update(self):
        self.pos.y += self.velocity
        self.velocity += gravity
    
    def draw(self):
        pygame.draw.circle(screen, "yellow", self.pos, self.radius)


def check_collision(circle_pos, circle_radius, rect):
    closest_x = max(rect.left, min(circle_pos[0], rect.right))
    closest_y = max(rect.top, min(circle_pos[1], rect.bottom))
    closest_point = pygame.math.Vector2(closest_x, closest_y)

    circle_center = pygame.math.Vector2(circle_pos)
    distance = circle_center.distance_to(closest_point)
    return distance <= circle_radius
    

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

gravity = 0.5
jump_force = -10
bird = Bird()

score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                bird.velocity = jump_force
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bird.velocity = jump_force

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

    bird.pos.y += bird.velocity
    bird.velocity += gravity

    is_collision = False 

    for pipe_pair in pipes:
        if (
            check_collision(bird.pos, bird.radius, pipe_pair["top"]) 
            or check_collision(bird.pos, bird.radius, pipe_pair["bottom"])
        ):
            is_collision = True;
            break;

    if bird.pos.y > height or bird.pos.y < 0 or is_collision:
        print("game end")
        break
    
    pygame.draw.circle(screen, "yellow", bird.pos, bird.radius)

    for pipe_pair in pipes:
        if pipe_pair["scored"] == False and bird.pos.x > pipe_pair["top"].x:
            score += 1
            pipe_pair["scored"] = True 
            break
    
    score_surface = font.render(f"{score}", False, (255, 255, 255))
    screen.blit(score_surface, (width / 2, 35))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

print(f"score: {score}")
pygame.quit()
