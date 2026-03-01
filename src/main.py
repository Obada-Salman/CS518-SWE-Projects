import pygame
from settings import *
import sys
from state_manager import StateManager
from Menu import MainMenuState
from StoryState import StoryState
from SettingsState import SettingsState
from LevelSelect import LevelSelectState
from LevelbuilderState import LevelBuilderState



def main():
    pygame.init()
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Onions May Cry")
    clock = pygame.time.Clock()
    state_manager = StateManager()
    
    state_manager.add_state('menu', MainMenuState('menu', state_manager))
    state_manager.add_state('story', StoryState(state_manager))
    # state_manager.add_state('custom', CustomLevelState(state_manager))
    state_manager.add_state('level_select',LevelSelectState('level_select', state_manager))
    state_manager.add_state('settings', SettingsState(state_manager))
    state_manager.add_state('level_builder', LevelBuilderState(state_manager))
    
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