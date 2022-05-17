import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy

VIEW_WIDTH = 800
VIEW_HEIGHT = 600

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


def Render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glOrtho(0, VIEW_WIDTH, 0, VIEW_HEIGHT, 0, 1)
    glColor4f(0.2, 0.6, 1.0, 1)
    glBegin(GL_POINTS)
    for p in particles:
        glVertex2f(p.x(0), p.x(1))
    glEnd()

    glutSwapBuffers()

def update():
    # compute_density_pressure()
    # compute_forces()
    # integrate()

    # glutPostRedisplay()
    pass

# def main():
#     pygame.init()
#     display = (VIEW_WIDTH, VIEW_HEIGHT)
#     pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    