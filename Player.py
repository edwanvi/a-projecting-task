import pygame
import constants
import arena


class Player(pygame.sprite.Sprite):
    """docstring for Player."""
    def __init__(self):
        super(Player, self).__init__()
        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.WHITE)
        # We need to tell pygame about the image we had it make.
        self.rect = self.image.get_rect()
        # hp
        self.health = 100
        # Speed variables
        self.change_x = 0
        self.change_y = 0
        # What can we hit?
        self.level = None

    def update(self):
        self.calc_grav()
        # move player by change_x
        self.rect.x += self.change_x
        # See if we hit anything and handle it
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        # moves along y according to change_y (gravity calculations tbd)
        self.rect.y += self.change_y
        # recalulate collision since we move x then move y. it makes sense if you don't think about it.
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Stop our vertical movement
            self.change_y = 0

    # Gravity calculations
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # see if we are on the bottom of the screen.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    ### PLAYER CONTROL METHODS ###
    def jump(self):
        # Called when you, well, jump
        # make sure we have something to jump off of
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        """Called when the user hits the left arrow."""
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """Called when the user hits the right arrow."""
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """Called when the user lets off the keyboard. Doesn't change direction."""
        self.change_x = 0
