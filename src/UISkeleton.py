import pygame
from copy import copy
from math import pi

import matrix
import bones
import UIItems

class UIGeometryItem(UIItems.UIItem):
    def __init__(self, manager):
        UIItems.UIItem.__init__(self, manager)

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

class UISkeleton(UIItems.UIItemManager):
    def __init__(self):
        UIItems.UIItemManager.__init__(self)
        self.build_UI_skeleton(bones.Root())
        
    def get_root(self):
        # The first joint is always the root
        return self.items[0]

    def reset(self):
        bones = copy(self.get_root().joint.bones_out)
        for bone in bones:
            bone.delete()        
        self.build_UI_skeleton(bones.Root())
        
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
            if isinstance(self.selected, UIJoint):
                joint = self.selected.joint
            elif isinstance(self.selected, UIBone):
                joint = self.selected.bone.end
            bone = bones.Bone(joint)
            bone.length = 50
            self.items += [UIBone(self, bone), UIJoint(self, bone.end)]
            self.build_UI_skeleton(self.get_root().joint)
                    
    def delete_bones(self):
        if self.selected:
            if isinstance(self.selected, UIBone):
                self.selected.bone.delete()
            elif isinstance(self.selected, UIJoint):
                bones = copy(self.selected.joint.bones_out)
                for bone in bones:
                    print bone
                    bone.delete()

            self.selected = None
            self.build_UI_skeleton(self.get_root().joint)
            
    def drag(self, p):
        if self.selected:
            self.selected.drag(p)

  
