
class Mangler:
    def __init__(self):
        # A list of names already taken. Global variables, global functions, keywords, etc.
        self.taken_names = []

    def add_taken_name(self, name):
        self.taken_names.append(name)

    # Creates a new name not already in self.taken_names based on a suggestion, and with added information
    def create_name(self, suggested="", scope_names=None):
        pass
