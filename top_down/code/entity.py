import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, hitbox):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 6
        self.direction = pygame.math.Vector2()
        self.hitbox = hitbox
        self.hitbox_pos_x = self.hitbox.x
        self.hitbox_pos_y = self.hitbox.y

    def move(self, speed, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox_pos_x = self.hitbox.x
        self.hitbox_pos_y = self.hitbox.y
        self.hitbox_pos_x += self.direction.x * (speed * dt)
        self.hitbox_pos_y += self.direction.y * (speed * dt)
        self.hitbox.x = round(self.hitbox_pos_x)
        self.hitbox.y = round(self.hitbox_pos_y)
        self.collision()
        self.speed_modifiers()
        self.rect.center = self.hitbox.center

    def collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacle_sprites, False)
        if self.direction.x != 0:
            for sprite in collision_sprites:
                # collision on the right
                if self.hitbox.right >= sprite.hitbox.left and self.old_hitbox.right <= sprite.old_hitbox.left:
                    self.hitbox.right = sprite.hitbox.left

                # collision on the left
                if self.hitbox.left <= sprite.hitbox.right and self.old_hitbox.left >= sprite.old_hitbox.right:
                    self.hitbox.left = sprite.hitbox.right

        if self.direction.y != 0:
            for sprite in collision_sprites:
                # collision on top
                if self.hitbox.bottom >=  sprite.hitbox.top and self.old_hitbox.bottom <= sprite.old_hitbox.top:
                    self.hitbox.bottom = sprite.hitbox.top

                # collision on bottom
                if self.hitbox.top <= sprite.hitbox.bottom and self.old_hitbox.top >= sprite.old_hitbox.bottom:
                    self.hitbox.top = sprite.hitbox.bottom

                    
    def speed_modifiers(self):
        self.speed = self.stats['speed']
        for sprite in self.slow_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                self.speed = self.stats['speed'] * 0.9