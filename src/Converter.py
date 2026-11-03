import math

class Converter:
    @staticmethod
    def do(x: float) -> int:
        if (x >= 100.7):
            x = 1000
        elif (x > 0 and x < 100.7):
            x = int(x)
        elif (x == 0.0):
            raise ValueError
        elif (x >= -30.4 and x < 0):
            x = int(x) - 5
        elif (x <= -30.5):
            x = -2000
        else:
            raise ValueError
        return x