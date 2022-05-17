import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
import random
import math

VIEW_WIDTH = 800
VIEW_HEIGHT = 600
DAM_PARTICLES = 100

G = [0.0, -9.8]
REST_DENS = 300.0
GAS_CONST = 2000.0
H = 16
HSQ = H * H
MASS = 2.5
VISC = 200.0
DT = 0.0007

POLY6 = 4.0 / (math.pi * pow(H, 8.0))
SPIKY_GRAD = -10.0 / (math.pi * pow(H, 5.0))
VISC_LAP = 40.0 / (math.pi * pow(H, 5.0))

EPS = int(H)
BOUND_DAMPING = -0.5

particles = []

class Particle:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.vel = [0, 0]
        self.force = [0, 0]
        self.rho = 0
        self.prs = 0
    # vector = numpy.linalg.


def init_gl():
    glClearColor(0.9, 0.9, 0.9, 1.)
    glEnable(GL_POINT_SMOOTH)
    glPointSize(H/2.0)
    glMatrixMode(GL_PROJECTION)

def init_sph():
    
    for y in range(EPS, VIEW_HEIGHT - EPS * 2, H):
        for x in range(int(VIEW_WIDTH / 4), int(VIEW_WIDTH /2), H):
            if len(particles) < DAM_PARTICLES:
                jitter = random.uniform(-.2, .2)
                particles.append(Particle(x + jitter, y))
            else: return

def compute_density_pressure():
    for pi in particles:
        pi.rho = 0
        for pj in particles:
            rij = pj.pos-pi.pos
            r2 = rij.squared_norm()

            if r2 < HSQ:
                pi.rho += MASS * POLY6 * pow(HSQ-r2, 3)
        pi.p = GAS_CONST * (pi.rho - REST_DENS)


def compute_forces():
    for pi in particles:
        fpress = [0., 0.]
        fvisc = [0., 0.]
        for pj in particles:
            if pj == pi: continue
            rij = pj.pos - pi.pos
            r = rij.norm()

            if r < H:
                fpress = -rij.normalized() * MASS * (pi.prs + pj.prs) / (2.0 * pj.rho) * SPIKY_GRAD * pow(H-r, 3)
                fvisc += VISC * MASS * (pj.vel-pi.vel) / pj.rho * VISC_LAP * (H-r)
        fgrav = G * MASS / pi.rho
        pi.force = fpress + fvisc + fgrav

def integrate():
    for p in particles:
        p.vel += DT * p.force / p.rho
        p.pos += DT * p.v

        if(p.pos[0] - EPS < 0.0):
            p.vel[0] *= BOUND_DAMPING
            p.pos[0] = EPS
        if p.pos[0] + EPS > VIEW_WIDTH:
            p.vel[0] *= BOUND_DAMPING
            p.pos[0] = VIEW_WIDTH - EPS
        if p.pos[1] - EPS < 0.0:
            p.vel[1] *= BOUND_DAMPING
            p.pos[1] = EPS
        if p.pos[1] + EPS > VIEW_HEIGHT:
            p.vel[1] *= BOUND_DAMPING
            p.pos[1] = VIEW_HEIGHT - EPS



def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glOrtho(0, VIEW_WIDTH, 0, VIEW_HEIGHT, 0, 1)
    glColor4f(0.2, 0.6, 1.0, 1)
    glBegin(GL_POINTS)
    for p in particles:
        glVertex2f(p.pos[0], p.pos[1])
    glEnd()

    glutSwapBuffers()

def update():
    compute_density_pressure()
    compute_forces()
    integrate()

    glutPostRedisplay()

if __name__ == '__main__':
    pygame.init()
    display = (VIEW_WIDTH, VIEW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    init_gl()
    init_sph()
    render()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    

    