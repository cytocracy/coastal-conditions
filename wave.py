import pygame

pygame.init()

WINDOW_SIZE = (600, 400)
 
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

COLS = 20
C=1
H=1
STEP = .1

u = []
u_new = []
v = []
for i in range(COLS):
    u.append(10)

for i in range(COLS):
    v.append(0)

def simulate():
    for i in range(COLS):
        f = C*C*(u[i-1] + u[i+1] - 2*u[i])/(h*h)
        v[i] = v[i] + f*STEP
        u_new[i] = u[i] + v[i]*STEP
    for i in range(COLS):
        u[i] = u_new[i]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))
    
    pygame.display.flip()


pygame.quit()
    






