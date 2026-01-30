import pygame
import sys
from settings import *
from state_manager import GameStateManager

from MenuState import MainMenuState    

from PauseState import PauseState       
from LevelSelect import LevelSelectState
from GalleryState import GalleryState
from LevelOne import LevelOne
from LevelTwo import LevelTwo
from LevelThree import LevelThree

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Onions May Cry")
    clock = pygame.time.Clock()

    manager = GameStateManager()
    
    manager.add_state('menu', MainMenuState(manager))
    manager.add_state('pause', PauseState(manager))
    manager.add_state('level_select', LevelSelectState(manager))
    manager.add_state('gallery', GalleryState(manager))
    
    manager.add_state('level_one', LevelOne(manager))
    manager.add_state('level_two', LevelTwo(manager))
    manager.add_state('level_three', LevelThree(manager))
    
    manager.set_state('menu')

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.update(events)
        manager.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()