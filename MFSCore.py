import time
import os
import shutil


def rmdir(path):
	shutil.move(path, path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'))

def truncate(path, length, f):
	size = os.path.getsize(path)
	if length <> size and not ".version" in path:
		data = f.read(size)
		fn = os.open(path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'), os.O_WRONLY | os.O_CREAT)
		os.write(fn,data)
		os.close(fn)

def unlink(path):
	os.rename(path, path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'))

def write(path):
	if not ".version" in path:
		ft = os.open(path, os.O_RDONLY)
		size = os.path.getsize(path)
		backdata = os.read(ft, size)
		fn = os.open(path + ".version" + time.strftime('%Y-%m-%d-%H-%M-%S'), os.O_WRONLY | os.O_CREAT)
		os.write(fn, backdata)
		os.close(fn)
		os.close(ft)
			
