from setuptools import setup

setup(
    name='pygments-rosi',
    version='0.1.0',
    py_modules=['rosi_lexer'],
    entry_points={
        'pygments.lexers': [
            'rosi = rosi_lexer:RosiLexer',
        ],
    },
)
