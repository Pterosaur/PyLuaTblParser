class NonePattern(Exception):
    def __init__(self, arg):
        self.__arg = arg
    def __str__(self):
        return self.__arg