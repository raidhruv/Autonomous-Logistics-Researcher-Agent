class StateManager:
    def __init__(self):
        self.state = "idle"

    def set(self, state):
        print(f"[STATE] → {state}")
        self.state = state

    def get(self):
        return self.state


state_manager = StateManager()