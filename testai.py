# testai
# made by minufy

import pygame
import random
import time

def dist(a, b):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

class TestAI:
    def __init__(self, type):
        self.type = type
        random.seed(time.time())

    def think(self, al_list):
        my_al_list = [al for al in al_list if al.type == self.type]
        my_al = random.choice(my_al_list)
        min_d = float("inf")
        other_al = None
        for al in al_list:
            if al.type != self.type:
                d = dist(my_al, al)
                if d < min_d:
                    min_d = d
                    other_al = al

        velocity_vector = -pygame.Vector2(my_al.x - other_al.x, my_al.y - other_al.y).normalize() * min_d * 0.13
        return my_al, velocity_vector