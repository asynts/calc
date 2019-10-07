import re

class Lexer:
    def __init__(self, input_):
        self._input = input_
        self._cursor = 0

    @property
    def _ahead(self):
        return self._input[self._cursor:]

    def _must(self, condition):
        if not condition:
            raise AssertionError('assertion failed')
    
    def _match(self, string):
        if self._ahead.startswith(string):
            self._cursor += len(string)
            return True
        return False

    _re_integer = re.compile('^[0-9]+')
    def _lex_integer(self) -> bool:
        match = self._re_integer.match(self._ahead)
        if match:
            self._cursor += len(match.group(0))
            print('integer:', match.group(0))
        return bool(match)

    _re_identifier = re.compile('^[_a-z0-9]+')
    def _lex_identifier(self) -> bool:
        match = self._re_identifier.match(self._ahead)
        if match:
            self._cursor += len(match.group(0))
            print('identifier:', match.group(0))
        return bool(match)

    def _lex_arguments(self) -> bool:
        if self._lex_expression():
            while self._match(','):
                self._must(self._lex_expression)
            return True
        return False

    def _lex_operand(self) -> bool:
        if self._match('('):
            self._must(self._lex_expression())
            self._must(self._match(')'))
            return True
        
        if self._lex_integer():
            return True
        
        if self._lex_identifier():
            if self._match('('):
                self._lex_arguments()
                self._must(self._match(')'))
                
            return True

        return False

    def _lex_prefix(self):
        for op in ['++', '--', '-']:
            if self._match(op):
                print('prefix:', op)
                return True
        return False

    def _lex_infix(self):
        for op in ['+', '-', '*', '/']:
            if self._match(op):
                print('infix:', op)
                return True
        return False

    def _lex_postfix(self):
        for op in ['++', '--']:
            if self._match(op):
                print('postfix:', op)
                return True
        return False
    
    def _lex_term(self) -> bool:
        print('backup')

        while self._lex_prefix():
            pass
        
        if not self._lex_operand():
            print('restore')
            return False
        
        print('apply')

        while self._lex_postfix():
            pass

        return True

    def _lex_expression(self) -> bool:
        if self._lex_term():
            while self._lex_infix():
                self._must(self._lex_term())
            
            return True
        return False

lexer = Lexer('(20+1)*2')
print(lexer._lex_expression())
