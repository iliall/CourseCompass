from enum import Enum

class TokenType(Enum):
    NONE = 0
    SUBJECT = 1 # In SUBJECTS
    CODE = 2 # In CODES
    COMMA = 3 # S,S (Could be AND or OR)
    SLASH = 4 # S/S (Equivalent to OR)
    LPAR = 5 # (S
    RPAR = 6 # S)
    OR = 7 # S or S
    AND = 8 # S and S
    ONEOF = 9 # One of S (Equivalent to OR)
    SEMICOLON = 10 # S;S (Equivalent to AND)

class Token:
    def __init__(self, 
                 token: str, 
                 type: TokenType):
        self.token = token
        self.type = type