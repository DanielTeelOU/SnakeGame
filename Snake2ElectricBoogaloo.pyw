import math # for calculations
import random # for snack placement
import pygame # to build the game
from pygame.locals import * # for menu
import tkinter as tk # for message box
from tkinter import messagebox # for message box
import sys # for menu / scores
import os # for menu / scores

# for the geometry
class cube(object):
    rows = 20
    w = 500
    
    # on game start, snake head color
    def __init__(self, start, dirnx=1, dirny=0, color = (254, 1, 154)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        pygame.display.set_caption('Snake 2: Electric Boogaloo')
    # movement of snake
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    # determining position of the cube
    def draw(self, surface):
        dis = self.w // self.rows # dimensions of the cube
        i = self.pos[0] # row
        j = self.pos[1] # column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2)) # determines where to draw the cube
        
# for the game logic
class snake(object):
    body = []
    turns = {}

    # sets snake head
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    # movement and game exit
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)

    # if retry is selected after failure. This is in the message box
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    # grow after snack is eaten
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
    # actually make it
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface)
            else:
                c.draw(surface)

# draws the lines to make it look like an actual grid
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (70, 102, 255), (x, 0),(x, w))
        pygame.draw.line(surface, (70, 102, 255), (0, y),(w, y))
        
# show the graphics
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

# make the snack appear in a random position within the grid
def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
        
    return (x, y)

# pops up on failure
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# the main method that runs the actual game
def main():
    global width, rows, s, snack, start
    width = 500
    rows = 20
    start = 8
    win = pygame.display.set_mode((width, width))
    s = snake((78, 253, 84), (10, 10)) # snake color
    snack = cube(randomSnack(rows, s), color=(85, 255, 0)) # snack starting color
    flag = True

    clock = pygame.time.Clock()
    
    while flag:
        pygame.time.delay(10) # game delay
        clock.tick(start) # fps / speed
        s.move()

        # ranks
        if 1 < len(s.body) <= 5:
            rank = 'n Uncultured Swine'
        if 6 <= len(s.body) <= 15:
            rank = ' Novice'
        if 16 <= len(s.body) <= 20:
            rank = 'n Average Gamer'
        if 21 <= len(s.body) <= 30:
            rank = ' Respectable Gamer'
        if 31 <= len(s.body) <= 40:
            rank = ' Gemini Man'
        if 41 <= len(s.body) <= 50:
            rank = ' Retro God'

        if s.body[0].pos == snack.pos:
            s.addCube()
            start = 8 + len(s.body)
            snack = cube(randomSnack(rows, s), color=(85, 255, 0)) # respawned snack color

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                start = 8
                message_box("Game Over", 'Your score was ' + str(len(s.body)) + ' points.' + '\nYou are a' + rank + ".\nWould you like to retry?") # message box content. Shows score and asks the player if they wanna replay
                s.reset((10, 10)) # if the ok option is clicked
                break

        redrawWindow(win) # show things on the screen

main()