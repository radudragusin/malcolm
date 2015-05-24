# Introduction #

The MalcolmFS application was tested and works on Linux. Other POSIX platforms, such as FreeBSD, might be supported, provided you can install Python and QT 4.6.


# Details #


## Linux (Ubuntu) ##

The application was developed and tested in Ubuntu 9.10 and it's deployment on this operating system is very simple:

<font color='red'>
<h3>Important First Step</h3>

Because the underlying file system might be mounted without support for extended attributes, it is recommended that you enable them if they are not enabled. To test this, use:<br>
<br>
<h3><code>sudo tune2fs -l [device]</code></h3>

If the <code>Default mount options</code> field has the <code>user_xattr</code>, then you are OK and can skip to the next section. Otherwise, use this command before using the application:<br>
<br>
<h3><code>sudo tune2fs -o user_xattr [device]</code></h3>
Where <code>[device]</code> is the partition you want to use with MalcomFS, <b><code>/dev/sda1</code></b> for example.<br>
Note that the partition requires remounting before extended attributes can be used, thus if it is the system partition you would like to version, <b>you need to reboot your machine</b>.<br>
</font>

### Installing and Running ###

  1. install Mercurial to be able to checkout the code from the repository: `sudo apt-get install mercurial`
  1. install Qt4 libraries: `sudo apt-get install libqtcore4 libqtgui4`
  1. install the bindings needed for the program (`PyQt4`, `python-xattr`): `sudo apt-get install python-qt4 python-xattr`
  1. inside a shell, in the location where you want to copy MalcolmFS, issue: `hg clone https://malcolm.googlecode.com/hg/ malcolm`
  1. now change the directory: `cd malcolm`
  1. now you are ready to run the application using: `python MFSAPI.py`
  1. you could also run from the CLI using: `python -cli <root_dir> <mountpoint>`

Here is the fast three step install and run:
```
sudo apt-get install mercurial libqtcore4 libqtgui4 python-qt4 python-xattr
hg clone https://malcolm.googlecode.com/hg/ malcolm
python malcolm/MFSAPI.py
```

## Mac OS X ##

The application should work on Mac OS X, however it was not tested.

  1. install the Qt Library for Mac from http://qt.nokia.com/downloads/mac-os-cpp
  1. install Python for Mac from http://www.python.org/download/
  1. install the `PyQt4` binding for Mac from http://www.riverbankcomputing.co.uk/software/pyqt/download
  1. install the xattr python package from http://pypi.python.org/pypi/xattr/0.4