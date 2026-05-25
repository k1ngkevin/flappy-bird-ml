import os
import neat
import pygame
from game import Bird, Pipe


def eval_genomes(genomes, config):
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
    score = 0
    dt = 0
    pipe_spawn_time = 1.5
    pipe_timer = 0

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 50)
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    running = True
    while running and len(birds) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill("#70C5CE")

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
            pipe.update(dt)

        pipe_timer += dt
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

        for bird in birds:
            bird.draw()
        for pipe in pipes:
            pipe.draw()

        for pipe in pipes:
            if not pipe.scored and len(birds) > 0 and birds[0].pos.x > pipe.top_pipe.right:
                pipe.scored = True
                for genome in ge:
                    genome.fitness += 5

        # for pipe in pipes:
        #     if pipe.score_if_passed(bird):
        #         score += 1
        #         break

        # score_surface = font.render(f"{score}", False, (255, 255, 255))
        # screen.blit(score_surface, (width / 2, 35))

        pygame.display.flip()
        dt = clock.tick(60) / 1000


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

    winner = population.run(eval_genomes, 100)

    print("Best genome:")
    print(winner)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-bird.txt")
    run_neat(config_path)
