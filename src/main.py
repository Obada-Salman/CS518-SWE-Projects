import pygame
from settings import *
import sys
from state_manager import StateManager
from Menu import MainMenuState
from StoryState import StoryState



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Onions May Cry")
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.RESIZABLE)
    clock = pygame.time.Clock()
    state_manager = StateManager()
    
    state_manager.add_state('menu',MainMenuState('menu', state_manager))
    state_manager.add_state('story',StoryState(state_manager))
    # state_manager.add_state('custom',CustomLevelState(state_manager))
    # state_manager.add_state('settings',SettingsState(state_manager))
    # state_manager.add_state('level_bld',LevelBuilderState(state_manager))
    
    state_manager.transition('menu')
    
    while not state_manager.window_should_close:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state_manager.quit()
        state_manager.update(events)
        state_manager.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()