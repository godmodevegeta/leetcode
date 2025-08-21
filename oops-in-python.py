class Human:
    species = "H. Sapien"

    def __init__(self, name):
        self.name = name
        self._age = 0

    def say(self, msg):
        print("Hi, my name is {name} and {msg}".format(name = self.name, msg = msg))
    
    def sing(self):
        print("Hi there!")
    