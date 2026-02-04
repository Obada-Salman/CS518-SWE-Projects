import pygame
import sys
import os

# Add the src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import *

class Cutscene:
    def __init__(self, dialogue_lines, cutscene_type="story"):
        self.dialogue_lines = dialogue_lines
        self.cutscene_type = cutscene_type
        self.current_line = 0
        self.line_timer = 0
        self.is_complete = False
    
    def update(self):
        """Update cutscene"""
        self.line_timer += 1
        if self.line_timer > 180:  # 3 seconds per line
            self.line_timer = 0
            self.current_line += 1
            if self.current_line >= len(self.dialogue_lines):
                self.is_complete = True
    
    def handle_input(self, keys):
        """Allow skipping with space"""
        if keys[pygame.K_SPACE]:
            self.line_timer = 120
    
    def draw(self, screen, font, large_font):
        """Draw cutscene"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        if self.current_line < len(self.dialogue_lines):
            dialogue = self.dialogue_lines[self.current_line]
            
            # Draw dialogue box
            box_height = 150
            box_y = SCREEN_HEIGHT - box_height
            pygame.draw.rect(screen, (50, 50, 50), (20, box_y, SCREEN_WIDTH - 40, box_height))
            pygame.draw.rect(screen, WHITE, (20, box_y, SCREEN_WIDTH - 40, box_height), 3)
            
            # Draw text
            lines = self._wrap_text(dialogue, 80)
            y_offset = box_y + 20
            for line in lines:
                text_surface = font.render(line, True, WHITE)
                screen.blit(text_surface, (40, y_offset))
                y_offset += 30
            
            # Continue indicator
            if self.line_timer > 60:
                continue_text = font.render("Press SPACE to continue", True, YELLOW)
                screen.blit(continue_text, (SCREEN_WIDTH - 300, box_y + box_height - 40))
    
    def _wrap_text(self, text, char_limit):
        """Wrap text to fit in box"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) < char_limit:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word + " "
        
        if current_line:
            lines.append(current_line)
        
        return lines


class StoryManager:
    def __init__(self):
        self.cutscenes = {}
        self.current_cutscene = None
        self.last_cutscene_key = None
        self._setup_cutscenes()
    
    def _setup_cutscenes(self):
        """Setup all cutscenes in the game"""
        
        # Intro cutscene
        self.cutscenes["intro"] = Cutscene([
            "You are an onion, guardian of the garden soil.",
            "For generations, your kind has thrived, absorbing nutrients, water, and sunlight.",
            "But today, darkness approaches...",
            "Beans, Peas, and Garlic - vegetables that compete for the same resources.",
            "They seek to overtake your territory and consume all the garden has to offer!",
            "You must stand against them. Only your emotions will give you strength.",
            "The more you fight, the more emotional you become.",
            "And when your emotion reaches its peak, unleash your most powerful attack!",
            "Let them know what it means to face an ONION ON THE VERGE OF CRYING!"
        ])
        
        # Level 1 intro
        self.cutscenes["level1_intro"] = Cutscene([
            "Stage 1: The Bean Invasion",
            "Beans have taken root in your garden.",
            "They seek the same nutrients as you.",
            "Stop them before they spread further!"
        ])
        
        # Level 1 outro
        self.cutscenes["level1_outro"] = Cutscene([
            "You have defeated the bean forces!",
            "Your layers grow thicker with each victory.",
            "But this is only the beginning...",
            "More invaders approach!"
        ])
        
        # Level 2 intro
        self.cutscenes["level2_intro"] = Cutscene([
            "Stage 2: The Pea Swarm",
            "The Peas move with incredible speed.",
            "Their hunger for sunlight knows no bounds.",
            "You must be swift and precise!"
        ])
        
        # Level 2 outro
        self.cutscenes["level2_outro"] = Cutscene([
            "The swift Pea forces have been repelled!",
            "Your emotional strength grows.",
            "But the greatest threat still lies ahead...",
            "A leader has emerged from among the invaders..."
        ])
        
        # Level 3 intro
        self.cutscenes["level3_intro"] = Cutscene([
            "Stage 3: The Garlic Conspiracy",
            "The Giant Garlic General commands the invasion.",
            "Its pungent aroma has coordinated the bean and pea forces.",
            "This is the final battle. Everything you love depends on victory!",
            "BECOME ONE WITH YOUR EMOTIONS!",
            "SHOW THEM THE POWER OF AN ONION'S TEARS!"
        ])
        
        # Victory cutscene
        self.cutscenes["victory"] = Cutscene([
            "You have triumphed!",
            "The invaders have been repelled.",
            "The garden belongs to you once more.",
            "The soil is rich with nutrients,",
            "The sun warms your layers,",
            "And the water quenches your roots.",
            "You may shed layers, but your spirit remains strong.",
            "You are an ONION THAT MAY CRY,",
            "But one that will never break.",
            "The garden is safe... for now."
        ])
        
        # Game Over cutscene
        self.cutscenes["gameover"] = Cutscene([
            "Your layers have been completely shed...",
            "Your essence fades into the soil.",
            "The invaders have claimed the garden.",
            "But your sacrifice will not be forgotten...",
            "From the darkness of soil, new growth will come.",
            "The cycle continues..."
        ])
    
    def start_cutscene(self, cutscene_key):
        """Start a specific cutscene"""
        if cutscene_key in self.cutscenes:
            self.current_cutscene = self.cutscenes[cutscene_key]
            self.last_cutscene_key = cutscene_key
            return True
        return False
    
    def is_cutscene_playing(self):
        """Check if a cutscene is currently active"""
        return self.current_cutscene is not None and not self.current_cutscene.is_complete
    
    def update(self, keys):
        """Update current cutscene"""
        if self.current_cutscene:
            self.current_cutscene.update()
            self.current_cutscene.handle_input(keys)
            if self.current_cutscene.is_complete:
                self.current_cutscene = None
    
    def draw(self, screen, font, large_font):
        """Draw current cutscene"""
        if self.current_cutscene:
            self.current_cutscene.draw(screen, font, large_font)
