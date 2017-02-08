import pygame
import constants
import arena


class Player(pygame.sprite.Sprite):
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
        # direction for bullets
        self.direction = "R"
        self.killcount = 0
        self.invul = False
        self.invultime = 0
        # cooldown on firing
        self.cooldown = 0

    def update(self):
        self.calc_grav()
        if self.invultime > 0:
            self.invul -= 1
        self.cooldown -= 1
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

    # PLAYER CONTROL METHODS #
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

    def fire(self):
        if self.cooldown <= 0:
            bull = Bullet(self)
            bull.rect.x = self.rect.x
            bull.rect.y = self.rect.y
        else:
            pass

    def set_invul(self, invul, time=120):
        self.invul = invul
        if invul:
            self.invultime = time


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player: Player):
        super(Bullet, self).__init__()
        self.player = player
        self.direction = player.direction
        self.change_x, self.change_y = (0, 0)
        # image creation
        width = 20
        height = 20
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.LIGHTBLUE)
        # We need to tell pygame about the image we had it make.
        self.rect = self.image.get_rect()
        self.player.level.other_list.add(self)

    def update(self):
        if self.change_x == 0 and self.change_y == 0:
            if self.direction == "R":
                self.change_x = 3
            elif self.direction == "L":
                self.change_x = -3
            if self.player.change_y != 0:
                self.change_y = 3
                self.player.change_y -= 2  # because physics
                self.player.cooldown += 15
            self.player.cooldown += 15
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        collided_things = pygame.sprite.spritecollide(self, self.player.level.enemy_list, True)
        if len(collided_things) > 0:
            self.kill()
            self.player.killcount += 1
