import pygame

import tweens
import UIItems
import barebones
import matrix

class UIAnimation(UIItems.UIItemManager):
    height = 30
    ignore_x_pixels = 200
    def __init__(self):
        UIItems.UIItemManager.__init__(self)
        self.animation = tweens.Animation()

    def new_keyframe(self, skeleton):
        t = 0.0 if self.items == [] else self.animation.total_time() + 3.0
        key = tweens.Keyframe(barebones.Root(skeleton.root.joint), t)
            
        self.animation.keyframes.append(key)
        self.build_UI_animation()

    def set_keyframe(self, skeleton):
        if self.selected:
            self.selected.keyframe.root = barebones.Root(skeleton.root.joint)
            
    def delete_keyframe(self):
        if self.selected:
            self.animation.keyframes.remove(self.selected.keyframe)
            self.build_UI_animation()
            self.selected = None

    def build_UI_animation(self):
        self.items = []
        for key in self.animation.keyframes:
            self.items.append(UIKeyframe(self, key))

    def play_from(self):
        self.animation.play_from(self.selected)

    def set_skeleton(self):
        if self.animation.playing:
            return self.animation.get_state()
        else:
            return False
        
    def draw(self, screen):
        UIItems.UIItemManager.draw(self, screen)        
        

class UIKeyframe(UIItems.UIItem):
    def __init__(self, manager, keyframe):
        UIItems.UIItem.__init__(self, manager)
        self.keyframe = keyframe
        self.font = pygame.font.Font(None, 14)
        self.position = matrix.Vector(0,0)

    def draw(self, screen):
        x = self.manager.ignore_x_pixels / 2
        if self.manager.animation.total_time() > 0.0:
            x += (screen.get_width() - self.manager.ignore_x_pixels) * \
                 self.keyframe.time / self.manager.animation.total_time()
            
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
        # You cannot drag the first keyframe. It should always be at zero
        keyn = self.manager.items.index(self)
        if keyn == 0: return

        new_time = self.keyframe.time + 0.001 * (p[0] - self.position[0])

        # You also cannot drag one keyframe past another
        min_time = self.manager.items[keyn - 1].keyframe.time + \
                   tweens.Animation.min_keyframe_delta
        if new_time < min_time:
            self.keyframe.time = min_time
            return

        # the last keyframe is a special case for not being able to
        # drag one keyframe past another
        nkeys = len(self.manager.items)
        if keyn != nkeys - 1:
            max_time = self.manager.items[keyn + 1].keyframe.time - \
                       tweens.Animation.min_keyframe_delta
            if new_time > max_time:
                self.keyframe.time = max_time
                return
                
    
        # If we got here we can change the time
        self.keyframe.time = new_time
