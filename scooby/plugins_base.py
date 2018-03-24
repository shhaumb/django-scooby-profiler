class Plugin(object):
    def __init__(self, name):
        self.name = name
        self.instrumented = False

    def should_be_used(self):
        return True

    def is_instrumented(self):
        return self.instrumented

    def instrument(self):
        self.instrumented = True
