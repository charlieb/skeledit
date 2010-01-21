import pygame

import UI

def main():
    pygame.init()
    pygame.font.init()
    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)

    ui = UI.UI()

    print 'Info:'
    print '\nAdd a bone: select a joint and press (n)ew'
    print '\nDelete a bone: select a bone and press (d)elete'

    mouse_down = False
    while True:
        pygame.event.pump()
        event = pygame.event.poll()

        # when event returns False it's time to go
        if not ui.event(event): return
        ui.update()
        ui.draw(screen)
        
        pygame.display.flip()
        screen.fill((0,0,0))
