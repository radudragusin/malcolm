## TO\_DO List ##

  * DONE ~~when closing the application, if the file system is not stopped, it will be stopped~~
  * when the maximum number of versions for a path is reached, delete its oldest version
  * add support for **setxattr**, **getxattr**, **removexattr** and possibly **listxattr**
  * DONE ~~add icons to the GUI and About box~~
  * make the stop button turn red when a the file system is mounted
  * when changing a directory's versioning policy also change the versioning policy of its subtree
  * add a logging tab
  * add support for limiting the frequency of versioning
  * currently the user cannot change the general settings from the CLI (in the future, add options for changing these settings)
  * add support for the event in which a file was deleted, and the user selects a version of a deleted file
  * add support for modifying the maximum file size of a version (currently defaults to 500MB and cannot be changed from the interface)