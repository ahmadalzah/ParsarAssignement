import ASTNodeDefs as AST

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position] if self.code else None
        self.tokens = []

    # Move to the next position in the code.
    def advance(self):
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    # Skip whitespaces.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Tokenize an identifier or keyword.
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        # Check for keywords
        if result == 'if':
            return ('IF', 'if')
        elif result == 'else':
            return ('ELSE', 'else')
        elif result == 'while':
            return ('WHILE', 'while')
        else:
            return ('IDENTIFIER', result)

    # Tokenize a number.
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', int(result))

    def token(self):
        if self.current_char is None:
            return ('EOF', None)
        if self.current_char.isspace():
            self.skip_whitespace()
            return self.token()
        if self.current_char.isalpha() or self.current_char == '_':
            return self.identifier()
        if self.current_char.isdigit():
            return self.number()
        if self.current_char == '+':
            self.advance()
            return ('PLUS', '+')
        if self.current_char == '-':
            self.advance()
            return ('MINUS', '-')
        if self.current_char == '*':
            self.advance()
            return ('MULTIPLY', '*')
        if self.current_char == '/':
            self.advance()
            return ('DIVIDE', '/')
        if self.current_char == '=':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return ('EQ', '==')
            else:
                return ('EQUALS', '=')
        if self.current_char == '<':
            self.advance()
            return ('LESS', '<')
        if self.current_char == '>':
            self.advance()
            return ('GREATER', '>')
        if self.current_char == '!':
            self.advance()
            if self.current_char == '=':
                self.advance()
                return ('NEQ', '!=')
            else:
                raise ValueError(f"Illegal character '!' at position {self.position}")
        if self.current_char == ',':
            self.advance()
            return ('COMMA', ',')
        if self.current_char == ':':
            self.advance()
            return ('COLON', ':')
        if self.current_char == '(':
            self.advance()
            return ('LPAREN', '(')
        if self.current_char == ')':
            self.advance()
            return ('RPAREN', ')')
        raise ValueError(f"Illegal character '{self.current_char}' at position {self.position}")

    # Collect all tokens into a list.
    def tokenize(self):
        while self.current_char is not None:
            token = self.token()
            if token[0] != 'EOF':
                self.tokens.append(token)
        self.tokens.append(('EOF', None))
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)  # Start with the first token

    def advance(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = ('EOF', None)

    def expect(self, token_type):
        if self.current_token[0] != token_type:
            raise ValueError(f"Expected {token_type} but got {self.current_token[0]}")

    def peek(self):
        if self.tokens:
            return self.tokens[0][0]
        else:
            return None

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
        return statements

    def statement(self):
        if self.current_token[0] == 'IDENTIFIER':
            next_token_type = self.peek()
            if next_token_type == 'EQUALS':
                return self.assign_stmt()
            elif next_token_type == 'LPAREN':
                return self.function_call()
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            self.advance()
            return self.if_stmt()
        elif self.current_token[0] == 'WHILE':
            self.advance()
            return self.while_stmt()
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")

    def assign_stmt(self):
        identifier = ('IDENTIFIER', self.current_token[1])
        self.advance()
        self.expect('EQUALS')
        self.advance()
        expression = self.expression()
        return AST.Assignment(identifier, expression)

    def if_stmt(self):
        condition = self.boolean_expression()
        self.expect('COLON')
        self.advance()
        then_block = self.block()
        else_block = None
        if self.current_token[0] == 'ELSE':
            self.advance()
            self.expect('COLON')
            self.advance()
            else_block = self.block()
        return AST.IfStatement(condition, then_block, else_block)

    def while_stmt(self):
        condition = self.boolean_expression()
        self.expect('COLON')
        self.advance()
        block = self.block()
        return AST.WhileStatement(condition, block)

    def block(self):
        statements = []
        while self.current_token[0] not in ['EOF', 'ELSE', 'ENDIF']:
            statements.append(self.statement())
        return AST.Block(statements)

    def expression(self):
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token
            self.advance()
            right = self.term()
            left = AST.BinaryOperation(left, op, right)
        return left

    def boolean_expression(self):
        left = self.expression()
        if self.current_token[0] in ['EQ', 'NEQ', 'LESS', 'GREATER']:
            op = self.current_token
            self.advance()
            right = self.expression()
            return AST.BooleanExpression(left, op, right)
        else:
            # If no boolean operator, return the left expression as is.
            return left

    def term(self):
        left = self.factor()
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token
            self.advance()
            right = self.factor()
            left = AST.BinaryOperation(left, op, right)
        return left

    def factor(self):
        if self.current_token[0] == 'NUMBER':
            node = self.current_token
            self.advance()
            return node
        elif self.current_token[0] == 'IDENTIFIER':
            node = self.current_token
            self.advance()
            return node
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            self.advance()
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        function_name = ('IDENTIFIER', self.current_token[1])
        self.advance()
        self.expect('LPAREN')
        self.advance()
        args = self.arg_list()
        self.expect('RPAREN')
        self.advance()
        return AST.FunctionCall(function_name, args)

    def arg_list(self):
        args = []
        if self.current_token[0] != 'RPAREN':
            args.append(self.expression())
            while self.current_token[0] == 'COMMA':
                self.advance()
                args.append(self.expression())
        return args