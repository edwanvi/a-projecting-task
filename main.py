#!/usr/bin/env python
# coding=utf-8
from Player import Player
from arena import *
import utils


def main():
    print("Starting up...")
    # init pygame
    pygame.init()
    font = pygame.font.Font(None, 36)
    # create and title screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('the game begins')
    # instance of player
    print("Creating player...")
    player = Player()
    # create arena
    print("Creating arena...")
    arena = Arena(player)
    # set player level
    player.level = arena
    # difficulty should scale with time
    difficulty = 0.01
    # list of sprites to draw
    active_list = pygame.sprite.Group()

    player.rect.x = 340
    # place player on ground
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_list.add(player)

    # loop control switch
    done = False
    # clockem sockem robots
    clock = pygame.time.Clock()

    # main loop
    # it's loopy
    while not done:
        for event in pygame.event.get():
            # Handle events
            if event.type == pygame.QUIT:
                print("Shutting down...")
                done = True
                print("Score: " + str(utils.calculate_score(player.killcount, pygame.time.get_ticks())))
            elif event.type == pygame.KEYDOWN:
                # handle key inputs
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()
                elif event.key == pygame.K_SPACE:
                    player.fire()
            elif event.type == pygame.KEYUP:
                # key is released
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_w:
                    player.stop()
                if event.key == pygame.K_SPACE:
                    player.fire()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            player.fire()
        # update sprite lists
        active_list.update()
        player.level.update()
        # check if player is dead after updates
        if player.health <= 0:
            done = True
            print("You died!")
            print("Score: " + str(utils.calculate_score(player.killcount, pygame.time.get_ticks())))
        # scrolling
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            player.level.shift_world(-diff)
        elif player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            player.level.shift_world(diff)
        # Keeping the player away from the edges
        if player.rect.right > constants.SCREEN_WIDTH:
            player.rect.right = constants.SCREEN_WIDTH
        elif player.rect.left < 0:
            player.rect.left = 0

        # ALL DRAWING BELOW THIS LINE
        player.level.draw(screen)
        active_list.draw(screen)
        # ALL DRAWING ABOVE THIS LINE

        # 60 FPS cap
        clock.tick(60)

        # Did you notice that everything was upside-down? OF COURSE NOT!
        pygame.display.flip()

if __name__ == "__main__":
    main()
