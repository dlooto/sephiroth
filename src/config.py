

import pytoml as toml





class Config:

    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'rb') as file:
            self.config = toml.load(file)


    def reload(self):
        pass




