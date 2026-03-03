from pathlib import Path
import pygame


class SoundManager:
    def __init__(self):
        self.enabled = self._init_mixer()
        self.current_track = None
        self.volume = 0.5
        self.sounds_dir = Path(__file__).resolve().parent.parent / "assets" / "sounds"

    def _init_mixer(self):
        if pygame.mixer.get_init():
            return True

        try:
            pygame.mixer.init()
            return True
        except pygame.error as err:
            print(f"[SoundManager] Mixer unavailable: {err}")
            return False

    def set_enabled(self, enabled):
        self.enabled = enabled and pygame.mixer.get_init() is not None
        if not self.enabled and pygame.mixer.get_init():
            pygame.mixer.music.stop()
            self.current_track = None

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, float(volume)))
        if self.enabled:
            pygame.mixer.music.set_volume(self.volume)

    def play_music_file(self, file_name, loops=-1, fade_ms=300):
        if not self.enabled or not file_name:
            return

        if self.current_track == file_name:
            return

        track_path = self.sounds_dir / file_name
        if not track_path.exists():
            print(f"[SoundManager] Missing music file: {track_path}")
            return

        try:
            pygame.mixer.music.load(str(track_path))
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            self.current_track = file_name
        except pygame.error as err:
            print(f"[SoundManager] Failed to play {track_path.name}: {err}")

    def stop_music(self, fade_ms=150):
        if not self.enabled:
            return
        pygame.mixer.music.fadeout(fade_ms)
        self.current_track = None