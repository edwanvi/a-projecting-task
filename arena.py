import pygame
import constants
import enemy


# Class for platforms, can be of arbitrary width and height
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLACK)
        self.rect = self.image.get_rect()


class Arena(object):
    def __init__(self, player):
        # Constructor, pass in a player please. (for moving platforms)
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        newenemy = enemy.Enemy("dark")
        newenemy.rect.x, newenemy.rect.y = (10, 100)
        newenemy.level = self
        self.enemy_list.add(newenemy)
        self.player = player
        # BG Image
        self.background = None
        # How far we've come in the world of scrolling.
        self.world_shift = 0
        self.level_limit = -1000
        newplat = Platform(10, 10)
        newplat.rect.x = 10
        newplat.rect.y = 550
        self.platform_list.add(newplat)

    def update(self):
        # Update things.
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        #Draw a level
        screen.fill(constants.BLUE)
        #Draw the sprites
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        #As we move, we need to scroll along with the player.
        self.world_shift += shift_x

        #Go through all the lists and render as needed
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
