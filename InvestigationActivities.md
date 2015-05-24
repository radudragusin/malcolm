December 21 2009:
  * Installed and configured a virtual machine with Ubuntu 9.10

December 22 2009:
  * Studied the python-fuse and fusepy bindings
  * Tried an example of using fusepy

December 23 2009:
  * Worked on the examples provided by fusepy ( http://code.google.com/p/fusepy/ )
  * Added to the repository a loopback filesystem that logs each operation to the console to use it, get a local copy of the source code and then mount a directory to a mountpoint with loopback:
```
hg clone https://malcolm.googlecode.com/hg/ malcolm 
python loopback.py rootdir mountpoint
# now every file system operation you do in mountpoint will be logged.
# to unmount:
fusermount -u mountpoint
```

January 15 2010:
  * Installed the `xattr` Python module
    * in Ubuntu: `sudo apt-get install python-xattr`
  * For xattr to work, need to do **one** of the following and then remount:
    * add in `/etc/fstab`, in the options section, `user_xattr`
    * `tune2fs -o user_xattr device`

January 16 2010:
  * Generate the Python code for the interface designed in Qt Designer:
> > `pyuic4 -o ui-MalcolmGUI.py MalcolmGUI.ui`