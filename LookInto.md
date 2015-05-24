## Stuff to look into ##

  * `QDesktopServices.DocumentsLocation` -> Returns the user's document folder - for use as standard browsing location as the source of the mount
  * `bool QDesktopServices.openUrl ( const QUrl & url )   [static]` - Opens the given url in the appropriate Web browser for the user's desktop environment, and returns true if successful; otherwise returns false. If the URL is a reference to a local file (i.e., the URL scheme is "file") then it will be opened with a suitable application instead of a Web browser.