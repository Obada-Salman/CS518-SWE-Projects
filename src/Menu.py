import pygame
from settings import *
from button import Button
from Player import Player
import resource_path

class MainMenuState:
    def __init__(self, name, state_machine):
        self.name = name
        self.state_machine = state_machine
        self.BASE_WIDTH = BASE_WIDTH
        self.BASE_HEIGHT = BASE_HEIGHT
        self.setup_ui()
        
    def setup_ui(self):
        surface = pygame.display.get_surface()
        if surface:
            self.screen_width, self.screen_height = surface.get_size()
        else:
            self.screen_width, self.screen_height = self.BASE_WIDTH, self.BASE_HEIGHT
            
        scale_x = self.screen_width / self.BASE_WIDTH
        scale_y = self.screen_height / self.BASE_HEIGHT
        
        scale = min(scale_x, scale_y)
        self.scale = scale
        
        btn_width = int(200 * scale)
        btn_height = int(50 * scale)
        btn_spacing = int(60 * scale)
        font_size = max(int(36 * scale), 10)
        btn_font = pygame.font.SysFont(None, font_size)
        
        button_x = (self.screen_width // 2) - (btn_width // 2)
        button_y = (self.screen_height // 2) - int(100 * scale)
        self.story = Button(button_x, button_y, btn_width, btn_height, "Continue", btn_font, BLACK, WHITE)
        self.custom = Button(button_x, button_y + btn_spacing, btn_width, btn_height, "Custom Level", btn_font, BLACK, WHITE)
        self.setting = Button(button_x, button_y + btn_spacing * 2, btn_width, btn_height, "Settings", btn_font, BLACK, WHITE)
        self.level_bld = Button(button_x, button_y + btn_spacing * 3, btn_width, btn_height, "Level Builder", btn_font, BLACK, WHITE)
        self.gallery = Button(button_x, button_y + btn_spacing * 4, btn_width, btn_height, "Gallery", btn_font, BLACK, WHITE)
        self.quit = Button(button_x, button_y + btn_spacing * 5, btn_width, btn_height, "Quit", btn_font, RED, WHITE)

        save_btn_font = pygame.font.SysFont(None, max(int(26 * scale), 10))
        panel_w = int(300 * scale)
        panel_h = int(310 * scale)
        panel_x = int(24 * scale)
        panel_y = int(140 * scale)
        self.save_panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        slot_btn_h = int(44 * scale)
        arrow_w = int(42 * scale)
        action_btn_w = panel_w - int(32 * scale)
        action_x = panel_x + int(16 * scale)
        arrow_y = panel_y + int(88 * scale)

        self.slot_prev = Button(panel_x + int(16 * scale), arrow_y, arrow_w, slot_btn_h, "<", save_btn_font, BLACK, WHITE)
        self.slot_next = Button(panel_x + panel_w - arrow_w - int(16 * scale), arrow_y, arrow_w, slot_btn_h, ">", save_btn_font, BLACK, WHITE)

        self.btn_load_save = Button(action_x, panel_y + int(150 * scale), action_btn_w, slot_btn_h, "Load Save", save_btn_font, BLACK, WHITE)
        self.btn_new_game = Button(action_x, panel_y + int(200 * scale), action_btn_w, slot_btn_h, "New Game", save_btn_font, BLACK, WHITE)
        self.btn_delete_save = Button(action_x, panel_y + int(250 * scale), action_btn_w, slot_btn_h, "Delete Save", save_btn_font, RED, WHITE)

        # Confirmation UI for destructive save deletion.
        confirm_w = int(440 * scale)
        confirm_h = int(220 * scale)
        confirm_x = (self.screen_width - confirm_w) // 2
        confirm_y = (self.screen_height - confirm_h) // 2
        self.delete_confirm_rect = pygame.Rect(confirm_x, confirm_y, confirm_w, confirm_h)
        confirm_btn_w = int(130 * scale)
        confirm_btn_h = int(48 * scale)
        confirm_btn_y = confirm_y + confirm_h - confirm_btn_h - int(25 * scale)
        self.btn_confirm_delete_yes = Button(
            confirm_x + int(35 * scale),
            confirm_btn_y,
            confirm_btn_w,
            confirm_btn_h,
            "Delete",
            save_btn_font,
            RED,
            WHITE,
        )
        self.btn_confirm_delete_no = Button(
            confirm_x + confirm_w - confirm_btn_w - int(35 * scale),
            confirm_btn_y,
            confirm_btn_w,
            confirm_btn_h,
            "Cancel",
            save_btn_font,
            BLACK,
            WHITE,
        )

        self.username_font = pygame.font.SysFont(None, max(int(32 * scale), 14))
        input_width = int(320 * scale)
        input_height = int(44 * scale)
        input_x = (self.screen_width // 2) - (input_width // 2)
        input_y = max(110, button_y - int(80 * scale))
        self.username_rect = pygame.Rect(input_x, input_y, input_width, input_height)
        self.username_active = False
        if not hasattr(self, "username_input"):
            existing = getattr(getattr(self.state_machine, "score_tracker", None), "username", "player1")
            self.username_input = self._normalize_username(existing)
        if not hasattr(self, "selected_slot"):
            raw_slot = getattr(self.state_machine, "active_save_slot", 1)
            try:
                self.selected_slot = int(raw_slot)
            except (TypeError, ValueError):
                self.selected_slot = 1
        if not hasattr(self, "pending_delete_confirmation"):
            self.pending_delete_confirmation = False

        self._refresh_slot_data()
        
        if self.state_machine.max_unlocked_level <= 5:
            self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Backgrounds/Menu1.png'))
        elif self.state_machine.max_unlocked_level <= 10:
            self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Backgrounds/Menu2.png'))
        else:
            self.background = pygame.image.load(resource_path.get_resource_path('assets/images/Backgrounds/Menu3.png'))
            
        self.scaled_bg = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
    def update(self, events, dt):
        for event in events:
            if self.pending_delete_confirmation:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pending_delete_confirmation = False
                    continue
                if self.btn_confirm_delete_yes.is_clicked(event):
                    self._confirm_delete_selected_save()
                    continue
                if self.btn_confirm_delete_no.is_clicked(event):
                    self.pending_delete_confirmation = False
                    continue
                if event.type == pygame.VIDEORESIZE:
                    self.__init__(self.name, self.state_machine)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.username_active = self.username_rect.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and self.username_active:
                if event.key == pygame.K_RETURN:
                    self._apply_username()
                    self.username_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.username_input = self.username_input[:-1]
                else:
                    typed = event.unicode
                    if typed and typed.isprintable() and len(self.username_input) < 32:
                        self.username_input += typed

            if self.story.is_clicked(event):
                self._apply_username()
                self.state_machine.transition('level_select')
            elif self.slot_prev.is_clicked(event):
                self._change_slot(-1)
            elif self.slot_next.is_clicked(event):
                self._change_slot(1)
            elif self.btn_load_save.is_clicked(event):
                self._load_selected_save()
            elif self.btn_new_game.is_clicked(event):
                self._new_game_selected_slot()
            elif self.btn_delete_save.is_clicked(event):
                self.pending_delete_confirmation = True
            elif self.custom.is_clicked(event):
                self.state_machine.transition('custom_select')
            elif self.setting.is_clicked(event):
                self.state_machine.transition('settings')
            elif self.level_bld.is_clicked(event):
                self.state_machine.transition('level_builder')
            elif self.gallery.is_clicked(event):
                self.state_machine.transition('gallery')
            elif self.quit.is_clicked(event):
                self.state_machine.quit()
            elif event.type == pygame.VIDEORESIZE:
                self.__init__(self.name, self.state_machine)  
                
    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.scaled_bg, (0, 0))
        title = pygame.font.Font(None, 74).render("Onions May Cry", True, BLACK)
        surface.blit(title, (self.screen_width//2 - title.get_width()//2, 50))

        label = self.username_font.render("Player Name", True, BLACK)
        surface.blit(label, (self.username_rect.x, self.username_rect.y - 24))
        border_color = RED if self.username_active else BLACK
        pygame.draw.rect(surface, WHITE, self.username_rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.username_rect, 2, border_radius=8)
        shown_name = self.username_input if self.username_input else "player1"
        name_text = self.username_font.render(shown_name, True, BLACK)
        surface.blit(name_text, (self.username_rect.x + 10, self.username_rect.y + 10))

        self.story.draw(surface)
        self.custom.draw(surface)
        self.setting.draw(surface)
        self.level_bld.draw(surface)
        self.gallery.draw(surface)
        self.quit.draw(surface)

        pygame.draw.rect(surface, (245, 240, 225), self.save_panel_rect, border_radius=16)
        pygame.draw.rect(surface, BLACK, self.save_panel_rect, 2, border_radius=16)

        panel_title_font = pygame.font.SysFont(None, max(int(30 * self.scale), 12))
        slot_text = panel_title_font.render(f"Save Slot {self.selected_slot}", True, BLACK)
        slot_text_y = self.save_panel_rect.y + int(18 * self.scale)
        surface.blit(slot_text, (self.save_panel_rect.centerx - slot_text.get_width() // 2, slot_text_y))

        slot_info = self._get_selected_slot_info()
        if slot_info and slot_info.exists:
            info_line_1 = f"{slot_info.username}"
            info_line_2 = f"Unlocked: {slot_info.max_unlocked_level}/15"
        else:
            info_line_1 = "Empty slot"
            info_line_2 = "Unlocked: 1/15"

        info_font = pygame.font.SysFont(None, max(int(24 * self.scale), 10))
        info_1 = info_font.render(info_line_1, True, BLACK)
        info_2 = info_font.render(info_line_2, True, BLACK)
        surface.blit(info_1, (self.save_panel_rect.centerx - info_1.get_width() // 2, self.save_panel_rect.y + int(50 * self.scale)))
        surface.blit(info_2, (self.save_panel_rect.centerx - info_2.get_width() // 2, self.save_panel_rect.y + int(72 * self.scale)))

        self.slot_prev.draw(surface)
        self.slot_next.draw(surface)
        self.btn_delete_save.draw(surface)
        self.btn_new_game.draw(surface)
        self.btn_load_save.draw(surface)

        if self.pending_delete_confirmation:
            self._draw_delete_confirmation(surface)
        
    def enter(self):
        self.__init__(self.name, self.state_machine)
        self.play_music()

    def _normalize_username(self, username):
        normalized = (username or "").strip()
        if not normalized:
            normalized = "player1"
        return normalized[:32]

    def _apply_username(self):
        if hasattr(self.state_machine, "set_player_username"):
            self.username_input = self.state_machine.set_player_username(self.username_input)
        else:
            self.username_input = self._normalize_username(self.username_input)

    def _refresh_slot_data(self):
        if hasattr(self.state_machine, "get_save_slots"):
            self.save_slots = self.state_machine.get_save_slots()
        else:
            self.save_slots = []

    def _get_selected_slot_info(self):
        for slot_info in getattr(self, "save_slots", []):
            if slot_info.slot == self.selected_slot:
                return slot_info
        return None

    def _change_slot(self, delta):
        slot_count = max(1, int(getattr(getattr(self.state_machine, "save_manager", None), "slot_count", 3)))
        self.selected_slot += delta
        if self.selected_slot < 1:
            self.selected_slot = slot_count
        elif self.selected_slot > slot_count:
            self.selected_slot = 1
        self._refresh_slot_data()
        self.setup_ui()
        self.play_music()

    def _load_selected_save(self):
        if hasattr(self.state_machine, "load_save_slot"):
            self.state_machine.load_save_slot(self.selected_slot)
            score_tracker = getattr(self.state_machine, "score_tracker", None)
            self.username_input = self._normalize_username(getattr(score_tracker, "username", "player1"))
        self._refresh_slot_data()
        self.setup_ui()
        self.play_music()

    def _new_game_selected_slot(self):
        if hasattr(self.state_machine, "create_new_game"):
            self.state_machine.create_new_game(self.selected_slot)
            score_tracker = getattr(self.state_machine, "score_tracker", None)
            self.username_input = self._normalize_username(getattr(score_tracker, "username", "player1"))
        self._refresh_slot_data()
        self.setup_ui()
        self.play_music()

    def play_music(self):
        if self.state_machine.max_unlocked_level > 10:
            track = 'menu_theme2.ogg'
        else:
            track = 'menu_theme.ogg'
        if track and hasattr(self.state_machine, 'sound_manager'):
            self.state_machine.sound_manager.play_music_file(track)

    def _delete_selected_save(self):
        if hasattr(self.state_machine, "delete_save_slot"):
            self.state_machine.delete_save_slot(self.selected_slot)
            score_tracker = getattr(self.state_machine, "score_tracker", None)
            self.username_input = self._normalize_username(getattr(score_tracker, "username", "player1"))
        self._refresh_slot_data()

        self.setup_ui()
        self.play_music()

    def _confirm_delete_selected_save(self):
        self._delete_selected_save()
        self.pending_delete_confirmation = False

    def _draw_delete_confirmation(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, WHITE, self.delete_confirm_rect, border_radius=12)
        pygame.draw.rect(surface, BLACK, self.delete_confirm_rect, 2, border_radius=12)

        title_font = pygame.font.SysFont(None, 40)
        body_font = pygame.font.SysFont(None, 30)
        title = title_font.render("Delete Save Slot?", True, BLACK)
        line1 = body_font.render(f"This will erase Slot {self.selected_slot} progress.", True, BLACK)
        line2 = body_font.render("This action cannot be undone.", True, RED)

        surface.blit(
            title,
            (
                self.delete_confirm_rect.centerx - title.get_width() // 2,
                self.delete_confirm_rect.y + 24,
            ),
        )
        surface.blit(
            line1,
            (
                self.delete_confirm_rect.centerx - line1.get_width() // 2,
                self.delete_confirm_rect.y + 78,
            ),
        )
        surface.blit(
            line2,
            (
                self.delete_confirm_rect.centerx - line2.get_width() // 2,
                self.delete_confirm_rect.y + 114,
            ),
        )

        self.btn_confirm_delete_yes.draw(surface)
        self.btn_confirm_delete_no.draw(surface)
        
                