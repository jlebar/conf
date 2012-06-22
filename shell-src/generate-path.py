#!/usr/bin/env python

import os

mypath = ['%s/bin' % os.environ['HOME'],
          '%s/bin' % os.environ['CONFDIR'],
          '%s/bin/moz' % os.environ['CONFDIR'],
          '%s/bin/android-tools' % os.environ['CONFDIR'],
          '%s/bin/android-platform-tools' % os.environ['CONFDIR'],
          '%s/code/moz/git-tools' % os.environ['HOME']]

if __name__ == '__main__':
    if os.path.exists('/opt/local/bin'):
        mypath.insert(0, '/opt/local/bin')

    path = os.environ['PATH']

    # Set newpathlist to path, without duplicates.
    newpathlist = []
    for p in path.split(':'):
        if p not in newpathlist:
            newpathlist.append(p)

    for p in mypath:
        if p not in newpathlist:
            # Add p to the *front* of newpathlist.
            newpathlist = [p] + newpathlist

    print ':'.join(newpathlist)
