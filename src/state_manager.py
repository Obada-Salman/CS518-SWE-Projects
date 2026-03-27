
from sound_manager import SoundManager
from score_tracker import ScoreTracker


class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.current_state_name = None
        self.window_should_close = False
        self.window_width = 800
        self.window_height = 600
        self.sound_manager = SoundManager()
        self.score_tracker = ScoreTracker()
        self.max_unlocked_level = 1
        self.state_music = {
            'menu': 'menu_theme.ogg',
            'level_select': 'menu_theme.ogg',
        }
    
    def add_state(self, name, state):
        self.states[name] = state
    
    def transition(self ,name):
        if(name in self.states):
            previous_state_name = self.current_state_name
        # If in the future we want to add additional things when entering and leaving states, we can add them here.
        # Can only be done if they have leave and enter functions.
            if self.current_state and hasattr(self.current_state, 'leave'):
                self.current_state.leave()
            self.current_state = self.states[name]
            self.current_state_name = name
            if hasattr(self.current_state, 'enter'):
                if not (name == 'story' and previous_state_name == 'pause'):
                    self.current_state.enter()
            self._play_state_music(name)
        return

    def set_story_level(self, level_number):
        story_state = self.states.get('story')
        if story_state and hasattr(story_state, 'set_level'):
            story_state.set_level(level_number)

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
        self.sound_manager.stop_music()
        self.window_should_close = True