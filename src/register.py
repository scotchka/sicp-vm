class Register:
    def __init__(self):
        self._contents = None

    def get_contents(self):
        return self._contents

    def set_contents(self, contents):
        self._contents = contents
