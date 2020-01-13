import sys
import os
import pygame

# user inputs
import config
from fish import Fish
from fish_list import FishList
from pipe_list import PipeList

# Setup screen ================================================================

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption('Flappy Fish')
bg = pygame.image.load(os.path.join("flappy_fish", "images", "underwater.png"))

# Game variables ==============================================================

fish_list = FishList()
pipe_list = PipeList()
gen_num = 1
font = pygame.font.Font("freesansbold.ttf", 20)
c = 0

# Start game loop =============================================================
while 1:
    # Make sure pygame quits on signal
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Update cycle ============================================================

    # check for collision or off screen
    fish_list.check_alive(pipe_list)
    # Update bird if it is alive
    pipe_info = pipe_list.update()
    fish_list.update(pipe_info)

    # Reset ===================================================================

    if len(fish_list.alive) == 0:
        # pygame.time.wait(500)
        fish_list.next_generation()
        pipe_list = PipeList()
        gen_num += 1

    # Draw Frame ==============================================================
    if c % 10 == 0:
        screen.blit(bg, (0,0))
        pipe_list.draw(screen)
        fish_list.draw(screen)
        text = font.render(f"gen: {gen_num} score: {fish_list.alive[0].score} ({fish_list.max_score})",
                        True, (250, 250, 200), None)
        text_rect = text.get_rect()
        text_rect.center = (config.WIDTH // 2, 30)
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(10)
    c += 1
