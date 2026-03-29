import pygame
from configs import *

class SpriteHandler:
    def __init__(self, sheet_path, type='enemy_carrot', scale=1, anim_time=7):
        self.sheet = pygame.image.load(sheet_path).convert_alpha()
        if scale != 1:
            self.sheet = pygame.transform.scale(
                self.sheet,
                (self.sheet.get_width() * scale, self.sheet.get_height() * scale),
            )
        self.type = type
        self.scale = scale

        # animation attributes
        self.direction = 1  # 0 = left, 1 = right
        self.state = 0      # 0 = idle, 1 = walk, 2 = jump/fall
        self.anim_speed = anim_time
        self.anim_counter = 0
        self.frame_idx = 0

        self.cfg = CONFIGS.get(type)

        # cache parsed frames so we don't do it each time
        self._all_frames = self.parse_frames()

    def parse_frames(self):
        frames = []
        sheet_length = self.cfg["cols"]
        sprite_width = self.cfg["frame_width"] * self.scale
            
        for i in range(sheet_length):
            frame = self.sheet.subsurface(
                (i * sprite_width, 0, sprite_width, self.sheet.get_height())
            )
            frames.append(frame)
        return frames

    def get_current_frames(self, direction=None, state=None):
        dir_idx = self.direction if direction is None else direction
        st_idx = self.state if state is None else state

        frames = self._all_frames
        idle_left_anim = self.cfg["animations"]["idle_left"]
        idle_right_anim = self.cfg["animations"]["idle_right"]
        walk_left_anim = self.cfg["animations"]["walk_left"]
        walk_right_anim = self.cfg["animations"]["walk_right"]
        jump_left_anim = self.cfg["animations"]["jump_left"]
        jump_right_anim = self.cfg["animations"]["jump_right"]

        if dir_idx == 0:  # left
            if st_idx == 0:  # idle
                return [frames[i] for i in idle_left_anim]
            elif st_idx == 1: # walk
                return [frames[i] for i in walk_left_anim]
            elif st_idx == 2:  # jump/fall
                return [frames[i] for i in jump_left_anim]
        else:  # right
            if st_idx == 0:
                return [frames[i] for i in idle_right_anim]
            elif st_idx == 1:
                return [frames[i] for i in walk_right_anim]
            elif st_idx == 2:
                return [frames[i] for i in jump_right_anim]
        # fallback to full list
        return frames
    
    def get_current_frame(self):
        frames = self.get_current_frames()
        
        if not frames:
            return None
        
        return frames[self.frame_idx]

    def update(self, direction=None, state=None):
        if direction is not None:
            self.direction = direction
        if state is not None:
            if state != self.state:
                # reset animation when state changes
                self.frame_idx = 0
                self.anim_counter = 0
            self.state = state

        frames = self.get_current_frames()

        self.anim_counter += 1
        if self.anim_counter >= self.anim_speed:
            self.anim_counter = 0
            self.frame_idx = (self.frame_idx + 1) % len(frames)

    def draw(self, surface, x, y):
        frames = self.get_current_frames()
        if not frames:
            return
        frame = frames[self.frame_idx]
        surface.blit(frame, (x, y))