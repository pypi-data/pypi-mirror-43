from pygments.lexer import RegexLexer, include, bygroups, words
from pygments.token import *


class FinesseLexer(RegexLexer):
    name = 'Finesse'
    aliases = ['finesse', 'kat']
    filenames = ['*.kat']

    def innerstring_rules(ttype):
        return [
            # the old style '%s' % (...) string formatting
            (r'%(\(\w+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?'
             '[hlL]?[E-GXc-giorsux%]', String.Interpol),
            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"%\n]+', ttype),
            (r'[\'"\\]', ttype),
            # unhandled string formatting sign
            (r'%', ttype),
            # newlines are an error (use "nl" state)
        ]

    tokens = {
            'root': [
                (r'[%#].*$', Comment),
                (r'[\s\*]', Text),
                include('components'),
                (r'^\w+', Keyword.Reserved),
                include('numbers'),
                (r'\$\w+', Name.Variable),
                (r'\w+', Text),
                (r'.*?\n', Text)
                ],
            'components': [
                    (r'(^l\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^m[12]?\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^s\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^bs[12]?\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^isol\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^mod\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^lens\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^pd\d*\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^ad\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^shot\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^qshot\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^bp\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^cp\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^guoy\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                    (r'(^beam\s+)(\w+)', bygroups(Keyword.Type, Name.Variable)),
                ],
            'numbers': [
                (r'[+-]?(\d+|\d+\.\d*|\d*\.\d+)[umkMG]?', Number),
                (r'1', Number),
                ],
            }
