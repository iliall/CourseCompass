
import re
from enum import Enum
from test import Node, NodeType
from api import API

TERM = 1245
SUBJECTS = API.subjects()
CODES = [] # R A C D L B J E M
for subject in SUBJECTS:
    CODES += API.codes({'term': 1245, 'subject': subject})

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
    
class clean:
    @staticmethod
    def full_clean(prereq_string: str) -> str:
        return clean.remove_prereq(clean.remove_coreq(clean.remove_antireq(prereq_string)))
    
    def remove_antireq(prereq_string: str) -> str:
        return re.sub(r"Antireq:.*", "", prereq_string).strip()

    def remove_coreq(prereq_string: str) -> str:
        return re.sub(r"Coreq:.*", "", prereq_string).strip()
    
    def remove_prereq(prereq_string: str) -> str:
        return re.sub(r"^Prereq: ", "", prereq_string)

class tokenize:
    def tokenize(prereq_string: str) -> list[Token]:
        tokens = []
        current_token = ''
        for char in prereq_string:
            if char == '(':
                if current_token:
                    if current_token in CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                        current_token = ''
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                        current_token = ""
                tokens.append(Token(char, TokenType.LPAR))
            elif char == ')':
                if current_token:
                    if current_token in CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                        current_token = ''
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                        current_token = ''
                tokens.append(Token(char, TokenType.RPAR))
            elif char == '/':
                if current_token:
                    if current_token in CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                        current_token = ''
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                        current_token = ''
                tokens.append(Token(char, TokenType.SLASH))
            elif char == ',':
                if current_token:
                    if current_token in CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                        current_token = ''
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                        current_token = ''
                tokens.append(Token(char, TokenType.COMMA))
            elif char == ' ':
                if current_token:
                    if current_token == 'One':
                        current_token += ' '
                    elif current_token in CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                        current_token = ''
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                        current_token = ''
            elif char == ';':
                if current_token:
                    if current_token in CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                        current_token = ''
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                        current_token = ''

                tokens.append(Token(char, TokenType.SEMICOLON))
            else:
                current_token += char
                if current_token in SUBJECTS:
                    tokens.append(Token(current_token, TokenType.SUBJECT))
                    current_token = ''
                elif current_token == 'or':
                    tokens.append(Token(current_token, TokenType.OR))
                    current_token = ''
                elif current_token == 'and':
                    tokens.append(Token(current_token, TokenType.AND))
                    current_token = ''
                elif current_token == 'One of':
                    tokens.append(Token(current_token, TokenType.ONEOF))
                    current_token = ''
        if current_token:
            if current_token in CODES:
                tokens.append(Token(current_token, TokenType.CODE))
            else:
                tokens.append(Token(current_token, TokenType.NONE))

        return tokens
    
class parse:
    def parse(tokens: list[Token]) -> Node:
        return Node()

prereq_string = API.requirementsDescription({'term': 1245, 'subject': 'CS', 'catalog-number': 485})
print(prereq_string)

tokenization = tokenize.tokenize(clean.full_clean(prereq_string))

for token in tokenization:
    print(token.token + " " + str(token.type))