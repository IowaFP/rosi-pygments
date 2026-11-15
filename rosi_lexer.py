# -----------------------------------------------------------------------------

#! /usr/bin/env python
import argparse
import sys
import pygments.cmdline as _cmdline
import pygments.lexer as _lexer
import pygments.token as _token

import re

from pygments.lexer import Lexer, RegexLexer, bygroups, do_insertions, \
    default, include, inherit
from pygments.lexers.haskell import HaskellLexer
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Generic
from pygments import unistring as uni

__all__ = ['RosiLexer']


line_re = re.compile('.*?\n')


class RosiLexer(RegexLexer):
  """
  Lexer for the Rosi language.
  """

  name = 'Rosi'
  url = ''
  aliases = ['rosi']
  filenames = ['*.ro']
  mimetypes = ['text/x-rosi']

  flags = re.MULTILINE | re.UNICODE

  reserved = ('forall', 'Pi', 'Sigma', 'Mu',
              'Record', 'Variant', 'row',
              'let', 'newtype', 'type', 'in', 'out', 'fix', 'prj', 'inj', 'ana', 'syn', 'Π', 'Σ', 'μ', 'L', '⋆')
  ascii = ('NUL', 'SOH', '[SE]TX', 'EOT', 'ENQ', 'ACK',
           'BEL', 'BS', 'HT', 'LF', 'VT', 'FF', 'CR', 'S[OI]', 'DLE',
           'DC[1-4]', 'NAK', 'SYN', 'ETB', 'CAN',
           'EM', 'SUB', 'ESC', '[FGRU]S', 'SP', 'DEL')

  tokens = {
      'root': [
          # Whitespace:
          (r'\s+', Text),
          # (r'--\s*|.*$', Comment.Doc),
          (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
          (r'\{-', Comment.Multiline, 'comment'),
          (r'\'(\w|\n)+', Number.Integer),
          # Lexemes:
          #  Identifiers
          (r'\bimport\b', Keyword.Reserved, 'import'),
          (r'\bmodule\b', Keyword.Reserved, 'module'),
          (r'\berror\b', Name.Exception),
          (r'\b(%s)(?!\')\b' % '|'.join(reserved), Keyword.Reserved),
          (r"'[^\\]'", String.Char),  # this has to come before the TH quote
          (r'^[_' + uni.Ll + r'][\w\']*', Name.Function),
          (r"'?[_" + uni.Ll + r"][\w']*", Name),
          (r"('')?[" + uni.Lu + r"][\w\']*", Keyword.Type),
          (r"(')[" + uni.Lu + r"][\w\']*", Keyword.Type),
          (r"(')\[[^\]]*\]", Keyword.Type),  # tuples and lists get special treatment in GHC
          (r"(')\([^)]*\)", Keyword.Type),  # ..
          #  Operators
          (r'\#', Keyword),
          (r'\\(?![:!#$%&*+.\\/<=>?@^|~-]+)', Name.Function),  # lambda operator
          (r'/\\(?![:!#$%&*+.\\/<=>?@^|~-]+)', Name.Function),
          (r'(<-|:|->|=>|=)(?![:!#$%&*+.\\/<=>?@^|~-]+)', Operator.Word),  # specials
          (r':[:!#$%&*+.\\/<=>?@^|~-]*', Keyword.Type),  # Constructor operators
          (r'[:!#$%&*+.\\/<=>?@^|~-μΠΣ⇒→▹∀⊤_∖λΛ＠⋆L]+', Operator),  # Other operators
          #  Numbers
          (r'0[xX]_*[\da-fA-F](_*[\da-fA-F])*_*[pP][+-]?\d(_*\d)*', Number.Float),
          (r'0[xX]_*[\da-fA-F](_*[\da-fA-F])*\.[\da-fA-F](_*[\da-fA-F])*'
           r'(_*[pP][+-]?\d(_*\d)*)?', Number.Float),
          (r'\d(_*\d)*_*[eE][+-]?\d(_*\d)*', Number.Float),
          (r'\d(_*\d)*\.\d(_*\d)*(_*[eE][+-]?\d(_*\d)*)?', Number.Float),
          (r'0[bB]_*[01](_*[01])*', Number.Bin),
          (r'0[oO]_*[0-7](_*[0-7])*', Number.Oct),
          (r'0[xX]_*[\da-fA-F](_*[\da-fA-F])*', Number.Hex),
          (r'\d(_*\d)*', Number.Integer),
          #  Character/String Literals
          (r"'", String.Char, 'character'),
          (r'"', String, 'string'),
          #  Special
          (r'\[\]', Keyword.Type),
          (r'\(\)', Name.Builtin),
          (r'[][(),;`{}]', Punctuation),
      ],
      'import': [
          # Import statements
          (r'\s+', Text),
          (r'"', String, 'string'),
          # after "funclist" state
          (r'\)', Punctuation, '#pop'),
          (r'qualified\b', Keyword),
          # import X as Y
          (r'([' + uni.Lu + r'][\w.]*)(\s+)(as)(\s+)([' + uni.Lu + r'][\w.]*)',
           bygroups(Name.Namespace, Text, Keyword, Text, Name), '#pop'),
          # import X hiding (functions)
          (r'([' + uni.Lu + r'][\w.]*)(\s+)(hiding)(\s+)(\()',
           bygroups(Name.Namespace, Text, Keyword, Text, Punctuation), 'funclist'),
          # import X (functions)
          (r'([' + uni.Lu + r'][\w.]*)(\s+)(\()',
           bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
          # import X
          (r'[\w.]+', Name.Namespace, '#pop'),
      ],
      'labels': [
         # Match labels matching: \B(\'\w+)\b
         (r"(\'\w+)\b", String.Other),
          # Match singletons e.g. #'l, #'x, #'y
          (r"(#\'?\w+)\b", String.Other),
       ],
      'module': [
          (r'\s+', Text),
          (r'([' + uni.Lu + r'][\w.]*)(\s+)(\()',
           bygroups(Name.Namespace, Text, Punctuation), 'funclist'),
          (r'[' + uni.Lu + r'][\w.]*', Name.Namespace, '#pop'),
      ],
      'funclist': [
          (r'\s+', Text),
          (r'[' + uni.Lu + r']\w*', Keyword.Type),
          (r'(_[\w\']+|[' + uni.Ll + r'][\w\']*)', Name.Function),
          (r'--(?![!#$%&*+./<=>?@^|_~:\\]).*?$', Comment.Single),
          (r'\{-', Comment.Multiline, 'comment'),
          (r',', Punctuation),
          (r'[:!#$%&*+.\\/<=>?@^|~-]+', Operator),
          # (HACK, but it makes sense to push two instances, believe me)
          (r'\(', Punctuation, ('funclist', 'funclist')),
          (r'\)', Punctuation, '#pop:2'),
      ],
      # NOTE: the next four states are shared in the AgdaLexer; make sure
      # any change is compatible with Agda as well or copy over and change
      'comment': [
          # Multiline Comments
          (r'[^-{}]+', Comment.Multiline),
          (r'\{-', Comment.Multiline, '#push'),
          (r'-\}', Comment.Multiline, '#pop'),
          (r'[-{}]', Comment.Multiline),
      ],
      'character': [
          # Allows multi-chars, incorrectly.
          (r"[^\\']'", String.Char, '#pop'),
          (r"\\", String.Escape, 'escape'),
          ("'", String.Char, '#pop'),
      ],
      'string': [
          (r'[^\\"]+', String),
          (r"\\", String.Escape, 'escape'),
          ('"', String, '#pop'),
      ],
      'escape': [
          (r'[abfnrtv"\'&\\]', String.Escape, '#pop'),
          (r'\^[][' + uni.Lu + r'@^_]', String.Escape, '#pop'),
          ('|'.join(ascii), String.Escape, '#pop'),
          (r'o[0-7]+', String.Escape, '#pop'),
          (r'x[\da-fA-F]+', String.Escape, '#pop'),
          (r'\d+', String.Escape, '#pop'),
          (r'\s+\\', String.Escape, '#pop'),
      ],
  }
