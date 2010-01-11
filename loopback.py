#!/usr/bin/env python

import time

"""
Based on the examples provided with fusepy binding created by Giorgos Verigakis
from http://code.google.com/p/fusepy/
"""

"""
errno.EACCES
	Permission denied
http://docs.python.org/library/errno.html?highlight=eacces#errno.EACCES
"""
from errno import EACCES

"""
os.path.realpath(path)
    Return the canonical path of the specified filename, eliminating any symbolic links 
    encountered in the path (if they are supported by the operating system).
http://docs.python.org/library/os.path.html?highlight=realpath#os.path.realpath
"""
from os.path import realpath

from sys import argv, exit

"""
threading.Lock()
    A factory function that returns a new primitive lock object. Once a thread has acquired 
    it, subsequent attempts to acquire it block, until it is released; any thread may release it.
http://docs.python.org/library/threading.html?highlight=threading.lock#threading.Lock
"""
from threading import Lock

import os

from fuse import FUSE, Operations, LoggingMixIn


class Loopback(LoggingMixIn, Operations):    
    def __init__(self, root):
        self.root = realpath(root)
        self.rwlock = Lock()

    def __call__(self, op, path, *args):
        return super(Loopback, self).__call__(op, self.root + path, *args)
    
    """ uses the access() system call to verify permissions over path.
    where mode:
		os.F_OK Value to pass as the mode parameter of access() to test the existence of path.
		os.R_OK Value to include in the mode parameter of access() to test the readability of path.
		os.W_OK Value to include in the mode parameter of access() to test the writability of path.
		os.X_OK Value to include in the mode parameter of access() to determine if path can be executed.
	http://docs.python.org/library/os.html?highlight=os.access#os.access
    """
    def access(self, path, mode):
        if not os.access(path, mode):
            raise OSError(EACCES, '')
    
    #http://docs.python.org/library/os.html#os.chmod
    chmod = os.chmod
    #http://docs.python.org/library/os.html#os.chown
    chown = os.chown
    
    """
    O_CREAT		If the file does not exist, it will be created. 
    O_WRONLY	Write only flag.
    http://docs.python.org/library/os.html#os.open
    """
    def create(self, path, mode):
        return os.open(path, os.O_WRONLY | os.O_CREAT, mode)
    
    """
    Force write of file with filedescriptor fd to disk.
    http://docs.python.org/library/os.html?highlight=os.chmod#os.fsync
    """
    def flush(self, path, fd):
        return os.fsync(fd)

    def fsync(self, path, datasync, fd):
        return os.fsync(fd)
                
    """
    os.lstat(path)
		Like stat(), but do not follow symbolic links.
		Perform a stat() system call on the given path. The return value is an object 
		whose attributes correspond to the members of the stat structure, namely: 
			st_mode (protection bits), 
			st_ino (inode number), 
			st_dev (device), 
			st_nlink (number of hard links), 
			st_uid (user id of owner), 
			st_gid (group id of owner), 
			st_size (size of file, in bytes), 
			st_atime (time of most recent access), 
			st_mtime (time of most recent content modification), 
			st_ctime (platform dependent; time of most recent metadata change on Unix, or the time of creation on Windows)
	http://docs.python.org/library/os.html#os.stat
    """
    def getattr(self, path, fd=None):
        st = os.lstat(path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
            'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))
    
    """
    We do not use extended attributes yet.
    Extended attributes might be used to define versioning policies for a file.
    http://manpages.ubuntu.com/manpages/karmic/en/man5/attr.5.html
    http://manpages.ubuntu.com/manpages/karmic/en/man1/setfattr.1.html
    """
    getxattr = None
    
    """
    listxattr  retrieves  the  list  of extended attribute names associated 
    with the given path in the filesystem.
    """
    listxattr = None
    
    """
    link(target, name)
		Should create the filesystem object name as a hardlink to target.
    http://docs.python.org/library/os.html#os.link
    """
    def link(self, target, source):
        return os.link(source, target)
    
    #http://docs.python.org/library/os.html#os.mkdir
    mkdir = os.mkdir
    #http://docs.python.org/library/os.html#os.mknod
    mknod = os.mknod
    #http://docs.python.org/library/os.html#os.open
    open = os.open
        
    """
    os.lseek(fd, offset, how)
		Set the current position of file descriptor fd to position offset, modified by how: 
		SEEK_SET or 0 to set the position relative to the beginning of the file; 
		SEEK_CUR or 1 to set it relative to the current position; 
		os.SEEK_END or 2 to set it relative to the end of the file.
    http://docs.python.org/library/os.html#os.lseek
    os.read(fd, n)
		Read at most n bytes from file descriptor fd. Return a string containing the bytes 
		read. If the end of the file referred to by fd has been reached, an empty string is 
		returned.
	http://docs.python.org/library/os.html#os.read
    """
    def read(self, path, size, offset, fd):
        with self.rwlock:
			# Code here executes with Lock held.  The lock is guaranteed to be 
			# released when the block is left. http://www.python.org/dev/peps/pep-0343/
            os.lseek(fd, offset, 0)
            return os.read(fd, size)
    
    """
    os.listdir(path)
		Return a list containing the names of the entries in the directory given by path. 
		The list is in arbitrary order. It does not include the special entries '.' and 
		'..' even if they are present in the directory.
	http://docs.python.org/library/os.html#os.listdir
    """
    def readdir(self, path, fd):
        return ['.', '..'] + os.listdir(path)

    #http://docs.python.org/library/os.html#os.readlink
    readlink = os.readlink
    
    #http://docs.python.org/library/os.html#os.close
    def release(self, path, fd):
        return os.close(fd)
        
    #http://docs.python.org/library/os.html#os.rename
    def rename(self, old, new):
        return os.rename(old, self.root + new)
    
    #http://docs.python.org/library/os.html#os.rmdir
    rmdir = os.rmdir
    
    """
    The function statvfs() returns information about a mounted file system.
               f_bsize;   file system block size 
               f_frsize;  fragment size 
               f_blocks;  size of fs in f_frsize units 
               f_bfree;   # free blocks 
               f_bavail;  # free blocks for non-root 
               f_files;   # inodes 
               f_ffree;   # free inodes 
               f_favail;  # free inodes for non-root 
               f_fsid;    file system ID 
               f_flag;    mount flags 
               f_namemax; maximum filename length 
	http://manpages.ubuntu.com/manpages/lucid/en/man2/statvfs.2.html
    http://docs.python.org/library/os.html#os.statvfs
    """
    def statfs(self, path):
        stv = os.statvfs(path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))
    
    #http://docs.python.org/library/os.html#os.symlink
    def symlink(self, target, source):
        return os.symlink(source, target)
    
    def truncate(self, path, length, fd=None):
        with open(path, 'r+') as f:
			#A template for opening a file that ensures the file is closed when 
			#the block is left. http://www.python.org/dev/peps/pep-0343/
            size = os.path.getsize(path)
            if length <> size and not ".version" in path:
                data = f.read(size)
                fn = os.open(path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'), os.O_WRONLY | os.O_CREAT)
                os.write(fn,data)
                os.close(fn)
            f.truncate(length)
    
    #Remove (delete) the file path. This is the same function as remove(); the unlink() 
    #name is its traditional Unix name. http://docs.python.org/library/os.html#os.unlink
    #http://docs.python.org/library/datetime.html?highlight=time#strftime-behavior
    def unlink(self, path):
		os.rename(path, path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'))
	#	os.unlink
	
    #http://docs.python.org/library/os.html#os.utime
    utimens = os.utime
    
    #http://docs.python.org/library/os.html#os.write
    def write(self, path, data, offset, fd):
        with self.rwlock:
            if not ".version" in path:
                ft = os.open(path, os.O_RDONLY)
                size = os.path.getsize(path)
                backdata = os.read(ft, size)
                fn = os.open(path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'), os.O_WRONLY | os.O_CREAT)
                os.write(fn, backdata)
                os.close(fn)            
            os.lseek(fd, offset, 0)
            return os.write(fd, data)

if __name__ == "__main__":
    if len(argv) != 3:
        print 'usage: %s <root> <mountpoint>' % argv[0]
        exit(2)	# Unix programs generally use 2 for command line syntax errors
    fuse = FUSE(Loopback(argv[1]), argv[2], foreground=True)
