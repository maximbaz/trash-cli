# Copyright (C) 2007-2011 Andrea Francia Trivolzio(PV) Italy

version = '0.23.9.23'


def debug_print(msg):
    import os
    import sys
    if os.environ.get('TRASHCLI_DEBUG')  == '1':
        print(msg, file=sys.stderr)

