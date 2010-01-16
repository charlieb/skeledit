import pygame
from pygame.locals import *
from math import pi, atan

from matrix import Identity, Rotation, Translation, Scale, Vector
from bones import Bone, Root, Joint

def dist(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
def mag(v):
    return math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
def norm(p):
    dist = mag(p)
    return [p[0] / dist, p[1] / dist]
def dir(p1, p2):
    return norm([p2[0] - p1[0], p2[1] - p1[1]])

class UIBone:
    def __init__(self, bone):
        self.bone = bone

    def draw(self):
        pygame.draw.line(screen, (150,150,150), 
                         [int(bone.start.position.matrix[0]), 
                          int(bone.start.position.matrix[1])],
                         [int(bone.end.position.matrix[0]), 
                          int(bone.end.position.matrix[1])],
                         3)
    def center(self):
        return Vector((self.bone.end.position.matrix[0] +
                       self.bone.start.position.matrix[0]) / 2, 
                      (self.bone.end.position.matrix[1] + 
                       self.bone.start.position.matrix[1]) / 2)
    
    def click_in(self, pt):
        return (dist(self.center(), pt) <= 5)

class UIJoint:
    def __init__(self, joint):
        self.joint = joint

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255),
                           [int(joint.position.matrix[0]), 
                            int(joint.position.matrix[1])],
                           5, 0)
    def click_in(self, pt):
        return (dist(joint.position.matrix, pt) <= 5)

class UISkeleton:
    def __init__(self):
        
def main():
    pygame.init()
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
