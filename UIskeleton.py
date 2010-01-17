import pygame
from pygame.locals import *
from math import pi

import matrix
import bones

def reload_UI_skeleton_imports():
    reload(matrix)
    reload(bones)

reload_UI_skeleton_imports()

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

    def draw(self, screen, offset):
        pygame.draw.line(screen, (150,150,150), 
                         [int(offset.matrix[0] + \
                                  self.bone.start.position.matrix[0]), 
                          int(offset.matrix[1] + \
                                  self.bone.start.position.matrix[1])],
                         [int(offset.matrix[0] + 
                              self.bone.end.position.matrix[0]), 
                          int(offset.matrix[1] + 
                              self.bone.end.position.matrix[1])])
        center = self.center()
        pygame.draw.circle(screen, (150, 150, 150),
                           [int(offset.matrix[0] + center.matrix[0]), 
                            int(offset.matrix[1] + center.matrix[1])],
                           2, 1)
        
    def center(self):
        return matrix.Vector((self.bone.end.position.matrix[0] +
                              self.bone.start.position.matrix[0]) / 2, 
                             (self.bone.end.position.matrix[1] + 
                              self.bone.start.position.matrix[1]) / 2)
    
    def click_in(self, pt):
        return (dist(self.center(), pt) <= 5)

class UIJoint:
    def __init__(self, joint):
        self.joint = joint

    def draw(self, screen, offset):
        pygame.draw.circle(screen, (0, 0, 255),
                           [int(offset.matrix[0] + self.joint.position.matrix[0]), 
                            int(offset.matrix[1] + self.joint.position.matrix[1])],
                           5, 1)
    def click_in(self, pt):
        return (dist(joint.position.matrix, pt) <= 5)

class UISkeleton:
    def __init__(self, root):
        self.joints = []
        self.bones = []
        self.build_UI_skeleton(root)
        self.offset = matrix.Vector(0,0)

    def get_root(self):
        # The first joint is always the root
        return self.joints[0]

    def set_position(self, new_pos):
        self.offset = matrix.Vector(new_pos.matrix[0], new_pos.matrix[1])
        

    def build_UI_skeleton(self, root):
        self.joints.append(UIJoint(root))
        for b in root.bones:
            self.bones.append(UIBone(b))
            self.build_UI_skeleton(b.end)

    def draw(self, screen):
        for item in self.joints + self.bones:
            item.draw(screen, self.offset)
    
def test_skele():
    root = bones.Joint()
    b1 = bones.Bone(root)
    b1.length = 50
    b1.rotation = pi / 2

    b2 = bones.Bone(b1.end)
    b2.length = 50
    b2.rotation = pi / 4

    b3 = bones.Bone(b1.end)
    b3.length = 50
    b3.rotation = -pi / 4

    root.calc_skeleton()

    bones.print_skeleton(root)
    print "-----"
    return root
  
def main():
    pygame.init()
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    UI = UISkeleton(test_skele())
    UI.set_position(matrix.Vector(320, 240))

    for joint in UI.joints:
        print joint.joint

    while True:
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                return True

        UI.bones[0].bone.rotation += pi / 50
        UI.get_root().joint.calc_skeleton()

        bones.print_skeleton(UI.get_root().joint)
        print "==============================="
        UI.draw(screen)
        pygame.display.flip()
        screen.fill((0,0,0))
