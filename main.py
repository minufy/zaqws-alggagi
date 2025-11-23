import sys
import pygame
from enum import Enum

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

UNIT = 32
BOARD_SIZE = UNIT * (19 - 1)

MAX_VELOCITY = UNIT * 30
FRICTION = 0.9

OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE) / 2
OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE) / 2

COLOR_BG = "#000000"
COLOR_FG = "#b9b9b9"
COLOR_WHITE = "#eeeeee"
COLOR_BLACK = "#222222"
COLOR_BOARD = "#ffc17a"

class Type(Enum):
    WHITE = COLOR_WHITE
    BLACK = COLOR_BLACK

class Al:
    def __init__(self, x, y, type):
        self.index = len(al_list)
        self.x = x
        self.y = y
        self.type = type
        self.velocity = pygame.Vector2(0, 0)

al_list = []
for i in range(5):
    al_list.append(Al(UNIT * 1 + i * UNIT * 4, UNIT * 3, Type.WHITE))
    al_list.append(Al(UNIT * 1 + i * UNIT * 4, BOARD_SIZE - UNIT * 3, Type.BLACK))

def collision(a, b):
    if (a.x - b.x) ** 2 + (a.y - b.y) ** 2 <= UNIT ** 2:
        return True
    return False

def draw_al(al_list):
    for al in al_list:
        pygame.draw.circle(screen, al.type.value, (al.x + OFFSET_X, al.y + OFFSET_Y), UNIT / 2)

def update_al(al_list: list[Al]):
    for i, al in enumerate(al_list[:]):
        al.x += al.velocity.x
        al.y += al.velocity.y
        al.velocity.x *= FRICTION
        al.velocity.y *= FRICTION
        if al.x + UNIT < 0 or al.x - UNIT > BOARD_SIZE or al.y + UNIT < 0 or al.y - UNIT > BOARD_SIZE:
            al_list.pop(i)
        for other_al in al_list:
            if al == other_al:
                continue
            if collision(al, other_al):
                collision_vector = pygame.Vector2(al.x - other_al.x, al.y - other_al.y).normalize()
                collision_vector *= al.velocity.length()
                other_al.velocity -= collision_vector
                al.velocity += collision_vector

def draw_board():
    pygame.draw.rect(screen, COLOR_BOARD, (OFFSET_X - UNIT, OFFSET_Y - UNIT, BOARD_SIZE + UNIT * 2, BOARD_SIZE + UNIT * 2))
    for x in range(19):
        pygame.draw.line(screen, COLOR_BG, (x * UNIT + OFFSET_X, OFFSET_Y), (x * UNIT + OFFSET_X, BOARD_SIZE + OFFSET_Y), 1)
    for y in range(19):
        pygame.draw.line(screen, COLOR_BG, (OFFSET_X, y * UNIT + OFFSET_Y), (BOARD_SIZE + OFFSET_X, y * UNIT + OFFSET_Y), 1)

selected_al = None
click_x = 0
click_y = 0
def click():
    global selected_al, click_x, click_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x -= OFFSET_X
    mouse_y -= OFFSET_Y
    for al in al_list:
        if (al.x - mouse_x) ** 2 + (al.y - mouse_y) ** 2 <= UNIT ** 2:
            selected_al = al
            click_x = mouse_x
            click_y = mouse_y
            return
    selected_al = None

def fire():
    global selected_al, click_x, click_y
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x -= OFFSET_X
    mouse_y -= OFFSET_Y
    if selected_al:
        selected_al.velocity.x = (click_x - mouse_x) / 10
        selected_al.velocity.y = (click_y - mouse_y) / 10
    selected_al = None

ais = {}
def init_ais(ai_white, ai_black):
    global ais
    ais[Type.WHITE] = ai_white
    ais[Type.BLACK] = ai_black

def validate(al, vector, type):
    if al.type != type:
        return False
    if vector.length() > MAX_VELOCITY:
        return False
    return True

turn_index = 0
def next_turn():
    global turn_index
    type = Type.WHITE if turn_index % 2 == 0 else Type.BLACK
    al, vector = ais[type].think(al_list)
    if validate(al, vector, type):
        al.velocity = vector
    turn_index += 1

from testai import TestAI
init_ais(TestAI(Type.WHITE), TestAI(Type.BLACK))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                fire()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                next_turn()

    screen.fill(COLOR_FG)
    draw_board()

    draw_al(al_list)
    update_al(al_list)

    pygame.display.update()
    clock.tick(60)