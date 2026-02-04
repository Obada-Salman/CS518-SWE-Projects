import pygame

pygame.mixer.init()
background_music = pygame.mixer.Sound("garden_background.mp3")
background_music.set_volume(.5)
click_sound = pygame.mixer.Sound("mouse_click.mp3")
click_sound.set_volume(.75)