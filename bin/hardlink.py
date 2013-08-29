"""Search through directories and hardlink together identical files."""

import os
import sys
import stat
import tempfile
import binascii
import popen2

newHardlinkedFiles = 0
newHardlinkedBytes = 0

class inode:
    def __init__(self, path, redirect):
        self.path = path
        self.redirect = redirect

def walk_list(dirs):
    # maps inumbers to inode objects.
    inodes = {}

    # maps file size to a list of inode objects with that size.
    hashes = {}

    for d in dirs:
        walk(d, inodes, hashes)

def walk(dir, inodes, hashes):
    global newHardlinkedFiles, newHardlinkedBytes

    for root, dirs, files in os.walk(dir):
        for f in files:
            # IIRC os.path.join is slow because it calls normpath.
            path = root + '/' + f
            st = os.lstat(path)
            # If this isn't a regular file, or if it's too small, skip it.
            if not stat.S_ISREG(st.st_mode) or st.st_size < 4092:
                continue
            try:
                ino = inodes[st.st_ino]
                was_new = False
            except KeyError:
                ino = handle_unknown_inode(path, st, inodes, hashes)
                was_new = True

            # We either decided to keep the inode (because its contents are
            # different from anything we'd seen before) or hardlink it to
            # something else.
            if ino.redirect:
                link(path, ino.redirect)
                if was_new:
                    newHardlinkedFiles += 1
                    newHardlinkedBytes += st.st_size

def handle_unknown_inode(path, st, inodes, hashes):
    # We've never seen this inode before.  Compare it to all other inodes with
    # the same hash.  If we find another inode whose contents match this one's,
    # then link them together.  Otherwise, declare that this is a genuinely
    # unique inode.
    fd = open(path, 'r')
    block = fd.read(4092)
    crc = binascii.crc32(block)

    def contents_equal(other_path):
        other_fd = open(other_path, 'r')
        other_initial_block = other_fd.read(4092)
        if other_initial_block != block:
            return False
        fd.seek(4092) # reset fd
        while True:
            b1 = fd.read(4092)
            b2 = other_fd.read(4092)
            if b1 != b2:
                return False
            if not len(b1):
                return True

    redirect = None
    if crc not in hashes:
        hashes[crc] = []
    for other in hashes[crc]:
        if contents_equal(other.path):
            redirect = other.path

    ino = inode(path, redirect)
    inodes[st.st_ino] = ino
    if not redirect:
        hashes[crc].append(ino)
    return ino

def diff(path1, path2):
    proc = popen2.Popen3(['diff', '-q', path1, path2])
    if proc.wait() != 0:
        print "%s does not match %s"
        print "Exiting..."
        sys.exit(1)

def link(link_name, link_target):
    # Make link_name a hardlink to link_target.
    print "Linking %s to %s" % (link_name, link_target)
    #diff(link_name, link_target)
    for i in range(0, 10):
        temp = 'hardlink-%d' % i
        try:
            os.link(link_target, temp)
            break
        except:
            pass

    os.rename(temp, link_name)

def link_duplicates(files, size):
    """Takes a list of files which all have the same size and tries to hardlink
    together the ones which are duplicates."""
    global newHardlinkedBytes, newHardlinkedFiles

    if len(files) == 1:
        return

    # Maps file paths to a chunk at the beginning.
    blocks = {}
    for f in files:
        file_obj = open(f, 'r')
        blocks[f] = file_obj.read(1024 * 32)
        file_obj.close()

    files1 = files[:]
    for f1 in files1:
        try:
            files.remove(f1)
        except ValueError:
            # The path was removed earlier; skip it.
            continue
        files2 = files[:]
        for f2 in files2:
            if contents_equal(f1, f2, blocks, size):
                link(f1, f2)
                files.remove(f2)
                newHardlinkedFiles += 1
                newHardlinkedBytes += size

def main(dirs):
    walk_list(dirs)
    print "Hardlinked an additional %d files, %0.0fmb" % \
          (newHardlinkedFiles, newHardlinkedBytes / (1024 * 1024.0))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Specify at least one directory."
        sys.exit(1)
    main(sys.argv[1:])
    for 
