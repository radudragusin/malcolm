import time
import os
import shutil
import xattr

MFSConfig = dict([
	('versioning_enabled', 'true'),
	('max_no_versions', '-1'), 		#-1:disabled
	('max_file_size', '524288000'), 	#500MB
	('timestamp_format', '%Y-%m-%d-%H-%M-%S'),
	('mountpoint_source', ''),
	('mountpoint_dest', '')
])

def rmdir(path):
	if shouldVersion(path):
		shutil.move(path, versionPath(path))
	else:
		shutil.rmtree(path) #os.rmdir(path)

def truncate(path, length, f):
	size = os.path.getsize(path)
	if length <> size and shouldVersion(path):
		data = f.read(size)
		fn = os.open(versionPath(path), os.O_WRONLY | os.O_CREAT)
		os.write(fn,data)
		os.close(fn)

def unlink(path):
	if shouldVersion(path):
		os.rename(path, versionPath(path))
	else:
		os.unlink(path)

def write(path):
	if shouldVersion(path):
		ft = os.open(path, os.O_RDONLY)
		size = os.path.getsize(path)
		backdata = os.read(ft, size)
		fn = os.open(versionPath(path), os.O_WRONLY | os.O_CREAT)
		os.write(fn, backdata)
		os.close(fn)
		os.close(ft)

#build the path of the new version (format: .<filename>-<timestamp>.MFS)
def versionPath(oldpath):
	(d, b) = os.path.split(oldpath)
	return d + os.sep + '.' + b + '-' + time.strftime(MFSConfig['timestamp_format']) + '.MFS'
			
def shouldVersion(path):
	apath = os.path.join(MFSConfig['mountpoint_source'],os.path.relpath(str(path),MFSConfig['mountpoint_dest']))
	attrfile = xattr.xattr(apath)
	if not ".MFS" in path:
		if 'user.versioning_enabled' in attrfile:
			if attrfile.get('user.versioning_enabled') == 'true':
				if 'user.max_file_size' in attrfile:
					if int(attrfile.get('user.max_file_size')) > os.path.getsize(path):
						return True
					else:
						return False #file too big to be versioned
				else:
					if int(MFSConfig['max_file_size']) > os.path.getsize(path):
						return True
					else:
						return False #file too big to be versioned
			else:
				return False #versioning disabled
		else:
			if MFSConfig['versioning_enabled'] == 'true':
				return True
			else:
				return False #versioning disabled by default
	else:
		return False #no need to version a version
	
import MFSComFUSE

def startFS(sourcePath,destPath,fg=True):
	MFSComFUSE.startFS(sourcePath, destPath, fg)
	
