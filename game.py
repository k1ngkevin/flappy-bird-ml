import pygame
import random

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 50)
width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


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


class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, 500)
        self.x = width
        self.gap_size = 200
        self.width = 60
        self.scored = False
        self.top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y)
        self.bottom_pipe = pygame.Rect(self.x, self.gap_y + self.gap_size, self.width,
                                       height - (self.gap_y + self.gap_size))

    def update(self, dt):
        self.x -= pipe_speed * dt
        self.top_pipe.x = int(self.x)
        self.bottom_pipe.x = int(self.x)

    def draw(self):
        pygame.draw.rect(screen, "green", self.top_pipe)
        pygame.draw.rect(screen, "green", self.bottom_pipe)

    def is_off_screen(self):
        return self.top_pipe.right <= 0

    def collides_with(self, bird):
        return (
            check_collision(bird.pos, bird.radius, self.top_pipe)
            or check_collision(bird.pos, bird.radius, self.bottom_pipe)
        )

    def score_if_passed(self, bird):
        if not self.scored and bird.pos.x > self.top_pipe.right:
            self.scored = True
            return True
        return False


def check_collision(circle_pos, circle_radius, rect):
    closest_x = max(rect.left, min(circle_pos[0], rect.right))
    closest_y = max(rect.top, min(circle_pos[1], rect.bottom))
    closest_point = pygame.math.Vector2(closest_x, closest_y)

    circle_center = pygame.math.Vector2(circle_pos)
    distance = circle_center.distance_to(closest_point)
    return distance <= circle_radius


pipe_spawn_time = 1.5
pipe_speed = 300

gravity = 0.5
jump_force = -8


def main():
    running = True
    dt = 0
    pipes = []
    pipe_timer = 0
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
                    bird.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bird.jump()

        screen.fill("#70C5CE")

        pipe_timer += dt
        if pipe_timer >= pipe_spawn_time:
            pipes.append(Pipe())
            pipe_timer = 0

        for pipe in pipes:
            pipe.update(dt)

        pipes = [
            pipe for pipe in pipes
            if not pipe.is_off_screen()
        ]

        for pipe in pipes:
            pipe.draw()

        bird.update()

        is_collision = False

        for pipe in pipes:
            if pipe.collides_with(bird):
                is_collision = True
                break

        if bird.pos.y > height or bird.pos.y < 0 or is_collision:
            print("game end")
            break

        bird.draw()

        for pipe in pipes:
            if pipe.score_if_passed(bird):
                score += 1
                break

        score_surface = font.render(f"{score}", False, (255, 255, 255))
        screen.blit(score_surface, (width / 2, 35))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    print(f"score: {score}")
    pygame.quit()


if __name__ == "__main__":
    main()
