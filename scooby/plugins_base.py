class Plugin(object):
    def __init__(self, name):
        self.name = name
        self.instrumented = False

    def is_instrumented(self):
        return self.instrumented

    def instrument(self):
        self.instrumented = True
