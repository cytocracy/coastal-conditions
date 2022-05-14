import pygame
from pygame import *
import random



pygame.init()

WINDOW_WIDTH = 600
WIDNOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, WIDNOW_HEIGHT)
 
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

COLS = 50
C=1
H=WINDOW_WIDTH/COLS
STEP = .1

u = []
u_new = []
v = []
for i in range(COLS):
    u.append(200)
    if(i==3): v.append(10)
    else: v.append(0)
    
    u_new.append(0)

  

def simulate():
    global u
    global u_new
    global v

    for i in range(COLS):
        f = 0
        if(i == 0):
            # f = C*C*(u[i+1] + u[COLS-1] - 2*u[i])/(H*H)
            pass
        elif(i==COLS-1): 
            # f = C*C*(u[i-1]+u[0] - 2*u[i])/(H*H)
            pass
        else:
            f = C*C*(u[i-1] + u[i+1] - 2*u[i])/(H*H)
        v[i] = v[i] + f*STEP
        u_new[i] = u[i] + v[i]*STEP
    for i in range(COLS):
        u[i] = u_new[i]

running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_SPACE:
            v[3] = 5;
    screen.fill((255,255,255))
    simulate()
    for i in range(COLS):
        pygame.draw.rect(screen, (0,0,255), Rect(i*H, WIDNOW_HEIGHT-u[i], H, u[i]))
        # pygame.draw.rect(screen, (0,0,255), Rect(i*H, 50, H, 30))
    
    pygame.display.flip()


pygame.quit()
    






