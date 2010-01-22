import pygame
from pygame.locals import *

import matrix
import UIItems
import UISkeleton

class UI:
    def __init__(self, size = (640, 480)):
        self.skeleton = UISkeleton.UISkeleton()
        self.size = matrix.Vector(size[0], size[1])

        self.run = True
        self.skeleton.position = matrix.Vector(self.size[0] / 2,
                                               self.size[1] / 2)

        self.main_menu = self.make_main_menu()
        self.joint_menu = self.make_joint_menu()
        self.bone_menu = self.make_bone_menu()
        self.menu = False

    def make_main_menu(self):
                
        def New():
            self.skeleton.reset()
        def Recenter():
            self.skeleton.position = matrix.Vector(self.size[0] / 2,
                                                   self.size[1] / 2)
        def Exit():
            self.run = False
            
        names_and_callbacks = [
            ("New", New),
            ("Recenter", Recenter),
            ("Save", None),
            ("Load", None),
            ("Exit", Exit)]

        return UIItems.UIMenu(names_and_callbacks)

    def make_joint_menu(self):

        def New_Bone():
            self.skeleton.add_bone()

        def Delete_Bones():
            self.skeleton.delete_bones()

        names_and_callbacks = [
            ("New Bone", New_Bone),
            ("Delete Bones", Delete_Bones)]

        return UIItems.UIMenu(names_and_callbacks)

    def make_bone_menu(self):

        def New_Bone():
            self.skeleton.add_bone()

        def Delete_Bones():
            self.skeleton.delete_bones()

        def Attach_Image():
            pass

        def Remove_Image():
            pass

        names_and_callbacks = [
            ("New Bone", New_Bone),
            ("Delete Bone", Delete_Bones),
            ("Attach Image", Attach_Image),
            ("Remove Image", Remove_Image)]

        return UIItems.UIMenu(names_and_callbacks)

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                return False
            elif event.key == K_n:
                self.skeleton.add_bone()
            elif event.key == K_d:
                self.skeleton.delete_bones()
                
        elif event.type == MOUSEMOTION:
            # event.pos lags horribly so get the mouse pos directly
            p = pygame.mouse.get_pos()
            # Left mouse button            
            if event.buttons[0]:
                self.skeleton.drag(matrix.Vector(p[0], p[1]))
            elif self.menu and event.buttons[2]:
                self.menu.hilight(matrix.Vector(p[0], p[1]))
            else:
                self.skeleton.hilight(matrix.Vector(p[0], p[1]))
                
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            # Any mouse button will select/deselect the skeleton
            self.skeleton.select(matrix.Vector(p[0], p[1]))
            if event.button == 3: # RMB
                if self.skeleton.selected:
                    if isinstance(self.skeleton.selected, UISkeleton.UIBone):
                        self.menu = self.bone_menu
                    elif isinstance(self.skeleton.selected, UISkeleton.UIJoint):
                        self.menu = self.joint_menu
                else:
                    self.menu = self.main_menu
                self.menu.position = matrix.Vector(p[0], p[1])
                
        elif event.type == MOUSEBUTTONUP:
            p = pygame.mouse.get_pos()
            if event.button == 3: # RMB
                if self.menu:
                    self.menu.select(matrix.Vector(p[0], p[1]))
                    self.menu = False

        return self.run
    
    def update(self):
        self.skeleton.get_root().joint.calc_skeleton()

    def draw(self, screen):
        self.skeleton.draw(screen)
        if self.menu: self.menu.draw(screen)
        

