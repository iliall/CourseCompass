from CourseCompass.api.prereq.init import TokenType, Token

class Tokenize:
    def __init__(self, codes: list[str], subjects: list[str]) -> None:
        self.CODES = codes
        self.SUBJECTS = subjects

    def tokenize(self, prereq_string: str) -> list[Token]:
        tokens = []
        current_token = ''
        
        for char in prereq_string:

            print(current_token)
            if char == '(':
                if current_token:
                    if current_token in self.CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                    current_token = ''
                tokens.append(Token(char, TokenType.LPAR))
                continue

            elif char == ')':
                if current_token:
                    if current_token in self.CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                    current_token = ''
                tokens.append(Token(char, TokenType.RPAR))
                continue

            elif char == '/':
                if current_token:
                    if current_token in self.CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                    current_token = ''
                tokens.append(Token(char, TokenType.SLASH))
                continue

            elif char == ',':
                if current_token:
                    if current_token in self.CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                    current_token = ''
                tokens.append(Token(char, TokenType.COMMA))
                continue

            elif char == ' ':
                if current_token:
                    if current_token == 'One' or current_token == 'one':
                        current_token += ' '
                        continue
                    elif current_token in self.CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                    current_token = ''
                continue
                

            elif char == ';':
                if current_token:
                    if current_token in self.CODES:
                        tokens.append(Token(current_token, TokenType.CODE))
                    else:
                        tokens.append(Token(current_token, TokenType.NONE))
                    current_token = ''
                tokens.append(Token(char, TokenType.SEMICOLON))
                continue

            else:
                current_token += char
                if current_token in self.SUBJECTS:
                    tokens.append(Token(current_token, TokenType.SUBJECT))
                    current_token = ''
                elif current_token == 'or':
                    tokens.append(Token(current_token, TokenType.OR))
                    current_token = ''
                elif current_token == 'and':
                    tokens.append(Token(current_token, TokenType.AND))
                    current_token = ''
                elif current_token == 'One of' or current_token == 'one of':
                    tokens.append(Token(current_token, TokenType.ONEOF))
                    current_token = ''

        if current_token:
            if current_token in self.CODES:
                tokens.append(Token(current_token, TokenType.CODE))
            else:
                tokens.append(Token(current_token, TokenType.NONE))

        return tokens

    def clean_None(self, tokens: list[Token]) -> list[Token]:
        return [token for token in tokens if token.type != TokenType.NONE]
