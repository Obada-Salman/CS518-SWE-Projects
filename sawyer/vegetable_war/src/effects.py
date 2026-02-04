import pygame
import random
import math
from constants import *

class Particle:
    """Simple particle for visual effects"""
    def __init__(self, x, y, vx, vy, lifetime, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = 5
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY * 0.5
        self.lifetime -= 1
    
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            size = max(1, self.size * (self.lifetime / self.max_lifetime))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(size))
    
    def is_alive(self):
        return self.lifetime > 0


class ParticleSystem:
    """Manages all particles in the game"""
    def __init__(self):
        self.particles = []
    
    def emit_hit(self, x, y, count=8, color=YELLOW):
        """Emit particles on hit"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 2
            particle = Particle(x, y, vx, vy, 20, color)
            self.particles.append(particle)
    
    def emit_tears(self, x, y, count=4):
        """Emit tear particles when emotional"""
        for _ in range(count):
            angle = random.uniform(-math.pi/4, -3*math.pi/4)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle = Particle(x, y, vx, vy, 30, BLUE)
            self.particles.append(particle)
    
    def emit_super_effect(self, x, y):
        """Emit particles for super attack"""
        for _ in range(16):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            particle = Particle(x, y, vx, vy, 25, PURPLE)
            self.particles.append(particle)
    
    def update(self):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()


class ScreenShake:
    """Simple screen shake effect"""
    def __init__(self, intensity=5, duration=10):
        self.intensity = intensity
        self.duration = duration
        self.timer = 0
        self.offset_x = 0
        self.offset_y = 0
    
    def update(self):
        if self.timer > 0:
            self.timer -= 1
            self.offset_x = random.randint(-self.intensity, self.intensity)
            self.offset_y = random.randint(-self.intensity, self.intensity)
        else:
            self.offset_x = 0
            self.offset_y = 0
    
    def start(self):
        self.timer = self.duration
    
    def get_offset(self):
        return (self.offset_x, self.offset_y)


class FloatingText:
    """Damage/score text that floats up"""
    def __init__(self, x, y, text, color=WHITE, lifetime=40):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.vy = -1
    
    def update(self):
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, screen, font):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            text_surface = font.render(self.text, True, self.color)
            screen.blit(text_surface, (int(self.x), int(self.y)))
    
    def is_alive(self):
        return self.lifetime > 0


class FloatingTextManager:
    """Manages floating text effects"""
    def __init__(self):
        self.texts = []
    
    def add_text(self, x, y, text, color=WHITE):
        self.texts.append(FloatingText(x, y, text, color))
    
    def update(self):
        for text in self.texts[:]:
            text.update()
            if not text.is_alive():
                self.texts.remove(text)
    
    def draw(self, screen, font):
        for text in self.texts:
            text.draw(screen, font)
