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
        self.items = []
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
                return True
        return False

    def select(self, p):
        self.selected = None
        for item in self.items:
            item.selected = False
        for item in self.items:
            if item.mouse_over(p):
                self.selected = item
                item.selected = True
                return True
        return False

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
    def __init__(self, manager, base_image, hilight_image, position):
        UIItem.__init__(self, manager)
        self.base_image = base_image
        self.hilight_image = hilight_image
        self.position = position

    def draw(self, screen):
        pos = self.position + self.manager.position
        if self.hilighted:
            screen.blit(self.hilight_image, pos.to_coord_tuple())
        else:
            screen.blit(self.base_image, pos.to_coord_tuple())

    def mouse_over(self, p):
        pos = self.position + self.manager.position
        pos_plus_size = pos + self.manager.item_size
        return p[0] > pos[0] and \
               p[0] < pos_plus_size[0] and \
               p[1] > pos[1] and \
               p[1] < pos_plus_size[1]

class UIMenu(UIItemManager):
    def __init__(self):
        UIItemManager.__init__(self)
        self.position = matrix.Vector(0,0)
        self.font = pygame.font.Font(None, 14)
        self.item_size = matrix.Vector(0, 0)

    def add_item(self, text, bg_filename = None, bg_hilight_filename = None):
        # load the hilighted and normal backgrounds
        if bg_filename:
            bg = pygame.image.load(bg_filename)
        else:
            bg = pygame.Surface(self.item_size.to_coord_tuple())
            
        if bg_hilight_filename:
            bg_hl = pygame.image.load(bg_hilight_filename)
        else:
            bg_hl = pygame.Surface(self.item_size.to_coord_tuple())

        # Render the text to a foreground surface
        fg = self.font.render(text, True, (150, 150, 150))
        fg_hl = self.font.render(text, True, (0, 0, 255))
        # Blit the text onto the background
        bg.blit(fg, (0,0))
        bg_hl.blit(fg_hl, (0,0))
        # Calculate the position of the new item 
        self.items.append(
            UIButton(self, bg, bg_hl, 
                     matrix.Vector(0,
                                   len(self.items) * self.item_size[1])))
    

class UIMainMenu(UIMenu):
    def __init__(self):
        UIMenu.__init__(self)
        names = ["New", "Recenter", "Save", "Load", "Exit"]
        for name in names:
            size = self.font.size(name)
            self.item_size = \
                           matrix.Vector(size[0] if size[0] > self.item_size[0]\
                                         else self.item_size[0], \
                                         size[1] if size[1] > self.item_size[1]\
                                         else self.item_size[1])
        for name in names:
            self.add_item(name)

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
    pygame.font.init()
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    UI = UISkeleton(test_skele())
    UI.position = matrix.Vector(320, 240)

    menu = False
    main_menu = UIMainMenu()

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
            # event.pos lags horribly so get the mouse pos directly
            p = pygame.mouse.get_pos()
            # Left mouse button            
            if event.buttons[0]:
                UI.drag(matrix.Vector(p[0], p[1]))
            elif menu and event.buttons[2]:
                menu.hilight(matrix.Vector(p[0], p[1]))
            else:
                UI.hilight(matrix.Vector(p[0], p[1]))
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            if event.button == 1: # LMB
                UI.select(matrix.Vector(p[0], p[1]))
            elif event.button == 3: # RMB
                main_menu.position = matrix.Vector(p[0], p[1])
                menu = main_menu
        elif event.type == MOUSEBUTTONUP:
            menu = False
               
        UI.get_root().joint.calc_skeleton()
        
        UI.draw(screen)
        if menu: menu.draw(screen)
        
        pygame.display.flip()
        screen.fill((0,0,0))
