import pygame
from pygame.locals import *
from math import pi, pow, sqrt, atan

import matrix
import bones

def reload_UI_skeleton_imports():
    reload(matrix)
    reload(bones)

reload_UI_skeleton_imports()

def dist(p1, p2):
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
def mag(v):
    return sqrt(pow(v[0], 2) + pow(v[1], 2))
def norm(p):
    dist = mag(p)
    return [p[0] / dist, p[1] / dist]
def direction(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]
def heading(p1, p2):
    d = direction(p1, p2)
    
    if d[0] < 0 and d[1] < 0:
        return pi + atan(d[0] / -d[1])
    elif d[0] < 0 and d[1] == 0:
        return pi / 2
    elif d[0] < 0 and d[1] > 0:
        return pi / 2 + atan(d[1] / d[0])
    
    elif d[0] == 0 and d[1] < 0:
        return pi
    # Don't change anything in this case    
    # elif d[0] == 0 and d[1] == 0:
    elif d[0] == 0 and d[1] > 0:
        return 0

    elif d[0] > 0 and d[1] > 0:
        return atan(d[0] / -d[1])
    elif d[0] > 0 and d[1] == 0:
        return 3 * pi / 2
    elif d[0] > 0 and d[1] < 0:
        return 3 * pi / 2 + atan(d[1] / d[0])
    
class UIItem:
    def __init__(self):
        self.selected = False
        self.hilighted = False

class UIBone(UIItem):
    def __init__(self, bone):
        UIItem.__init__(self)
        self.bone = bone

    def draw(self, screen, offset):
        bone_colour = (150,150,150)
        selector_colour = (0, 0, 255)
        selector_size = 3
        selector_width = 0
        if self.hilighted:
            bone_colour = (100,200,100)
            selector_size = 5
            selector_width = 1
        if self.selected:
            bone_colour = (100,200,100)
            selector_colour = (0, 255, 0)
            
        pygame.draw.line(screen, bone_colour, 
                         [int(offset.matrix[0] + \
                                  self.bone.start.position.matrix[0]), 
                          int(offset.matrix[1] - \
                                  self.bone.start.position.matrix[1])],
                         [int(offset.matrix[0] + 
                              self.bone.end.position.matrix[0]), 
                          int(offset.matrix[1] - 
                              self.bone.end.position.matrix[1])])
        center = self.center()
        pygame.draw.circle(screen, selector_colour,
                           [int(offset.matrix[0] + center.matrix[0]), 
                            int(offset.matrix[1] - center.matrix[1])],
                           selector_size, selector_width)
        
    def center(self):
        return matrix.Vector((self.bone.end.position.matrix[0] +
                              self.bone.start.position.matrix[0]) / 2, 
                             (self.bone.end.position.matrix[1] + 
                              self.bone.start.position.matrix[1]) / 2)
    
    def click_in(self, x, y):
        return (dist(self.center().matrix, [x, y]) <= 5)

    def drag(self, x, y, offset):
        self.bone.set_absolute_rotation( \
            heading(self.bone.start.position.matrix,
                    [x - offset.matrix[0], -y + offset.matrix[1]]))

class UIJoint(UIItem):
    def __init__(self, joint):
        UIItem.__init__(self)
        self.joint = joint

    def draw(self, screen, offset):
        colour = (175, 175, 175)
        size = 2
        width = 0
        if self.hilighted:
            size = 5
            width = 1
        if self.selected:
            colour = (0, 255, 0)
            size = 3
        pygame.draw.circle(screen, colour,
                           [int(offset.matrix[0] + self.joint.position.matrix[0]), 
                            int(offset.matrix[1] - self.joint.position.matrix[1])],
                           size, width)
    def click_in(self, x, y):
        return (dist(self.joint.position.matrix, [x, y]) <= 5)

    def drag(self, x, y, offset):
        bone = self.joint.bone_in
        corrected_pos = [x - offset.matrix[0], -y + offset.matrix[1]]
        bone.length = dist(bone.start.position.matrix, corrected_pos)
        bone.set_absolute_rotation( \
            heading(bone.start.position.matrix, corrected_pos))

class UIRoot(UIJoint):
    def __init__(self, root):
        UIJoint.__init__(self, root)
        self.offset = matrix.Vector(0,0)

    def drag(self, x, y, offset):
        self.offset = matrix.Vector(x, y)
    
class UISkeleton:
    def __init__(self, root):
        self.joints = []
        self.bones = []
        self.build_UI_skeleton(root)
        self.selected = None
        
    def get_root(self):
        # The first joint is always the root
        return self.joints[0]

    def set_position(self, new_pos):
        self.get_root().offset = matrix.Vector(new_pos.matrix[0], new_pos.matrix[1])
        
    def __build_UI_skeleton_r(self, root):
        self.joints.append(UIJoint(root))
        for b in root.bones_out:
            self.bones.append(UIBone(b))
            self.__build_UI_skeleton_r(b.end)

    def build_UI_skeleton(self, root):
        self.joints.append(UIRoot(root))
        for b in root.bones_out:
            self.bones.append(UIBone(b))
            self.__build_UI_skeleton_r(b.end)

    def draw(self, screen):
        for item in self.joints + self.bones:
            item.draw(screen, self.get_root().offset)

    def hilight(self, (x, y)):
        for item in self.bones + self.joints:
            item.hilighted = False
        for item in self.bones + self.joints:
            if item.click_in(x - self.get_root().offset.matrix[0],
                             -y + self.get_root().offset.matrix[1]):
                item.hilighted = True
                return

    def select(self, (x, y)):
        self.selected = None
        for item in self.bones + self.joints:
            item.selected = False
        for item in self.bones + self.joints:
            if item.click_in(x - self.get_root().offset.matrix[0],
                             -y + self.get_root().offset.matrix[1]):
                self.selected = item
                item.selected = True
                return

    def drag(self, (x, y)):
        if self.selected:
            self.selected.drag(x, y, self.get_root().offset)
        
def test_skele():
    root = bones.Root()
    b1 = bones.Bone(root)
    b1.length = 50
    b1.rotation = 0

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
    
    mouse_down = False
    while True:
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                return True
        elif event.type == MOUSEMOTION:
            if mouse_down:
                UI.drag(pygame.mouse.get_pos())
            else:
                UI.hilight(pygame.mouse.get_pos())
        elif event.type == MOUSEBUTTONDOWN:
            UI.select(pygame.mouse.get_pos())
            mouse_down = True
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False


            
        #UI.bones[0].bone.rotation += pi / 50
        #UI.bones[2].bone.rotation += pi / 100
                
        UI.get_root().joint.calc_skeleton()

        #bones.print_skeleton(UI.get_root().joint)
        #print "==============================="
        UI.draw(screen)
        pygame.display.flip()
        screen.fill((0,0,0))
