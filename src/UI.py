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

        self.main_menu = UIItems.UIMenu(names_and_callbacks)
        self.menu = False

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                return False
            elif event.key == K_n:
                self.skeleton.add_bone()
            elif event.key == K_d:
                self.skeleton.delete_bone()
                
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
                    pass
                else:
                    self.main_menu.position = matrix.Vector(p[0], p[1])
                    self.menu = self.main_menu
                
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
        

