import pygame

import matrix

class UIItem:
    def __init__(self, manager):
        self.selected = False
        self.hilighted = False
        self.manager = manager

    def draw(self, _):
        return False
    
    def mouse_over(self, _):
        return False

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


class UIButton(UIItem):
    def __init__(self, manager, base_image, hilight_image, position):
        UIItem.__init__(self, manager)
        self.base_image = base_image
        self.hilight_image = hilight_image
        self.position = position
        self.callback = None

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
    def __init__(self, names_and_callbacks = ()):
        UIItemManager.__init__(self)
        self.position = matrix.Vector(0,0)
        self.font = pygame.font.Font(None, 14)
        self.item_size = matrix.Vector(0, 0)

        for name in names_and_callbacks:
            size = self.font.size(name[0])
            self.item_size[0] = size[0] if size[0] > self.item_size[0] \
                                    else self.item_size[0]
            self.item_size[1] = size[1] if size[1] > self.item_size[1] \
                                    else self.item_size[1]
            
        for name in names_and_callbacks:
            self.add_item(name[0], name[1])


    def add_item(self, text, callback, \
                 bg_filename = None, \
                 bg_hilight_filename = None):
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
        item = UIButton(self, bg, bg_hl, 
                        matrix.Vector(0, len(self.items) * self.item_size[1]))
        item.callback = callback
        self.items.append(item)
            
    
    def select(self, p):
        UIItemManager.select(self, p)
        for item in self.items:
            if item.selected:
                if item.callback:
                    item.callback()
        
