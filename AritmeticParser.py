

class AritmeticParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current_token = None


    def parse(self):
        print('parsing aritmetic')


    def parea(self, T):
        if self.current_token == T:
            self.current_token = self.next_token()


    def next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return 404
