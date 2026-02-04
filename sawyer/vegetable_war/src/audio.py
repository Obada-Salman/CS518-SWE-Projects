import pygame
import random
import os
import sys

# Use PulseAudio on Linux systems (especially WSL)
if sys.platform.startswith('linux'):
    os.environ['SDL_AUDIODRIVER'] = 'pulse'

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self.audio_available = True
        self.music_loaded = False
        self.music_volume = 0.7  # Music volume (0.0 to 1.0)
        self.sfx_volume = 0.5    # Sound effects volume
        
        # Get the assets directory
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.sounds_path = os.path.join(self.base_path, 'assets', 'sounds')
        
        # Try to initialize audio, but don't fail if it's not available
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.set_reserved(1)  # Reserve one channel for music
        except Exception as e:
            print(f"Warning: Audio not available ({e}). Game will run without sound.")
            self.audio_available = False
            self.sfx_enabled = False
            return
        
        # Set default volumes
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except:
            pass
        
        self._create_procedural_sounds()
        self._load_music()
    
    def _create_procedural_sounds(self):
        """Create procedural sounds programmatically"""
        # Note: This creates simple placeholder sounds
        # You can replace with actual .wav files later
        
        try:
            # Create a simple beep sound for attack
            self.sounds['attack'] = self._generate_beep(440, 0.1)
            self.sounds['super_attack'] = self._generate_beep(880, 0.3)
            self.sounds['hit'] = self._generate_beep(220, 0.05)
            self.sounds['jump'] = self._generate_beep(600, 0.1)
            self.sounds['emotion_full'] = self._generate_beep(1000, 0.2)
            self.sounds['level_complete'] = self._generate_beep(800, 0.3)
        except Exception as e:
            print(f"Could not create procedural sounds: {e}")
    
    def _load_music(self):
        """Load background music from files"""
        if not self.audio_available:
            return
        
        try:
            # Look for music files in the sounds directory
            if os.path.exists(self.sounds_path):
                files = os.listdir(self.sounds_path)
                for file in sorted(files):
                    if file.lower().endswith(('.mp3', '.ogg', '.wav', '.flac')):
                        music_path = os.path.join(self.sounds_path, file)
                        try:
                            pygame.mixer.music.load(music_path)
                            self.music_loaded = True
                            print(f"✓ Loaded music: {file}")
                            return
                        except Exception as load_err:
                            print(f"⚠ Could not load {file}: {load_err}")
                            continue
                if not self.music_loaded:
                    print(f"⚠ No compatible audio files found in {self.sounds_path}")
            else:
                print(f"⚠ Sounds directory not found: {self.sounds_path}")
        except Exception as e:
            print(f"⚠ Error loading music: {e}")
    
    def _generate_beep(self, frequency, duration):
        """Generate a simple beep sound"""
        sample_rate = 22050
        num_samples = int(duration * sample_rate)
        
        import math
        import array
        
        frames = array.array('h')
        for i in range(num_samples):
            sample = int(32767 * 0.1 * math.sin(2 * math.pi * frequency * i / sample_rate))
            frames.append(sample)
        
        sound = pygame.mixer.Sound(buffer=frames)
        return sound
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.audio_available or not self.sfx_enabled or sound_name not in self.sounds:
            return
        
        try:
            self.sounds[sound_name].play()
        except Exception as e:
            pass  # Silently fail if audio unavailable
    
    def play_music(self, track_name=None):
        """Play background music"""
        if not self.audio_available:
            return
        
        if not self.music_enabled:
            return
        
        if not self.music_loaded:
            return
        
        try:
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 means loop infinitely
            print(f"▶ Playing music (volume: {self.music_volume})")
        except Exception as e:
            print(f"✗ Could not play music: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if not self.audio_available:
            return
        
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            pass  # Silently fail if audio unavailable
    
    def set_music_enabled(self, enabled):
        """Toggle music"""
        self.music_enabled = enabled
    
    def set_sfx_enabled(self, enabled):
        """Toggle sound effects"""
        self.sfx_enabled = enabled
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except:
            pass
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))


# Global sound manager instance
sound_manager = None

def init_sound_manager():
    """Initialize the global sound manager"""
    global sound_manager
    sound_manager = SoundManager()
    return sound_manager

def get_sound_manager():
    """Get the global sound manager"""
    global sound_manager
    if sound_manager is None:
        init_sound_manager()
    return sound_manager
