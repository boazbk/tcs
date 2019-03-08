#from pygments.lexers.asm import CppLexer
from pygments.lexers.compiled import CppLexer
from pygments.token import Name, Keyword

class MDCppLexer(CppLexer):
    name = 'MDCpp'
    aliases = ['mdcpp']

    EXTRA_KEYWORDS = ['Atom', 'System', 'vec3']

    def get_tokens_unprocessed(self, text):
        for index, token, value in CppLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.EXTRA_KEYWORDS:
                yield index, Keyword, value
            else:
                yield index, token, value
