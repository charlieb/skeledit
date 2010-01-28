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

    def remove_dups(event_list):
        last_event_type = None
        remaining_events = []
        for e in event_list:
            if e.type != last_event_type:
                remaining_events.append(e)
                last_event_type = e.type
        #print "%s / %s"%(len(remaining_events), len(event_list))
        return remaining_events

    mouse_down = False
    while True:
        pygame.event.pump()
        events = remove_dups(pygame.event.get())        

        # when event returns False it's time to go
        for event in events:
            if not ui.event(event): return
        ui.update()
        ui.draw(screen)
        
        pygame.display.flip()
        screen.fill((0,0,0))
