import os
import neat
import pygame
import sys
from game import Bird, Pipe

generation = 0

simulation_steps_per_frame = 1
simulation_dt = 1 / 60

minus_button = pygame.Rect(15, 100, 40, 40)
plus_button = pygame.Rect(145, 100, 40, 40)


def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))


def eval_genomes(genomes, config):
    global simulation_steps_per_frame
    global generation
    generation += 1
    score = 0

    birds = []
    nets = []
    ge = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0.0

        birds.append(Bird())
        nets.append(net)
        ge.append(genome)

    pipes = [Pipe()]
    pipe_spawn_time = 1.5
    pipe_timer = 0

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 50)
    button_font = pygame.font.SysFont("Arial", 36)
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    running = True

    while running and len(birds) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (mouse_pos >= (15, 100) and mouse_pos <= (65, 140)):
                    simulation_steps_per_frame = clamp(
                        simulation_steps_per_frame - 1, 1, 8)
                if (mouse_pos >= (145, 100) and mouse_pos <= (185, 140)):
                    simulation_steps_per_frame = clamp(
                        simulation_steps_per_frame + 1, 1, 8)

        for _ in range(simulation_steps_per_frame):
            if not running or len(birds) == 0:
                break

            pipe_index = 0
            if len(pipes) > 1 and birds[0].pos.x > pipes[0].top_pipe.right:
                pipe_index = 1

            for i, bird in enumerate(birds):
                ge[i].fitness += 0.1
                pipe = pipes[pipe_index]

                output = nets[i].activate((
                    bird.velocity,
                    bird.pos.y,
                    pipe.x - bird.pos.x,
                    pipe.gap_y,
                    pipe.gap_y + pipe.gap_size
                ))

                if output[0] > 0.5:
                    bird.jump()

                bird.update()

            for pipe in pipes:
                pipe.update(simulation_dt)

            pipe_timer += simulation_dt
            if pipe_timer >= pipe_spawn_time:
                pipes.append(Pipe())
                pipe_timer = 0

            pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]

            for i in range(len(birds) - 1, -1, -1):
                bird = birds[i]

                hit_pipe = False
                for pipe in pipes:
                    if pipe.collides_with(bird):
                        hit_pipe = True

                if bird.pos.y > height or bird.pos.y < 0 or hit_pipe:
                    ge[i].fitness -= 1
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

            for pipe in pipes:
                if not pipe.scored and len(birds) > 0 and birds[0].pos.x > pipe.top_pipe.right:
                    pipe.scored = True
                    score += 1

                    for genome in ge:
                        genome.fitness += 5

        screen.fill("#70C5CE")

        for bird in birds:
            bird.draw()
        for pipe in pipes:
            pipe.draw()

        gen_surface = font.render(
            f"gen: {generation}", False, (255, 255, 255))
        screen.blit(gen_surface, (15, 15))

        score_surface = font.render(
            f"{score}", False, (255, 255, 255))
        screen.blit(score_surface, (width / 2, 15))

        speed_surface = font.render(
            f"{simulation_steps_per_frame}x", False, (255, 255, 255))
        speed_rect = speed_surface.get_rect(
            center=(100, minus_button.centery))
        screen.blit(speed_surface, speed_rect)

        pygame.draw.rect(screen, "white", minus_button)
        pygame.draw.rect(screen, "white", plus_button)

        minus_text = button_font.render("-", True, "black")
        minus_rect = minus_text.get_rect(center=minus_button.center)
        screen.blit(minus_text, minus_rect)

        plus_text = button_font.render("+", True, "black")
        plus_rect = plus_text.get_rect(center=plus_button.center)
        screen.blit(plus_text, plus_rect)

        pygame.display.flip()
        clock.tick(60)

    print(f"Generation {generation} score: {score}")


def run_neat(config_path):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 100000)

    print("Best genome:")
    print(winner)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-bird.txt")
    run_neat(config_path)
