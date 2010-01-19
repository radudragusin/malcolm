import time
import os
import shutil
import xattr
import re

MFSConfig = dict([
	('versioning_enabled', 'true'),
	('max_no_versions', '-1'), 		#-1:disabled
	('max_file_size', '524288000'), 	#500MB
	('timestamp_format', '%Y-%m-%d-%H-%M-%S'),
	('mountpoint_source', os.path.expanduser('~')),
	('mountpoint_dest', os.path.expanduser('~'))
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
	apath = os.path.normpath(apath)
	attrfile = xattr.xattr(apath)
	
	if ".MFS" in path:
		return False #no need to version a version
		
	if os.path.getsize(path) > int(MFSConfig['max_file_size']):
		return False #file too big to be versioned
		
	if not isVersioningEnabled(attrfile) or not isInRangeToVersion(attrfile,apath):
		return False #file has either versioning disabled or the max number of versions per file was excideed
	
	return True

def isVersioningEnabled(attrfile):
	if 'user.versioning_enabled' in attrfile:
		if attrfile.get('user.versioning_enabled') == 'true':
			return True
		else:
			return False
	else:
		if MFSConfig['versioning_enabled'] == 'true':
			return True
		else:
			return False

def isInRangeToVersion(attrfile,apath):
	if 'user.max_no_versions' in attrfile:
		if int(attrfile.get('user.max_no_versions')) == -1:
			return True
		else:
			return noOfVersions(apath) <= int(attrfile.get('user.max_no_versions'))
	else:
		if int(MFSConfig['max_no_versions']) == -1:
			return True
		else:
			return noOfVersions(apath) <= int(MFSConfig['max_no_versions'])

def noOfVersions(apath):
	if apath[-1] == os.sep:
		(apath,file) = os.path.split(apath[1:-1])
	else:
		(apath,file) = os.path.split(apath)
	files = os.listdir(apath)
	r = re.compile("^\."+file+"-....-..-..-..-..-..\.MFS$") #version format: .<filename>-<timestamp>.MFS
	versions = filter(r.search, files)
	return len(versions)						
	
import MFSComFUSE

def startFS(sourcePath,destPath,fg=True):
	MFSComFUSE.startFS(sourcePath, destPath, fg)
	
