"""
Based on the examples provided with fusepy binding created by Giorgos Verigakis
from http://code.google.com/p/fusepy/
"""

import time
from errno import EACCES
from os.path import realpath
from sys import argv, exit
from threading import Lock
"""
threading.Lock()
    A factory function that returns a new primitive lock object. Once a thread has acquired 
    it, subsequent attempts to acquire it block, until it is released; any thread may release it.
http://docs.python.org/library/threading.html?highlight=threading.lock#threading.Lock
"""

import os
from fuse import FUSE, Operations, LoggingMixIn
import MFSCore

class MFSComFUSE(LoggingMixIn, Operations):    
    def __init__(self, root):
        self.root = realpath(root)
        self.rwlock = Lock()

    def __call__(self, op, path, *args):
        return super(MFSComFUSE, self).__call__(op, self.root + path, *args)
    
    def access(self, path, mode):
        """ uses the access() system call to verify permissions over path.
        http://docs.python.org/library/os.html?highlight=os.access#os.access
        """
        if not os.access(path, mode):
            raise OSError(EACCES, '')
    
    chmod = os.chmod
    """http://docs.python.org/library/os.html#os.chmod"""
    
    chown = os.chown
    """#http://docs.python.org/library/os.html#os.chown"""
    
    def create(self, path, mode):
        """ O_CREAT		If the file does not exist, it will be created. 
            O_WRONLY	Write only flag.
        http://docs.python.org/library/os.html#os.open
        """
        return os.open(path, os.O_WRONLY | os.O_CREAT, mode)
    
    def flush(self, path, fd):
        """ Force write of file with file descriptor fd to disk.
        http://docs.python.org/library/os.html?highlight=os.chmod#os.fsync
        """
        return os.fsync(fd)

    def fsync(self, path, datasync, fd):
        return os.fsync(fd)
                
    def getattr(self, path, fd=None):
        """ os.lstat(path) Like stat(), but do not follow symbolic links.
        http://docs.python.org/library/os.html#os.stat
        """
        st = os.lstat(path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
    
    getxattr = None
    """http://manpages.ubuntu.com/manpages/karmic/en/man5/attr.5.html and http://manpages.ubuntu.com/manpages/karmic/en/man1/setfattr.1.html"""
        
    listxattr = None
    """listxattr  retrieves  the  list  of extended attribute names associated with the given path in the filesystem."""
    
    
    def link(self, target, source):
        """link(target, name) Should create the filesystem object name as a hardlink to target.
        http://docs.python.org/library/os.html#os.link
        """
        return os.link(source, target)
    
    mkdir = os.mkdir
    """http://docs.python.org/library/os.html#os.mkdir"""
    
    mknod = os.mknod
    """http://docs.python.org/library/os.html#os.mknod"""
    
    open = os.open
    """http://docs.python.org/library/os.html#os.open"""
        
    def read(self, path, size, offset, fd):
        """ os.lseek(fd, offset, how) Set the current position of file descriptor fd to position offset, 
        modified by how (0 to set the position relative to the beginning of the file). 
        http://docs.python.org/library/os.html#os.lseek
        os.read(fd, n) Read at most n bytes from file descriptor fd.
        http://docs.python.org/library/os.html#os.read
        Code here executes with Lock held.  The lock is guaranteed to be released when the block is left. 
        http://www.python.org/dev/peps/pep-0343/
        """
        with self.rwlock:
            os.lseek(fd, offset, 0)
            return os.read(fd, size)
    
    def readdir(self, path, fd):
        """ os.listdir(path) Return a list containing the names of the entries in the directory given by path. 
        The list is in arbitrary order. It does not include the special entries '.' and 
        '..' even if they are present in the directory.
        http://docs.python.org/library/os.html#os.listdir
        """
        return ['.', '..'] + os.listdir(path)

    readlink = os.readlink
    """http://docs.python.org/library/os.html#os.readlink"""
    
    def release(self, path, fd):
        """http://docs.python.org/library/os.html#os.close"""
        return os.close(fd)
    
    def rename(self, old, new):
        """http://docs.python.org/library/os.html#os.rename"""
        return os.rename(old, self.root + new)
    
    def rmdir(self, path):
        """http://docs.python.org/library/os.html#os.rmdir"""
        MFSCore.rmdir(path)
    
    def statfs(self, path):
        """ The function statvfs() returns information about a mounted file system.
        http://manpages.ubuntu.com/manpages/lucid/en/man2/statvfs.2.html
        http://docs.python.org/library/os.html#os.statvfs
        """
        stv = os.statvfs(path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))
    
    def symlink(self, target, source):
        """http://docs.python.org/library/os.html#os.symlink"""
        return os.symlink(source, target)
    
    def truncate(self, path, length, fd=None):
        """Uses a template for opening a file that ensures the file is closed when 
        the block is left. http://www.python.org/dev/peps/pep-0343/"""
        with open(path, 'r+') as f:
            MFSCore.truncate(path,length,f)
            f.truncate(length)
    
    def unlink(self, path):
		MFSCore.unlink(path)
	
    utimens = os.utime
    """http://docs.python.org/library/os.html#os.utime"""
    
    def write(self, path, data, offset, fd):
        """http://docs.python.org/library/os.html#os.write"""
        with self.rwlock:
            MFSCore.write(path)         
            os.lseek(fd, offset, 0)
            return os.write(fd, data)

def startFS(sourcePath,destPath,fg):
    """Start the filesystem. """
    FUSE(MFSComFUSE(sourcePath),destPath,foreground = fg)
