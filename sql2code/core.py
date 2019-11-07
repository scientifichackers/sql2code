from typing import NamedTuple, List

from sly import Lexer, Parser


class SQLFunctionsLexer(Lexer):
    literals = {'(', ')', '{', '}', ',', ';'}
    tokens = {VAR, WORD, OTHER}
    ignore = ' \t'
    ignore_comment = r'\-\-.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    VAR = r'(\$\w+|\'\$\w+\')'
    WORD = r'\w+'
    OTHER = r'[^\n\(\)\{\}\,\;\$]+'


class QueryVar(NamedTuple):
    name: str
    is_quoted: bool


class SQLFunction(NamedTuple):
    name: str
    params: List[str]
    body: List[List[str]]

    def __repr__(self):
        return 'Function(\n\tname: %r\n\tparams: %r\n\tbody: [%s\n\t]\n)' % (
            self.name,
            self.params,
            ''.join(f'\n\t\t{stmt!r},' for stmt in self.body),
        )


class SQLFunctionsParser(Parser):
    tokens = SQLFunctionsLexer.tokens
    literals = SQLFunctionsLexer.literals

    # root

    @_('', 'function', 'function root')
    def root(self, p):
        root = []
        try:
            root.append(p.function)
        except KeyError:
            pass
        try:
            root += p.root
        except KeyError:
            pass
        return root

    # SQL fragment

    @_('WORD', 'OTHER', '")"', '"("', '","', 'fragment fragment')
    def fragment(self, p):
        return ' '.join(p)

    # SQL statement (fragment + variables)

    @_('VAR')
    def statement(self, p):
        return [
            QueryVar(
                p.VAR.strip("'").strip('$'),
                p.VAR.startswith("'") and p.VAR.endswith("'"),
            )
        ]

    @_('fragment')
    def statement(self, p):
        return [p.fragment]

    @_('statement statement')
    def statement(self, p):
        total = []
        for statement in p:
            if isinstance(statement, list):
                total += statement
            else:
                total.append(statement)
        return total

    # SQL statements

    @_('statement ";"', 'statement ";" body')
    def body(self, p):
        body = [p.statement]
        try:
            body += p.body
        except KeyError:
            pass
        return body

    # function

    @_('WORD "(" params ")" "{" body "}"', 'WORD "(" ")" "{" body "}"')
    def function(self, p):
        try:
            params = p.params
        except KeyError:
            params = []
        return SQLFunction(p.WORD, params, p.body)

    # params

    @_('WORD', 'WORD ","', 'WORD "," params')
    def params(self, p):
        params = [p.WORD]
        try:
            params += p.params
        except KeyError:
            pass
        return params
