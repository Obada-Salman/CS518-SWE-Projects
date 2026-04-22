
from sound_manager import SoundManager
from score_tracker import ScoreTracker
from save_manager import SaveManager


class StateManager:
    def __init__(self):
        self.states = {}
        self.previous_state_name = None
        self.current_state = None
        self.current_state_name = None
        self.window_should_close = False
        self.window_width = 1280
        self.window_height = 720
        self.sound_manager = SoundManager()
        self.score_tracker = ScoreTracker()
        self.save_manager = SaveManager()
        self.active_save_slot = 1
        self.max_unlocked_level = 1
        self.state_music = {
            'menu': 'menu_theme.ogg',
            'level_select': 'menu_theme.ogg',
                'settings': 'menu_theme.ogg',
                'custom': 'Surface.ogg',
                'level_builder': 'Waiting.ogg',
        }

        # collectibles that save across levels
        self.water_collected = 0
        self.sunlight_collected = 0
        self.nutrients_collected = 0
        self.load_save_slot(self.active_save_slot)

    def _default_progress(self):
        return {
            'username': 'player1',
            'max_unlocked_level': 1,
            'water_collected': 0,
            'sunlight_collected': 0,
            'nutrients_collected': 0,
            'current_story_level': 1,
        }

    def set_player_username(self, username: str) -> str:
        cleaned = (username or "").strip()
        if not cleaned:
            cleaned = "player1"
        cleaned = cleaned[:32]
        self.score_tracker.username = cleaned
        self.autosave()
        return cleaned

    def get_water_collected(self):
        return self.water_collected
    
    def get_sunlight_collected(self):
        return self.sunlight_collected
    
    def get_nutrients_collected(self):
        return self.nutrients_collected
    
    def add_water(self, amount):
        self.water_collected += amount
        if self.water_collected < 0:
            self.water_collected = 0
        self.autosave()

    def add_sunlight(self, amount):
        self.sunlight_collected += amount
        if self.sunlight_collected < 0:
            self.sunlight_collected = 0
        self.autosave()

    def add_nutrients(self, amount):
        self.nutrients_collected += amount
        if self.nutrients_collected < 0:
            self.nutrients_collected = 0
        self.autosave()

    def set_max_unlocked_level(self, level: int):
        self.max_unlocked_level = max(1, int(level))
        self.autosave()

    def get_save_slots(self):
        return self.save_manager.list_slots()

    def get_active_slot_summary(self):
        for slot in self.get_save_slots():
            if slot.slot == self.active_save_slot:
                return slot
        return None

    def serialize_progress(self):
        current_story_level = 1
        story_state = self.states.get('story')
        if story_state and hasattr(story_state, 'current_level'):
            try:
                current_story_level = max(1, int(story_state.current_level))
            except (TypeError, ValueError):
                current_story_level = 1

        return {
            'username': self.score_tracker.username,
            'max_unlocked_level': int(max(1, self.max_unlocked_level)),
            'water_collected': int(max(0, self.water_collected)),
            'sunlight_collected': int(max(0, self.sunlight_collected)),
            'nutrients_collected': int(max(0, self.nutrients_collected)),
            'current_story_level': current_story_level,
        }

    def apply_progress(self, payload):
        if not isinstance(payload, dict):
            return

        self.score_tracker.username = str(payload.get('username', 'player1')).strip()[:32] or 'player1'
        self.max_unlocked_level = max(1, int(payload.get('max_unlocked_level', 1)))
        self.water_collected = max(0, int(payload.get('water_collected', 0)))
        self.sunlight_collected = max(0, int(payload.get('sunlight_collected', 0)))
        self.nutrients_collected = max(0, int(payload.get('nutrients_collected', 0)))

        story_level = max(1, int(payload.get('current_story_level', 1)))
        if story_level > self.max_unlocked_level:
            story_level = self.max_unlocked_level
        if 'story' in self.states:
            self.set_story_level(story_level)

    def load_save_slot(self, slot: int):
        self.active_save_slot = min(max(int(slot), 1), self.save_manager.slot_count)
        payload = self.save_manager.load_slot(self.active_save_slot)
        if payload is None:
            self.apply_progress(self._default_progress())
            return False
        self.apply_progress(payload)
        return True

    def create_new_game(self, slot: int | None = None):
        if slot is not None:
            self.active_save_slot = min(max(int(slot), 1), self.save_manager.slot_count)
        self.apply_progress(self._default_progress())
        self.autosave()

    def delete_save_slot(self, slot: int):
        target_slot = min(max(int(slot), 1), self.save_manager.slot_count)
        deleted = self.save_manager.delete_slot(target_slot)
        if target_slot == self.active_save_slot:
            self.create_new_game(target_slot)
        return deleted

    def autosave(self):
        self.save_manager.save_slot(self.active_save_slot, self.serialize_progress())
    
    def add_state(self, name, state):
        self.states[name] = state
    
    def transition(self ,name):
        if(name in self.states):
            self.previous_state_name = self.current_state_name
        # If in the future we want to add additional things when entering and leaving states, we can add them here.
        # Can only be done if they have leave and enter functions.
            if self.current_state and hasattr(self.current_state, 'leave'):
                self.current_state.leave()
            self.current_state = self.states[name]
            self.current_state_name = name
            if hasattr(self.current_state, 'enter'):
                if not (name in ['story', 'custom'] and self.previous_state_name == 'pause'):
                    self.current_state.enter()
            
            self._play_state_music(name)
        return

    def set_story_level(self, level_number):
        story_state = self.states.get('story')
        if story_state and hasattr(story_state, 'set_level'):
            story_state.set_level(level_number)
    
    def set_custom_level(self, level_number):
        custom_state = self.states.get('custom')
        if custom_state and hasattr(custom_state, 'set_level'):
            custom_state.set_level(level_number)

    def _play_state_music(self, state_name):
        track = self.state_music.get(state_name)
        if track:
            self.sound_manager.play_music_file(track)

    def update(self, events):
        if self.current_state:
            self.current_state.update(events)

    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)
            
    def remove_state(self, name):
        if name in self.states:
            del self.states[name]
            
    def quit(self):
        self.autosave()
        self.sound_manager.stop_music()
        self.window_should_close = True