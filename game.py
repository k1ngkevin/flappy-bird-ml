import pygame
import random
from pathlib import Path

base_dir = Path(__file__).parent
asset_dir = base_dir / "bird-assets"


pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 50)
width, height = 1280, 720

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

bird_sheet = pygame.image.load(
    str(asset_dir / "Player" / "StyleBird1" / "Bird1-1.png")).convert_alpha()

bird_frame_rect = pygame.Rect(0, 0, 16, 16)
bird_img = bird_sheet.subsurface(bird_frame_rect)
bird_img = pygame.transform.scale(bird_img, (60, 60))

background_img = pygame.image.load(
    str(asset_dir / "Background" / "Background7.png")).convert()
background_img = pygame.transform.scale(background_img, (width, height))

pipe_sheet = pygame.image.load(
    str(asset_dir / "Tiles" / "Style 1" / "PipeStyle1.png")
).convert_alpha()

tile_width = 32
tile_height = 80

row = 0
col = 2

pipe_top_rect = pygame.Rect(
    col * tile_width,
    row * tile_height,
    tile_width,
    15,
)

pipe_bottom_rect = pygame.Rect(
    col * tile_width,
    65,
    tile_width,
    15,
)

pipe_middle_rect = pygame.Rect(
    col * tile_width,
    15,
    tile_width,
    50,
)

pipe_top_img = pipe_sheet.subsurface(pipe_top_rect)
pipe_bottom_img = pipe_sheet.subsurface(pipe_bottom_rect)
pipe_middle_img = pipe_sheet.subsurface(pipe_middle_rect)


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
        bird_rect = bird_img.get_rect(center=self.pos)
        screen.blit(bird_img, bird_rect)


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
        cap_height = int(15 * (self.width / tile_width))

        top_body_rect = pygame.Rect(
            self.top_pipe.x,
            self.top_pipe.y,
            self.top_pipe.width,
            max(0, self.top_pipe.height - cap_height),
        )
        top_cap_rect = pygame.Rect(
            self.top_pipe.x,
            self.top_pipe.bottom - cap_height,
            self.top_pipe.width,
            cap_height,
        )
        bottom_cap_rect = pygame.Rect(
            self.bottom_pipe.x,
            self.bottom_pipe.y,
            self.bottom_pipe.width,
            cap_height,
        )
        bottom_body_rect = pygame.Rect(
            self.bottom_pipe.x,
            self.bottom_pipe.y + cap_height,
            self.bottom_pipe.width,
            max(0, self.bottom_pipe.height - cap_height),
        )

        if top_body_rect.height > 0:
            top_body = pygame.transform.scale(
                pipe_middle_img,
                (top_body_rect.width, top_body_rect.height),
            )
            screen.blit(top_body, top_body_rect)

        top_cap = pygame.transform.scale(
            pipe_bottom_img,
            (top_cap_rect.width, top_cap_rect.height),
        )
        screen.blit(top_cap, top_cap_rect)

        bottom_cap = pygame.transform.scale(
            pipe_top_img,
            (bottom_cap_rect.width, bottom_cap_rect.height),
        )
        screen.blit(bottom_cap, bottom_cap_rect)

        if bottom_body_rect.height > 0:
            bottom_body = pygame.transform.scale(
                pipe_middle_img,
                (bottom_body_rect.width, bottom_body_rect.height),
            )
            screen.blit(bottom_body, bottom_body_rect)

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

        screen.blit(background_img, (0, 0))

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
