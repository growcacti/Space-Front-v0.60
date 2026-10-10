import pygame as pg
import random
import math
from math import tan, copysign
from math import pi, hypot, cos, sin, atan2, degrees, radians
from pygame.math import Vector2
from constants import Constants

c = Constants
screen = c.screen


LERP_FACTOR = 0.0001
minimum_distance = 250

maximum_distance = 250000000000


class Nme:
    def __init__(self, image, x, y):
        self.x = x
        self.y = y
        self.max_rotation = 1
        self.max_acceleration = 5.0
        self.orig_image = image
        self.font = pg.font.Font(None, 18)
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = 0.0
        self.length = 4
        self.max_acceleration = 2.0

        self.max_velocity = 50
        self.thrust = 50
        self.sim_inertia = 50  # iner

        self.acceleration = 1
        self.rotation = 0.0

        self.direction = Vector2(0, 0)

        self.rect3 = pg.Rect(self.image.get_rect(center=self.rect.center))
        self.hitbox = pg.draw.rect(screen, (0, 200, 255), self.rect3, 3)
        self.group = []

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(
            -self.max_velocity, min(self.velocity.x, self.max_velocity)
        )

        angular_velocity = 0
        vel = self.velocity * dt
        self.position += vel

        self.rect.center = self.position
        self.angle += degrees(angular_velocity) * dt

        self.image = pg.transform.rotozoom(self.orig_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect3 = pg.Rect(self.rect)
        self.hitbox = pg.draw.rect(self.image, (255, 255, 0), self.rect3, 3)
        self.direction = pg.Vector2(1, 0).rotate(-self.angle)

    def move_towards_player(self, pos, ang):
        distance = self.position.distance_to(pos)
        if distance > minimum_distance:
            direction_vector = (pos - self.position) / distance
            min_step = max(0, distance - maximum_distance)
            max_step = distance - minimum_distance
            step_distance = min_step + (max_step - min_step) * LERP_FACTOR
            self.position = self.position + direction_vector * step_distance

        speed = self.velocity.length() / 10000

        # Calculate the direction vector
        direction_vector = pos - self.position

        # Normalize the direction vector
        direction_vector.normalize()

        # Calculate the angle in radians and then convert to degrees
        rad = atan2(-direction_vector.y, direction_vector.x)
        self.angle = degrees(rad)

        # Rotate the enemy sprite
        self.image = pg.transform.rotozoom(self.orig_image, self.angle, 1)
        self.position += direction_vector * speed
