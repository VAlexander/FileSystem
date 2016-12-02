import os
import sys
from stat import S_ISDIR, S_ISREG
import errno
# import contextlib

def walktree(top, callback, output):
    try:
        pathname = top
        for f in os.listdir(pathname):
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
    except IOError as e:
        if e.errno == errno.EACCES:
            print "{0}: error code is {1}".format(pathname, e.errno)
        else:
            raise
    except WindowsError as e:
        if e.errno == errno.EACCES:
            print "{0}: error code is {1}".format(pathname, e.errno)
        elif e.errno in (errno.ESRCH, errno.ENOENT):
            print "Something wrong with {0}: {1}".format(pathname, e.strerror)
        else:
            raise
    except Exception as e:
        print "{0}: error code is {1}".format(pathname, e.message)


def getFileSize(file, output):
    try:
        size = os.path.getsize(file) / 1024 / 1024
        if size >= 100:
            output.write('{0} \t {1}\n'.format(file, size))
    except Exception as e:
        print "Skipping {0} due to error: {1}".format(file, sys.exc_info()[0])

if __name__ == '__main__':
    with open('results.txt', 'w') as results:
        if os.path.exists('results.txt'):
            if os.path.getsize('results.txt') > 0:
                results.truncate()

        walktree('C:\\', getFileSize, results)