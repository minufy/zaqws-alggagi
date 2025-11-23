import sys
import pygame
from enum import Enum
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

UNIT = 32
COLOR_BG = "#000000"
COLOR_FG = "#b9b9b9"
COLOR_WHITE = "#eeeeee"
COLOR_BLACK = "#222222"
COLOR_BOARD = "#ffc17a"

BOARD_SIZE = UNIT * 19
OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE) / 2
OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE) / 2

class Type(Enum):
    WHITE = COLOR_WHITE
    BLACK = COLOR_BLACK

class Al:
    def __init__(self, x, y, type):
        global total_index
        self.index = (total_index := total_index + 1)
        self.x = x
        self.y = y
        self.type = type
        self.velocity = pygame.Vector2(0, 0)

total_index = 0
al_list = [
    Al(10, 10, Type.WHITE),
    Al(50, 50, Type.BLACK),
]
FRICTION = 0.9

def collision(a, b):
    if (a.x - b.x) ** 2 + (a.y - b.y) ** 2 <= UNIT ** 2:
        return True
    return False

def draw_al(al_list):
    for al in al_list:
        pygame.draw.circle(screen, al.type.value, (al.x + OFFSET_X, al.y + OFFSET_Y), UNIT / 2)

def update_al(al_list: list[Al]):
    for al in al_list:
        al.x += al.velocity.x
        al.y += al.velocity.y
        al.velocity.x *= FRICTION
        al.velocity.y *= FRICTION
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
    for x in range(19 + 1):
        pygame.draw.line(screen, COLOR_BG, (x * UNIT + OFFSET_X, OFFSET_Y), (x * UNIT + OFFSET_X, BOARD_SIZE + OFFSET_Y), 1)
    for y in range(19 + 1):
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

    screen.fill(COLOR_FG)
    draw_board()

    draw_al(al_list)
    update_al(al_list)

    pygame.display.update()
    clock.tick(60)