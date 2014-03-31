#!/usr/bin/env python

import os
import optparse
import itertools
import stat
import sha

def os_walk_files_iter(dirs):
    for root, dirs, files in itertools.chain(*[os.walk(d) for d in dirs]):
        for f in files:
            yield root + '/' + f

def size_hasher(paths_iter):
    inodes = set()
    for path in paths_iter:
        st = os.lstat(path)
        # Skip this file if it's not a regular file or if it's too small.
        if not stat.S_ISREG(st.st_mode) or st.st_size < 4096:
            continue
        # Skip this file if we've already seen its inode.
        if st.st_ino in inodes:
            continue
        inodes.add(st.st_ino)

        yield (path, st.st_size)

def sm_hasher(paths_iter):
    # Sample some blocks from the files.
    block_size = 8 * 1024
    for path in paths_iter:
        size = os.lstat(path).st_size
        h = sha.new()
        f = open(path, 'rb')
        h.update(f.read(block_size))
        f.close()
        yield (path, h.digest())

def full_hasher(paths_iter):
    block_size = 8 * 1024
    for path in paths_iter:
        f = open(path, 'rb')
        h = sha.new()
        while True:
            block = f.read(block_size)
            if not block:
                break
            h.update(block)
        f.close()
        yield (path, h.digest())

def collect_hashes(paths_iter, hash_iter_fn):
    '''Yield groups of at least two paths which hash to the same value,
    according to hash_iter_fn.'''

    num_hashes = 0
    hashes = {}
    for (path, hash) in hash_iter_fn(paths_iter):
        num_hashes += 1
        if hash not in hashes:
            hashes[hash] = []
        hashes[hash].append(path)

    print '%d invocations of %s' % (num_hashes, hash_iter_fn)
    for paths in hashes.itervalues():
        if not isinstance(paths, basestring) and len(paths) > 1:
            yield paths

def hardlink_all(options, dirs):
    for same_sizes in collect_hashes(os_walk_files_iter(dirs), size_hasher):
        for same_sm_hashes in collect_hashes(same_sizes, sm_hasher):
            for same_full_hashes in collect_hashes(same_sm_hashes, full_hasher):
                print 'Identical: %s' % str(same_full_hashes)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='%prog [options] DIR [DIR ...]')
    parser.add_option('-n', '--dry-run', action='store_true', dest='dry_run', default=False)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose')

    (options, dirs) = parser.parse_args()
    if not dirs:
        parser.error('Specify at least one directory.')
    hardlink_all(options, dirs)
