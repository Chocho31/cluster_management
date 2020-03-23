class Plugin:
    def __init__(self, *args, **kwargs):
        print("Plugin one init: ", args, kwargs)

    def execute(self, a, b):
        return a + b
