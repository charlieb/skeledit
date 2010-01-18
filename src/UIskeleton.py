import pygame
from pygame.locals import *
from math import pi

import matrix
import bones

def correct_pos(p, offset):
    return matrix.Vector(p[0] - offset[0], -p[1] + offset[1])

def reload_UI_skeleton_imports():
    reload(matrix)
    reload(bones)

reload_UI_skeleton_imports()
   
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
                         [int(offset[0] + self.bone.start.position[0]), 
                          int(offset[1] - self.bone.start.position[1])],
                         [int(offset[0] + self.bone.end.position[0]), 
                          int(offset[1] - self.bone.end.position[1])])
        center = self.center()
        pygame.draw.circle(screen, selector_colour,
                           [int(offset[0] + center[0]), 
                            int(offset[1] - center[1])],
                           selector_size, selector_width)
        
    def center(self):
        return (self.bone.start.position + self.bone.end.position) * 0.5
    
    def click_in(self, p):
        return self.center().distance(p) <= 5

    def drag(self, p):
        self.bone.set_absolute_rotation(self.bone.start.position.heading(p))

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
                           [int(offset[0] + self.joint.position[0]), 
                            int(offset[1] - self.joint.position[1])],
                           size, width)
    def click_in(self, p):
        return self.joint.position.distance(p) <= 5

    def drag(self, p):
        bone = self.joint.bone_in
        bone.length = bone.start.position.distance(p)
        bone.set_absolute_rotation(bone.start.position.heading(p))

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

    def set_position(self, p):
        self.get_root().offset = p
        
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

    def add_bone(self):
        if self.selected:
            if isinstance(self.selected, UIBone):
                print "Please select a Joint"
                return
            bone = bones.Bone(self.selected.joint)
            bone.length = 10
            self.bones.append(UIBone(bone))
            self.joints.append(UIJoint(bone.end))

    def draw(self, screen):
        for item in self.joints + self.bones:
            item.draw(screen, self.get_root().offset)

    def hilight(self, p):
        for item in self.bones + self.joints:
            item.hilighted = False
        for item in self.bones + self.joints:
            if item.click_in(correct_pos(p, self.get_root().offset)):
                item.hilighted = True
                return

    def select(self, p):
        self.selected = None
        for item in self.bones + self.joints:
            item.selected = False
        for item in self.bones + self.joints:
            if item.click_in(correct_pos(p, self.get_root().offset)):
                self.selected = item
                item.selected = True
                return

    def drag(self, p):
        if self.selected:
            self.selected.drag(correct_pos(p, self.get_root().offset))
        
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
    return root
  
def main():
    pygame.init()
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    UI = UISkeleton(test_skele())
    UI.set_position(matrix.Vector(320, 240))

    print 'Info:'
    print '\nAdd a bone: select a joint and press n'

    mouse_down = False
    while True:
        pygame.event.pump()
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                return True
            elif event.key == K_n:
                UI.add_bone()
                
        elif event.type == MOUSEMOTION:
            p = pygame.mouse.get_pos()
            if mouse_down:
                UI.drag(matrix.Vector(p[0], p[1]))
            else:
                UI.hilight(matrix.Vector(p[0], p[1]))
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            UI.select(matrix.Vector(p[0], p[1]))
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
