import random

import pygame

import resource_path


class SequencePlayer:
    """Modal dialogue/cutscene sequencer for gameplay states."""

    def __init__(self):
        self._sequence_type = None
        self._entries = []
        self._index = 0
        self._on_complete = None
        self._font = pygame.font.Font(None, 30)
        self._hint_font = pygame.font.Font(None, 22)
        self._image_cache = {}

    @property
    def active(self):
        return bool(self._entries)

    def start_dialogue(self, lines, on_complete=None, shuffle=False, max_lines=None):
        entries = list(lines)
        if shuffle:
            random.shuffle(entries)
        if max_lines is not None:
            entries = entries[:max_lines]
        if not entries:
            return

        self._sequence_type = "dialogue"
        self._entries = entries
        self._index = 0
        self._on_complete = on_complete

    def start_cutscene(self, frames, on_complete=None):
        entries = list(frames)
        if not entries:
            return

        self._sequence_type = "cutscene"
        self._entries = entries
        self._index = 0
        self._on_complete = on_complete

    def process_events(self, events):
        if not self.active:
            return False

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_e):
                    self._advance()
                    return True
                if event.key == pygame.K_ESCAPE:
                    self._finish()
                    return True

        return False

    def _advance(self):
        if not self.active:
            return

        self._index += 1
        if self._index >= len(self._entries):
            self._finish()

    def _finish(self):
        on_complete = self._on_complete
        self._entries = []
        self._index = 0
        self._sequence_type = None
        self._on_complete = None
        if on_complete:
            on_complete()

    def draw(self, surface):
        if not self.active:
            return

        entry = self._entries[self._index]
        if self._sequence_type == "dialogue":
            self._draw_dialogue(surface, entry)
        elif self._sequence_type == "cutscene":
            self._draw_cutscene(surface, entry)

    def _draw_dialogue(self, surface, entry):
        width, height = surface.get_size()
        panel_h = int(height * 0.28)
        panel_rect = pygame.Rect(20, height - panel_h - 20, width - 40, panel_h)

        backdrop = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        backdrop.fill((0, 0, 0, 200))
        surface.blit(backdrop, panel_rect.topleft)
        pygame.draw.rect(surface, (240, 240, 240), panel_rect, 3)

        speaker = str(entry[0]) if len(entry) > 0 else ""
        line = str(entry[1]) if len(entry) > 1 else ""

        speaker_text = self._font.render(f"{speaker}:", True, (255, 228, 170))
        surface.blit(speaker_text, (panel_rect.x + 18, panel_rect.y + 14))

        wrapped = self._wrap_text(line, self._font, panel_rect.width - 36)
        y = panel_rect.y + 48
        for part in wrapped[:4]:
            line_surface = self._font.render(part, True, (245, 245, 245))
            surface.blit(line_surface, (panel_rect.x + 18, y))
            y += 30

        hint = self._hint_font.render("Press E / Space / Enter to continue", True, (190, 190, 190))
        surface.blit(hint, (panel_rect.right - hint.get_width() - 16, panel_rect.bottom - hint.get_height() - 10))

    def _draw_cutscene(self, surface, entry):
        width, height = surface.get_size()
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((12, 12, 18, 210))
        surface.blit(overlay, (0, 0))

        image_path = entry.get("image")
        caption = entry.get("text", "")

        frame_rect = pygame.Rect(int(width * 0.12), int(height * 0.08), int(width * 0.76), int(height * 0.64))
        image = self._load_image(image_path) if image_path else None
        if image is not None:
            scaled = pygame.transform.smoothscale(image, (frame_rect.width, frame_rect.height))
            surface.blit(scaled, frame_rect.topleft)
        else:
            placeholder = pygame.Surface((frame_rect.width, frame_rect.height))
            placeholder.fill((34, 36, 44))
            surface.blit(placeholder, frame_rect.topleft)
            label = self._font.render("Cutscene Frame Placeholder", True, (220, 220, 220))
            surface.blit(label, (frame_rect.centerx - label.get_width() // 2, frame_rect.centery - label.get_height() // 2))

        pygame.draw.rect(surface, (230, 230, 230), frame_rect, 3)

        text_rect = pygame.Rect(int(width * 0.10), int(height * 0.76), int(width * 0.80), int(height * 0.18))
        text_bg = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 190))
        surface.blit(text_bg, text_rect.topleft)
        pygame.draw.rect(surface, (230, 230, 230), text_rect, 2)

        wrapped = self._wrap_text(caption, self._font, text_rect.width - 28)
        y = text_rect.y + 12
        for part in wrapped[:3]:
            line_surface = self._font.render(part, True, (245, 245, 245))
            surface.blit(line_surface, (text_rect.x + 14, y))
            y += 30

        hint = self._hint_font.render("Press E / Space / Enter to continue (Esc to skip)", True, (190, 190, 190))
        surface.blit(hint, (text_rect.right - hint.get_width() - 10, text_rect.bottom - hint.get_height() - 8))

    def _load_image(self, image_path):
        if image_path in self._image_cache:
            return self._image_cache[image_path]

        try:
            image = pygame.image.load(resource_path.get_resource_path(image_path)).convert_alpha()
        except Exception:
            image = None

        self._image_cache[image_path] = image
        return image

    @staticmethod
    def _wrap_text(text, font, max_width):
        words = str(text).split()
        if not words:
            return [""]

        lines = []
        current = words[0]
        for word in words[1:]:
            trial = f"{current} {word}"
            if font.size(trial)[0] <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines
