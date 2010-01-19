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
    def __init__(self, manager):
        self.selected = False
        self.hilighted = False
        self.manager = manager

class UIGeometryItem(UIItem):
    def __init__(self, manager):
        UIItem.__init__(self, manager)

    def to_screen_pos(self, p):
        return matrix.Vector(p[0] + self.manager.position[0], \
                             -p[1] + self.manager.position[1])

    def from_screen_pos(self, p):
        return matrix.Vector(p[0] - self.manager.position[0], \
                             -p[1] + self.manager.position[1])

class UIBone(UIGeometryItem):
    def __init__(self, manager, bone):
        UIGeometryItem.__init__(self, manager)
        self.bone = bone

    def draw(self, screen):
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

        start = self.to_screen_pos(self.bone.start.position)
        end = self.to_screen_pos(self.bone.end.position)

        pygame.draw.line(screen, bone_colour, 
                         [int(start[0]), int(start[1])],
                         [int(end[0]), int(end[1])])
        center = self.to_screen_pos(self.center())
        pygame.draw.circle(screen, selector_colour,
                           [int(center[0]), int(center[1])],
                           selector_size, selector_width)
        
    def center(self):
        return (self.bone.start.position + self.bone.end.position) * 0.5
    
    def mouse_over(self, p):
        return self.center().distance(self.from_screen_pos(p)) <= 5

    def drag(self, p):
        self.bone.set_absolute_rotation(\
            self.bone.start.position.heading(self.from_screen_pos(p)))

class UIJoint(UIGeometryItem):
    def __init__(self, manager, joint):
        UIGeometryItem.__init__(self, manager)
        self.joint = joint

    def draw(self, screen):
        colour = (175, 175, 175)
        size = 2
        width = 0
        if self.hilighted:
            size = 5
            width = 1
        if self.selected:
            colour = (0, 255, 0)
            size = 3

        pos = self.to_screen_pos(self.joint.position)
        pygame.draw.circle(screen, colour,
                           [int(pos[0]), int(pos[1])],
                           size, width)
        
    def mouse_over(self, p):
        return self.joint.position.distance(self.from_screen_pos(p)) <= 5

    def drag(self, p):
        bone = self.joint.bone_in
        bone.length = bone.start.position.distance(self.from_screen_pos(p))
        bone.set_absolute_rotation( \
            bone.start.position.heading(self.from_screen_pos(p)))

class UIRoot(UIJoint):
    def __init__(self, manager, root):
        UIJoint.__init__(self, manager, root)

    def drag(self, p):
        self.manager.position = p

class UIItemManager:
    def __init__(self):
        self.sub_items = []
        self.position = matrix.Vector(0, 0)

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

    def hilight(self, p):
        for item in self.items:
            item.hilighted = False
        for item in self.items:
            if item.mouse_over(p):
                item.hilighted = True
                return

    def select(self, p):
        self.selected = None
        for item in self.items:
            item.selected = False
        for item in self.items:
            if item.mouse_over(p):
                self.selected = item
                item.selected = True
                return

    def drag(self, p):
        if self.selected:
            self.selected.drag(p)

    
class UISkeleton(UIItemManager):
    def __init__(self, root):
        self.build_UI_skeleton(root)
        self.position = matrix.Vector(0, 0)
        
    def get_root(self):
        # The first joint is always the root
        return self.items[0]
        
    def __build_UI_skeleton_r(self, root):
        self.items.append(UIJoint(self, root))
        for b in root.bones_out:
            self.items.append(UIBone(self, b))
            self.__build_UI_skeleton_r(b.end)

    def build_UI_skeleton(self, root):
        self.items = []
        self.items.append(UIRoot(self, root))
        for b in root.bones_out:
            self.items.append(UIBone(self, b))
            self.__build_UI_skeleton_r(b.end)

    def add_bone(self):
        if self.selected:
            if not isinstance(self.selected, UIJoint):
                print "Please select a Joint"
                return
            bone = bones.Bone(self.selected.joint)
            bone.length = 10
            self.items += [UIBone(self, bone), UIJoint(self, bone.end)]
                    
    def delete_bone(self):
        if self.selected:
            if not isinstance(self.selected, UIBone):
                print "Please select a Bone"
                return
            self.selected.bone.delete()
            self.selected = None
            # Cache the offset so it doesn't get wiped out by the rebuild
            self.build_UI_skeleton(self.get_root().joint)
            
    def drag(self, p):
        if self.selected:
            self.selected.drag(p)


class UIButton(UIItem):
    def __init__(self, image, position):
        self.image = image
        self.position = position

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def mouse_over(self, p):
        return p[0] > position[0] and \
               p[0] < position[0] + self.image.get_width() and  \
               p[1] > position[1] and \
               p[1] < position[1] + self.image.get_height()

class UIMenu(UIItem):
    def __init__(self, position):
        self.image = image
        self.position = position
        self.buttons = []

    def hilight(self, p):
        for item in self.bones + self.joints:
            item.hilighted = False
        for item in self.bones + self.joints:
            if item.mouse_over(correct_pos(p, self.get_root().offset)):
                item.hilighted = True
                return          

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
    UI.position = matrix.Vector(320, 240)

    print 'Info:'
    print '\nAdd a bone: select a joint and press (n)ew'
    print '\nDelete a bone: select a bone and press (d)elete'

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
            elif event.key == K_d:
                UI.delete_bone()
                
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
               
        UI.get_root().joint.calc_skeleton()
        
        UI.draw(screen)
        pygame.display.flip()
        screen.fill((0,0,0))
