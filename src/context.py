


class Context:

    def __init__(self):
        self.return_value = None

    def set_return_value(self, return_value):
        self.return_value = return_value

    def __str__(self):
        
        return "Context: %s %s" % (id(self), str(self.return_value))