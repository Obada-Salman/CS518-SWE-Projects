class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.last_level = None

    def add_state(self, name, state):
        self.states[name] = state

    def set_state(self, name):
        if name in self.states:
            self.current_state = self.states[name]
            if hasattr(self.current_state, "enter"):
                self.current_state.enter()

    def update(self, events):
        if self.current_state:
            self.current_state.update(events)

    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)