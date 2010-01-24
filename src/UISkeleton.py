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

class UIImage(UIGeometryItem):
    def __init__(self, manager, image):
        UIItems.UIItem.__init__(self, manager)
        self.image = image
        self.surface = pygame.image.load(self.image.filename)

    def image_radius(self):
        size = self.surface.get_size()
        return max(size[0], size[1]) / 2

    def handle_pos(self):
        rot = matrix.Rotation(self.image.bone.end.get_rotation())
        handle = matrix.Vector(self.image_radius(), 0)
        return (handle * rot) + self.image.bone.end.get_position()

    def center(self):
        return (self.image.bone.end.get_position() + self.handle_pos()) * 0.5
  
    def draw(self, screen):
        rot = self.image.bone.end.get_rotation() * (180.0 / pi)
        rotated_image = pygame.transform.rotate(self.surface, rot)
        size = rotated_image.get_size()
        pos = self.image.bone.end.get_position()
        trans = self.to_screen_pos(matrix.Vector(-size[0] / 2, size[1] / 2) + pos)
                
        screen.blit(rotated_image, [int(trans[0]), int(trans[1])])

        handle_colour = (150,150,150)
        selector_colour = (0, 0, 255)
        selector_size = 3
        selector_width = 0
        if self.hilighted:
            handle_colour = (200,200,100)
            selector_size = 5
            selector_width = 1
        if self.selected:
            handle_colour = (100,200,100)
            selector_colour = (255, 255, 0)

        start = self.to_screen_pos(pos)
        center = self.to_screen_pos(self.center())
        end = self.to_screen_pos(self.handle_pos())
        
        pygame.draw.line(screen, handle_colour,
                         [int(start[0]), int(start[1])],
                         [int(end[0]), int(end[1])])
        pygame.draw.circle(screen, selector_colour,
                           [int(center[0]), int(center[1])],
                           selector_size, selector_width)
        pygame.draw.circle(screen, selector_colour,
                           [int(end[0]), int(end[1])],
                           selector_size, selector_width)
        

    def mouse_over(self, p):
        return False
        size = self.surface.get_size()
        radius = max(size[0], size[1]) / 2

        pos = self.to_screen_pos(self.image.bone.end.get_position())
        print pos.distance(p)
        
        return pos.distance(p) <= radius            
        
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

        start = self.to_screen_pos(self.bone.start.get_position())
        end = self.to_screen_pos(self.bone.end.get_position())

        pygame.draw.line(screen, bone_colour, 
                         [int(start[0]), int(start[1])],
                         [int(end[0]), int(end[1])])
        center = self.to_screen_pos(self.center())
        pygame.draw.circle(screen, selector_colour,
                           [int(center[0]), int(center[1])],
                           selector_size, selector_width)

        
    def center(self):
        return (self.bone.start.get_position() + self.bone.end.get_position()) * 0.5
    
    def mouse_over(self, p):
        return self.center().distance(self.from_screen_pos(p)) <= 5

    def drag(self, p):
        self.bone.set_absolute_rotation(\
            self.bone.start.get_position().heading(self.from_screen_pos(p)))

    def set_image(self, image_filename):
        self.bone.attach_image(image_filename)
        self.manager.build_UI_skeleton()

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

        pos = self.to_screen_pos(self.joint.get_position())
        pygame.draw.circle(screen, colour,
                           [int(pos[0]), int(pos[1])],
                           size, width)
        
    def mouse_over(self, p):
        return self.joint.get_position().distance(self.from_screen_pos(p)) <= 5

    def drag(self, p):
        bone = self.joint.bone_in
        bone.length = bone.start.get_position().distance(self.from_screen_pos(p))
        bone.set_absolute_rotation( \
            bone.start.get_position().heading(self.from_screen_pos(p)))

class UIRoot(UIJoint):
    def __init__(self, manager, root):
        UIJoint.__init__(self, manager, root)

    def drag(self, p):
        self.manager.position = p

class UISkeleton(UIItems.UIItemManager):
    def __init__(self):
        UIItems.UIItemManager.__init__(self)
        self.root = UIRoot(self, bones.Root())
        self.items = [self.root]

        self.build_UI_skeleton()
        
    def reset(self):
        root_bones = copy(self.root.joint.bones_out)
        for bone in root_bones:
            bone.delete()        
        self.build_UI_skeleton()
        
    def __build_UI_skeleton_r(self, joint, root = False):
        if root:
            self.root = UIRoot(self, joint)
            self.items.append(self.root)
        else:
            self.items.append(UIJoint(self, joint))
            
        for b in joint.bones_out:
            self.items.append(UIBone(self, b))
            if b.image:
                # Use insert to ensure that images are always
                # drawn first = bones on top
                self.items.insert(0, UIImage(self, b.image))
            self.__build_UI_skeleton_r(b.end)

    def build_UI_skeleton(self):
        self.items = []
        self.__build_UI_skeleton_r(self.root.joint, True)

    def add_image(self, filename):
        if self.selected:
            if isinstance(self.selected, UIBone):
                bone = self.selected.bone
                if bone.image: bone.image.bone = None
                bone.image = bones.Image(filename, bone)
                self.build_UI_skeleton()

    def remove_image(self):
        if self.selected:
            if isinstance(self.selected, UIBone):
                if self.selected.bone.image:
                    self.selected.bone.image.bone = None
                    self.selected.bone.image = None
                    self.build_UI_skeleton()

    def add_bone(self):
        if self.selected:
            if isinstance(self.selected, UIJoint):
                joint = self.selected.joint
            elif isinstance(self.selected, UIBone):
                joint = self.selected.bone.end
            bone = bones.Bone(joint)
            bone.length = 50
            self.items += [UIBone(self, bone), UIJoint(self, bone.end)]
            self.build_UI_skeleton()
                    
    def delete_bones(self):
        if self.selected:
            if isinstance(self.selected, UIBone):
                self.selected.bone.delete()
            elif isinstance(self.selected, UIJoint):
                bones = copy(self.selected.joint.bones_out)
                for bone in bones:
                    bone.delete()

            self.selected = None
            self.build_UI_skeleton()
            
    def drag(self, p):
        if self.selected:
            self.selected.drag(p)

  
