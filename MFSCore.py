import time
import os
import shutil
import xattr
import re


"""The MFSConfig dictionary: 
	This is the default configuration for the filesystem. This configuration will be used 
	unless otherwise specified in the setting.MMFS file."""
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
		shutil.rmtree(path)

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

def versionPath(oldpath):
	"""Returns a string containing the versioned path of the oldpath argument.
	The new path is build based on the format: .<filename>-<timestamp>.MFS
	"""
	(d, b) = os.path.split(oldpath)
	return d + os.sep + '.' + b + '-' + time.strftime(MFSConfig['timestamp_format']) + '.MFS'
			
def shouldVersion(path):
	"""Returns True if the file (given as path) obeys the versioning restrictions, and False otherwise.
	Returns True is all of the following file settings are satisfied:
		it is not a version file (a file of format '.<filename>-<timestamp>.MFS')
		the versioning_enabled attribute equals 'true'
		the max_file_size attribute for the file is bigger than the actual file size
		the max_no_versions attribute is bigger than the current number of versions of the file
	The attributes are taken from the file's extended attributes. If an attribute cannot be found in the file's 
	extended attribute, the filesystem's default value will be used.
	"""
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
	"""Returns True if the file has versioning enabled (given by the 'versioning_enabled' setting of the file). False otherwise.
	The value of the 'versioning_enabled' is taken from the extended attribute of the file, and if there is no such xattribute,
	it uses the filesystem's default value.
	Takes an xattr object (corresponding to a path) as argument.
	"""
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
	"""Returns True if the file has not yet reached the maximum number of versions permitted(given by the 'max_no_versions' 
	setting of the file). Returns False otherwise.
	Takes two arguments. The first is a xattr object corresponding to the path given as second argument.
	The value of the 'max_no_versions' is taken from the extended attribute of the file, and if there is no such xattribute,
	it uses the filesystem's default value.
	A value of -1 for the 'max_no_versions' means that the number is unlimited (this is the default setting). 
	A value of n>-1 means that a file can have only n versions, plus itself.
	If the maximum number of versions has been reached, versioning will no longer take place, except in the event in which 
	some of the older versions are manually deleted. [This behavior should be changed in future versions, so that the older 
	versions are deleted when the maximum number has been reached, thus making space for the newest version]
	"""
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
	"""Returns an integer representing the number of versions the file (given by argument apath) currently has.
	A version file is a file of format '.<filename>-<timestamp>.MFS' 
	It only searches in the current directory.
	"""
	if apath[-1] == os.sep:
		(apath,file) = os.path.split(apath[1:-1])
	else:
		(apath,file) = os.path.split(apath)
	files = os.listdir(apath)
	r = re.compile("^\."+file+"-....-..-..-..-..-..\.MFS$")
	versions = filter(r.search, files)
	return len(versions)
	
import MFSComFUSE

def startFS(sourcePath,destPath,fg=True):
	"""Passes the filesystem start call to the MFSComFUSE module. 
	It is called from module MFSAPI.
	"""
	MFSComFUSE.startFS(sourcePath, destPath, fg)
	
