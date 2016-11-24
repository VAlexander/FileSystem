import os
import sys
from stat import S_ISDIR, S_ISREG
import contextlib

def walktree(top, callback, output):

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        if os.path.exists(pathname):
            if pathname.find('$') < 0:
                mode = os.stat(pathname).st_mode
                if S_ISDIR(mode):
                    walktree(pathname, callback, output)
                elif S_ISREG(mode):
                    callback(pathname, output)
                else:
                    print 'Skipping %s' % pathname


def getFileSize(file, output):
    try:
        size = os.stat(file).st_size / 1024 / 1024
        if size >= 100:
            output.writeline('%s \t %d\n' % (file, size))
    except:
        print "Skipping {0} due to error: {1}".format(file, sys.exc_info()[0])

if __name__ == '__main__':
    with open('results.txt', 'w') as results:
        if os.path.exists('results.txt'):
            if os.path.getsize('results.txt') > 0:
                results.truncate()

        walktree('c:\\', getFileSize, results)