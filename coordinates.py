class coordinates:
    def __init__(self):
        self.origin = [0, -8, 0]
        self.home = [170, 2627]
        self.last = [249, 2630]
        self.touch = 2
        
        self.keyboard = {
            "enter": [62, -12],
            "shift":[4, -22],
            "transform":[4,-12],
            ".":[54, -12],
            "amount_enter":[59,-36]
        }
        self.alphabet = {
            "a": [7, -31],
            "b": [40, -21],
            "c": [26, -21],
            "d": [17, -31],
            "e": [17, -41],
            "f": [26, -31],
            "g": [33, -31],
            "h": [39, -31],
            "i": [50, -41],
            "j": [46, -31],
            "k": [53, -31],
            "l": [59, -31],
            "m": [53, -21],
            "n": [46, -21],
            "o": [57, -41],
            "p": [63, -41],
            "q": [3, -41],
            "r": [23, -41],
            "s": [12, -31],
            "t": [30, -41],
            "u": [43, -41],
            "v": [33, -21],
            "w": [10, -41],
            "x": [20, -21],
            "y": [37, -41],
            "z": [13, -21]
        }
        self.capital = {
            "A": [7, -31],
            "B": [40, -21],
            "C": [26, -21],
            "D": [17, -31],
            "E": [17, -41],
            "F": [26, -31],
            "G": [33, -31],
            "H": [39, -31],
            "I": [50, -41],
            "J": [46, -31],
            "K": [53, -31],
            "L": [59, -31],
            "M": [53, -21],
            "N": [46, -21],
            "O": [57, -41],
            "P": [63, -41],
            "Q": [3, -41],
            "R": [23, -41],
            "S": [12, -31],
            "T": [30, -41],
            "U": [43, -41],
            "V": [33, -21],
            "W": [10, -41],
            "X": [20, -21],
            "Y": [37, -41],
            "Z": [13, -21]
        }
        self.number = {
            "1": [3, -50],
            "2": [10, -50],
            "3": [17, -50],
            "4": [23, -50],
            "5": [30, -50],
            "6": [37, -50],
            "7": [43, -50],
            "8": [50, -50],
            "9": [57, -50],
            "0": [64, -50]
        }
        self.lock = {
            "1": [15, -73],
            "2": [33, -73],
            "3": [50, -73],
            "4": [15, -58],
            "5": [33, -58],
            "6": [50, -58],
            "7": [16, -43],
            "8": [33, -43],
            "9": [50, -43],
            "0": [33, -28]
        }
        self.amount = {
            "1": [9, -47],
            "2": [26, -47],
            "3": [41, -47],
            "4": [9, -34],
            "5": [26, -34],
            "6": [41, -34],
            "7": [9, -23],
            "8": [26, -23],
            "9": [41, -23],
            "0": [26, -13]
        }
        self.sign = {
            "&": [44,-31],
            "%": [30,-31],
            "#": [17,-31],
            "@": [11,-31]
        }
    def get_home(self):
        return self.home

    def get_last(self):
        return self.last

    def get_keyboard(self, key):
        return self.keyboard.get(key, None)
    
    def get_alphabet(self, letter):
        return self.alphabet.get(letter, None)
    
    def get_capital(self, letter):
        return self.capital.get(letter, None)
    
    def get_number(self, number):
        return self.number.get(number, None)
    
    def get_lock(self, number):
        return self.lock.get(number, None)
    
    def get_sign(self, x):
        return self.sign.get(x, None)

    def get_amount(self, x):
        return self.amount.get(x, None)
