#!/usr/bin/env python

import os
from os import listdir, environ
from os.path import abspath, normpath, isdir
from itertools import chain

if __name__ == '__main__':
    # Add $HOME/bin, $CONFDIR/bin, and all their subdirectories (including
    # symlinked subdirs) to the path.
    root_dirs = map(abspath,
                    [os.path.join(environ['HOME'], 'bin'),
                     os.path.join(environ['CONFDIR'], 'bin')])

    # TODO: Should also modify the MANPATH.
    # MANPATH="/usr/local/opt/coreutils/libexec/gnuman"

    new_path = filter(os.path.isdir,
                      ['/usr/local/bin', '/usr/local/opt/coreutils/libexec/gnubin'])

    for r in filter(isdir, root_dirs):
        new_path.append(r)
        new_path += filter(isdir, [os.path.join(r, d) for d in listdir(r)])

    new_path += [d for d in environ['PATH'].split(':') if d not in new_path]

    print ':'.join(new_path)
