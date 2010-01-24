import pygame
from pygame.locals import *

from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfile, askopenfile

import matrix
import UIItems
import UISkeleton
import saveload

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
        self.image_menu = self.make_image_menu()
        self.menu = False

    def make_main_menu(self):
                
        def New():
            self.skeleton.reset()
        def Recenter():
            self.skeleton.position = matrix.Vector(self.size[0] / 2,
                                                   self.size[1] / 2)
        def Save():
            root = Tk()
            root.withdraw()
            f = asksaveasfile(filetypes=[("Skeledit Files", "*.ske")],
                              title='Save Bones')
            if f:
                saveload.save(self.skeleton.root.joint, f)
                file.close(f)
        def Load():
            root = Tk()
            root.withdraw()
            f = askopenfile(filetypes=[("Skeledit Files", "*.ske")],
                            title='Load Bones')
            if f:
                self.skeleton.root.joint = saveload.load(f)
                file.close(f)
                self.skeleton.build_UI_skeleton()
        def Exit():
            self.run = False
            
        names_and_callbacks = [
            ("New", New),
            ("Recenter", Recenter),
            ("Save", Save),
            ("Load", Load),
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
            # Hide the stupid Tk root window!
            root = Tk()
            root.withdraw()
            filename = askopenfilename(filetypes=[("PNG", "*.png")],
                                       title='Choose Image to Attach')
            print filename
            if filename:
                self.skeleton.add_image(filename)

        def Remove_Image():
            self.skeleton.remove_image()

        names_and_callbacks = [
            ("New Bone", New_Bone),
            ("Delete Bone", Delete_Bones),
            ("Attach Image", Attach_Image),
            ("Remove Image", Remove_Image)]

        return UIItems.UIMenu(names_and_callbacks)

    def make_image_menu(self):
        
        def Mirror_Vertically():
            self.skeleton.selected.image.mirror_y = \
                 not self.skeleton.selected.image.mirror_y
            self.skeleton.build_UI_skeleton()
            
        def Mirror_Horizontally():
            self.skeleton.selected.image.mirror_x = \
                 not self.skeleton.selected.image.mirror_x 
            self.skeleton.build_UI_skeleton()

        def Change_Image():
            # Hide the stupid Tk root window!
            root = Tk()
            root.withdraw()
            filename = askopenfilename(filetypes=[("PNG", "*.png")],
                                       title='Choose Image to Attach')
            print filename
            if filename:
                self.skeleton.add_image(filename)

        def Remove_Image():
            self.skeleton.remove_image()

        names_and_callbacks = [
            ("Mirror Vertically", Mirror_Vertically),
            ("Mirror Horizontally", Mirror_Horizontally),
            ("Change Image", Change_Image),
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
                    elif isinstance(self.skeleton.selected, UISkeleton.UIImage):
                        self.menu = self.image_menu

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
        self.skeleton.root.joint.calc_skeleton()

    def draw(self, screen):
        self.skeleton.draw(screen)
        if self.menu: self.menu.draw(screen)
        

