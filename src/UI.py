import pygame
from pygame.locals import *

from Tkinter import Tk
from tkFileDialog import askopenfilename, asksaveasfile, askopenfile

import matrix
import UIItems
import UISkeleton
import UITweens
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
        self.keyframe_menu = self.make_keyframe_menu()
        self.menu = False

        self.animation = UITweens.UIAnimation()

    def make_main_menu(self):
                
        def New():
            self.skeleton.reset()
        def Recenter():
            self.skeleton.position = matrix.Vector(self.size[0] / 2,
                                                   self.size[1] / 2)
        def New_Keyframe():
            self.animation.new_keyframe(self.skeleton)
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
            ("New Keyframe", New_Keyframe),
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


    def make_keyframe_menu(self):
        def Set_Keyframe():
            self.animation.set_keyframe(self.skeleton)
        def Delete_Keyframe():
            self.animation.delete_keyframe()
        def Play_from_Here():
            self.animation.play_from()

        names_and_callbacks = [
            ("Set Keyframe", Set_Keyframe),
            ("Delete Keyframe", Delete_Keyframe),
            ("Play from Here", Play_from_Here)]
        
        return UIItems.UIMenu(names_and_callbacks,
                              pop_upwards = True)
        
        
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
                self.animation.drag(matrix.Vector(p[0], p[1]))
            elif self.menu and event.buttons[2]:
                self.menu.hilight(matrix.Vector(p[0], p[1]))
            elif self.animation.hilight(matrix.Vector(p[0], p[1])):
                pass
            else:
                self.skeleton.hilight(matrix.Vector(p[0], p[1]))
                
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            # Any mouse button will select/deselect the skeleton
            self.animation.select(matrix.Vector(p[0], p[1]))
            self.skeleton.select(matrix.Vector(p[0], p[1]))
            if event.button == 3: # RMB
                if self.animation.selected:
                    self.menu = self.keyframe_menu
                elif self.skeleton.selected:
                    if isinstance(self.skeleton.selected, UISkeleton.UIBone):
                        self.menu = self.bone_menu
                    elif isinstance(self.skeleton.selected, UISkeleton.UIJoint):
                        self.menu = self.joint_menu
                    elif isinstance(self.skeleton.selected, UISkeleton.UIImage):
                        self.menu = self.image_menu

                else:
                    self.menu = self.main_menu
                self.menu.position = matrix.Vector(p[0], p[1])
            elif event.button == 1:
                if self.animation.select(matrix.Vector(p[0], p[1])):
                    key = self.animation.selected.keyframe
                    self.skeleton.set_bones(key.root)
                
        elif event.type == MOUSEBUTTONUP:
            p = pygame.mouse.get_pos()
            if event.button == 3: # RMB
                if self.menu:
                    self.menu.select(matrix.Vector(p[0], p[1]))
                    self.menu = False

        return self.run
    
    def update(self):
        new_root = self.animation.set_skeleton()
        if new_root: self.skeleton.set_bones(new_root)
        self.skeleton.root.joint.calc_skeleton()

    def draw(self, screen):
        self.skeleton.draw(screen)
        self.animation.draw(screen)
        if self.menu: self.menu.draw(screen)
        

