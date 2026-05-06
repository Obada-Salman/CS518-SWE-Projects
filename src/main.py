import pygame
from settings import *
import sys
from state_manager import StateManager
from Menu import MainMenuState
from StoryState import StoryState
from SettingsState import SettingsState
from LevelSelect import LevelSelectState
from LevelbuilderState import LevelBuilderState
from PauseState import PauseState
from CustomLevelSelect import CustomLevelSelect
from CustomState import CustomState
from GalleryState import GalleryState
from HowToPlayState import HowToPlayState

def main():
    pygame.init()
    screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT))
    pygame.display.set_caption("Onions May Cry")
    clock = pygame.time.Clock()
    state_manager = StateManager()
    
    state_manager.add_state('menu', MainMenuState('menu', state_manager))
    state_manager.add_state('story', StoryState(state_manager))
    state_manager.add_state('level_select',LevelSelectState('level_select', state_manager))
    state_manager.add_state('custom_select', CustomLevelSelect('custom_select',state_manager))
    state_manager.add_state('settings', SettingsState(state_manager))
    state_manager.add_state('how_to_play', HowToPlayState(state_manager))
    state_manager.add_state('custom', CustomState(state_manager))
    state_manager.add_state('level_builder', LevelBuilderState(state_manager))
    state_manager.add_state('pause', PauseState('pause', state_manager))
    state_manager.add_state('gallery', GalleryState('gallery', state_manager))
    state_manager.load_save_slot(state_manager.active_save_slot)
    
    state_manager.transition('menu')
    
    while not state_manager.window_should_close:
        events = pygame.event.get()
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000.0
        for event in events:
            if event.type == pygame.QUIT:
                state_manager.quit()
        # state_manager.set_max_unlocked_level(15) # for debugging
        state_manager.update(events, dt)
        state_manager.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()