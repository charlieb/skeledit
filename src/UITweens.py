import pygame

import tweens
import UIItems
import barebones
import matrix

class UIAnimation(UIItems.UIItemManager):
    height = 30
    ignore_x_pixels = 20
    def __init__(self):
        UIItems.UIItemManager.__init__(self)

    def new_keyframe(self, skeleton):
        key = UIKeyframe(self,
                         tweens.Keyframe(barebones.Root(skeleton.root.joint),
                                         self.total_time()))
        if self.items != []: key.keyframe.time += 3.0
        self.items.append(key)

    def set_keyframe(self, skeleton):
        if self.selected:
            self.seleted.keyframe.root = barebones.Root(skeleton.root.joint)
            
    def delete_keyframe(self):
        if self.selected:
            print self.selected
            print self.items
            self.items.remove(self.selected)
            print self.items
            self.selected = None

    def total_time(self):
        if self.items != []:
            return self.items[-1].keyframe.time
        else:
            return 0.0

class UIKeyframe(UIItems.UIItem):
    def __init__(self, manager, keyframe):
        UIItems.UIItem.__init__(self, manager)
        self.keyframe = keyframe
        self.font = pygame.font.Font(None, 14)
        self.position = matrix.Vector(0,0)

    def draw(self, screen):
        x = self.manager.ignore_x_pixels / 2
        if self.manager.total_time() > 0.0:
            x += (screen.get_width() - self.manager.ignore_x_pixels) * \
                 self.keyframe.time / self.manager.total_time()
            
        y = screen.get_height()
        # Recalculate position while we have the screen size
        self.position = matrix.Vector(x, y)
        pygame.draw.line(screen,
                         (0,255,0) if self.selected else (255,255,255),
                         (x, y), (x, y - self.manager.height),
                         3 if self.hilighted else 1)
        if self.hilighted:
            secs = self.font.render(str(self.keyframe.time),
                                    True,
                                    (150, 150, 255))
            screen.blit(secs, (x - secs.get_width() / 2,
                               y - self.manager.height - secs.get_height()))

    def mouse_over(self, p):
        return p[0] > self.position[0] - 3 and \
               p[0] < self.position[0] + 3 and \
               p[1] > self.position[1] - self.manager.height and \
               p[1] < self.position[1] 

    def drag(self, p):
        self.keyframe.time += 0.001 * (p[0] - self.position[0])
    
