
from pygments.lexers.python import Python3Lexer

from pygments.token import Name, Keyword

class NANDLexer(Python3Lexer):
    name = 'NAND'
    aliases = ['nand']

    EXTRA_KEYWORDS = ['NAND', 'X', 'Y','Xvalid','Yvalid','loop','i']

    def get_tokens_unprocessed(self, text):
        for index, token, value in Python3Lexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
