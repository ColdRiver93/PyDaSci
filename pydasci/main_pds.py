#!/usr/bin/env python

import os

from pydasci.parser_pds import Parser
from pydasci.lexer_pds import Lexer


def main():
    import sys
    begin(sys.argv)


def begin(argv):

    def _bytes(x):
        if bytes == str:
            return bytes(x)
        else:
            return bytes(x, 'utf-8')

    if len(argv) > 1:
        lg = Lexer()
        lexer = lg.get_lexer()
        pg = Parser()
        pg.parse()
        parser = pg.get_parser()   
     
        with open(argv[1], 'r') as f:
            l = lexer.lex(f.read())
            result = parser.parse(l)

    else:
        os.write(1, _bytes("Please provide a filename."))


if __name__ == '__main__':
    main()