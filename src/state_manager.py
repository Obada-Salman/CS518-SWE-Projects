
class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.window_should_close = False
        self.window_width = 800
        self.window_height = 600
    
    def add_state(self, name, state):
        self.states[name] = state
    
    def transition(self,name):
        if(name in self.states):
        # If in the future we want to add additional things when entering and leaving states, we can add them here.
        # Can only be done if they have leave and enter functions.
            # if(self.current_state):
                # if hasattr(self.current_state, 'leave'):
                #     self.current_state.leave()
            self.current_state = self.states[name]
            if hasattr(self.current_state, 'enter'):
                self.current_state.enter()
        return

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
        self.window_should_close = True