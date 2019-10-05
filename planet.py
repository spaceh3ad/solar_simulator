import pygame
from pygame.math import Vector2
import logging, sys

class Body():

    def __init__(self, game, position, velocity, mass, radius, color):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.game = game
        self.x, self.y = position
        self.a, self.b = velocity

        self.position = Vector2(self.x,self.y)
        self.velocity = Vector2(self.a, self.b)
        self.mass = mass
        self.radius = radius
        self.color = color
        
        self.tail = []

        self.acceleration = Vector2(0,0)

    def add_force(self,vector):
        self.acceleration = -vector*0.0008

    def tick(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.x, self.y = self.position


    def draw(self):
        for i in self.tail:
            pygame.draw.circle(self.game.screen, (255,255,255), i, 0)
        pygame.draw.circle(self.game.screen, self.color, (int(self.x),int(self.y)), int(self.radius))
        self.tailor()
        
    def tailor(self):
        self.tail.append((int(self.x),int(self.y)))
        if len(self.tail) > 500:
            del self.tail[0]
