
```
Principles of Computer System Design
Assignment 2a
Kostas Rutkauskas, Radu Dragusin, Paula Petcu

```

# Requirements Specification #

## 1 INTRODUCTION ##

1.1 Product Overview

MalcolmFS - a stackable file system that integrates versioning of the files on top of traditional file system behavior.

1.2 Purpose

The purpose of this document is to present a description and listing of the functionality of a stackable file system that supports file versioning. This document is intended for users of the system including designers, implementation unit and evaluators.

1.3 Scope

The developed product is a stackable file system that integrates some functionality on top of traditional file systems. MalcolmFS will itself provide a set of features that will allow users to set access rights on files, manage their versioning rules and tour through all life-cycle of any file in its file system.

The primary goal of such an application is to transparently provide assistance for a user who has difficulty in understanding the versioning concept. The following is achieved by adding the invisible, yet easy to use feature of "going back" to past and using the previously saved content of a file in the file system.

MalcolmFS itself is a fully functioning layer on top of traditional file systems. Additionally, MalcolmFS provides a library allowing external applications to perform operations such as retrieving previous versions of files, as well as modifying retention or access policies over a particular file. The document broadly presents these functionalities, excluding the GUI of MalcolmFS. The GUI part is restricted to the specification of interfaces that are required for its functionality.

1.4 Abbreviation

Stackable file system - a layer on top of underlying file system providing additional functionality. {1}

FUSE - Filesystem in Userspace. {2}

1.5. Overview

Following is an overall description of the system, including the product's perspective, its functions and general constraints, followed by the system requirements and a prototype design.

1.6. References

{1} Heidemann, J. S. and Popek, G. J. 1994. File-system development with stackable layers. ACM Trans. Comput. Syst. 12, 1 (Feb. 1994), 58-89.

{2} http://fuse.sourceforge.net/

{3} http://fuse4bsd.creo.hu/README.new_fusepy_api.html

{4} http://en.wikipedia.org/wiki/Filesystem_in_Userspace

{5} Cornell, B., Dinda, P. A., and Bustamante, F. E. 2004. Wayback: a user-level versioning file system for linux. In Proceedings of the Annual Conference on USENIX Annual Technical Conference (Boston, MA, June 27 - July 02, 2004). USENIX Annual Technical Conference. USENIX Association, Berkeley, CA, 27-27.

{6} Beazley, D. M. 1996. SWIG: an easy to use tool for integrating scripting languages with C and C++. In Proceedings of the 4th Conference on USENIX Tcl/Tk Workshop, 1996 - Volume 4 (Monterey, California, July 10 - 13, 1996). USENIX Tcl\Tk Conference. USENIX Association, Berkeley, CA, 15-15.

{7} Saltzer, J. H. and Kaashoek, M. F. 2009 Principles of Computer System Design: an Introduction. Morgan Kaufmann Publishers Inc., Section 6.1.2

{8} A.Kantee, and A. Crooks. 2007. ReFUSE: Userspace FUSE Reimplementation Using puffs. In 6th European BSD Conference (2007).

{9} Peterson, Z. and Burns, R. 2005. Ext3cow: a time-shifting file system for regulatory compliance. Trans. Storage 1, 2 (May. 2005), 190-212.

{10} Collins-Sussman, B. 2002. The subversion project: buiding a better CVS. Linux J. 2002, 94 (Feb. 2002), 3.

{11} Tichy, W. F. 1985. RCS—a system for version control. Softw. Pract. Exper. 15, 7 (Jul. 1985), 637-654.

{12} Peterson, Z. N. J., Burns, R., and Stubblefield, A. 2004. Limiting liability in a federally compliant file system. In Proceedings of the PORTIA Workshop on Sensitive Data in Medical, Financial, and Content Distribution Systems.

{13} Pilato, M. 2004 Version Control with Subversion. O'Reilly & Associates, Inc.

{14} Muniswamy-Reddy, K., Wright, C. P., Himmer, A., and Zadok, E. 2004. A Versatile and User-Oriented Versioning File System. In Proceedings of the 3rd USENIX Conference on File and Storage Technologies (San Francisco, CA, March 31 - 31, 2004). Conference On File And Storage Technologies. USENIX Association, Berkeley, CA, 115-128.

{15} IEEE Std 830-1998 IEEE Recommended Practice for Software Requirements Specifications - Description

{16} Jacobsen, C. L. 2009. Assignment 1. In SCI-B2-0910-Principles of Computer System Design, Datalogisk Institut, Kobenhavns Universitet.

{17} Jacobsen, C. L. 2009. Assignment 2a. In SCI-B2-0910-Principles of Computer System Design, Datalogisk Institut, Kobenhavns Universitet.

## 2 OVERALL DESCRIPTION ##

The developed software, MalcolmFS, is a stackable file system. It assists users on the managing operations of workflow over the files in the traditional file system. From the common user's perspective it is an ordinary operations supporting file system that also possesses the feature of navigation through a file's history.

The product benefits the user by minimizing the impact of data-loss which may arise from the actions of unexperienced computer users, and by simplifying the recovery from such an event. An administrator will setup and maintain the access rights and retention policies on the files, while the user is restricted to customization of its own criteria on retention policies. The product will contain a rigorous interface for the GUI and the API for external applications in order for these to use the provided functionality.

The intended, but not limited, audience is the everyday computer user who has either Mac OS X or GNU/Linux installed on his/her machine and from time to time requires the ability to revert a particular file to its previous versions.

2.1 Product Perspective

The system needs some third party products (FUSE) in order to function on top of underlying file systems. Nevertheless, the functionality should be transparent for end-users and require no additional training. The only exception is that the end-user should be familiar with the idea that files are saved from time to time and it is possible to use the snapshot of the file that was versioned previously.

Users can retrieve previous versions of files that are stored in their file system. Users can also setup the versioning parameters, or retention policies, i.e. how long a version should be stored or how frequently versioning should occur, etc. The user can get the differences (diffs) between versions and proceed to using previous version of a file if needed. All the abovementioned actions are performed using the command line interface.

An administrator is, like his name suggests, responsible for administrative tasks. These comprehend managing the general retention policies and access rights.

2.2 Product Functions

  * MalcolmFS should act in background and be transparent for users in terms of usage (as it cannot be transparent eventually, or probably, in terms of performance).

  * MalcolmFS should operate with any type of files and should work in all operating systems that support FUSE and Python.

  * The user can setup the rules under which the versioning engine operates. That is, the user is free to choose the storage or time limits for MalcolmFS.

  * The user can retrieve, compare and use the working copy of a file's previous version provided that the version is stored in MalcolmFS.

  * The user can select which files should be versioned and which ones are restricted to traditional behavior.

  * The administrator can set the general retention policies and access rights on versions for users, i.e. it is possible to forbid a user to revert to previous versions (such a feature might be useful for logging purposes).

2.3 User Characteristics

A user should be able to use MalcolmFS without any prior knowledge of version control systems. The only additional activities will include usage of command line tools which, to some extend, might be considered as any other particular application.
A user can choose whether his/her changes on files are visible to other users or not.

2.4 General Constraints

  * Like any other versioning system, MalcolmFS exhibits the overhead on usage of storage. MalcolmFS is based on copy-on-write transactions. Therefore, each time the file is saved, the full previous version of the file is saved to the disk. Depending on negligently set retention policies, the usage of MalcolmFS might lead to significant overhead. The dealing of such cases is left for the administrator who has the right and ability to set the overall retention policies, and prevent the degradation that arises from the extensive usage of disk space.

  * MalcolmFS is also limited to operating systems which support FUSE and Python.

  * The product is written in C and Python. C is the native API, and the Python binding supports all highlevel methods of the FUSE library. {3}

  * MalcolmFS should provide an API to other applications which would use it, thus benefiting of automated file versioning.

2.5 Assumptions and Dependencies

  * The operating system where the product will run on must be either Linux with a kernel v2.4/2.6 or Mac OS X.

  * FUSE 2.8 or higher must be installed.

  * Python 2.4 or higher must be also installed.

## 3 SPECIFIC REQUIREMENTS ##

3.1 External Interface Description

**FUSE**

The product will need FUSE as it is an in-between layer that forwards product's calls to the operating system's kernel. Filesystem in Userspace (FUSE) is a loadable kernel module for Unix-like computer operating systems, that allows non-privileged users to create their own file systems without editing the kernel code. This is achieved by running the file system code in user space, while the FUSE module only provides a "bridge" to the actual kernel interfaces. {4}

It is important to distinguish two areas in which FUSE operates:

3.1.1 MalcolmFS <==> FUSE lib.
```
uses documentation that comes with FUSE package
```

When MalcolmFS calls fuse\_main() (lib/helper.c),
fuse\_main() parses the arguments passed to MalcolmFS,
then calls fuse\_mount() (lib/mount.c).

fuse\_mount() creates a UNIX domain socket pair, then forks and execs
fusermount (util/fusermount.c) passing it one end of the socket in the
FUSE\_COMMFD\_ENV environment variable.

fusermount (util/fusermount.c) makes sure that the fuse module is
loaded. fusermount then open /dev/fuse and send the file handle over a
UNIX domain socket back to fuse\_mount().

fuse\_mount() returns the filehandle for /dev/fuse to fuse\_main().

fuse\_main() calls fuse\_new() (lib/fuse.c) which allocates the struct
fuse datastructure that stores and maintains a cached image of the
filesystem data.

Lastly, fuse\_main() calls either fuse\_loop() (lib/fuse.c) or
fuse\_loop\_mt() (lib/fuse\_mt.c) which both start to read the filesystem
system calls from the /dev/fuse, call the usermode functions
stored in struct fuse\_operations datastructure before calling
fuse\_main(). The results of those calls are then written back to the
/dev/fuse file where they can be forwarded back to the system
calls.

3.1.2 FUSE lib. <==> OS kernel
```
uses documentation that comes with FUSE package
```

The kernel module consists of two parts. First the proc filesystem
component in kernel/dev.c -and second the filesystem system calls
kernel/file.c, kernel/inode.c, and kernel/dir.c

All the system calls in kernel/file.c, kernel/inode.c, and
kernel/dir.c make calls to either request\_send(),
request\_send\_noreply(), or request\_send\_nonblock(). Most of the calls
(all but 2) are to request\_send(). request\_send() adds the request to,
"list of requests" structure (fc->pending), then waits for a response.
request\_send\_noreply() and request\_send\_nonblock() are both similar in
function to request\_send() except that one is non-blocking, and the
other does not respond with a reply.

The proc filesystem component in kernel/dev.c responds to file io
requests to the file /dev/fuse. fuse\_dev\_read() handles the
file reads and returns commands from the "list of requests" structure
to the calling program. fuse\_dev\_write() handles file writes and takes
the data written and places them into the req->out datastructure where
they can be returned to the system call through the "list of requests"
structure and request\_send().

**MalcolmFS API**

MalcolmFS will have an API that can be called from an external application program to access features of versioning that MalcolmFS provides. The external application must initialize the MalcolmFS library in order to use MalcolmFS functions. The application must also terminate the library when MalcolmFS functions are no longer needed. The external application is therefore responsible for managing initialization and termination of the library within the application process.

3.2 Functional requirements

3.2.1. Create a retention policy

(i) User selects retention policies for specific file or directory. The retention policies might be:

> (i).a Number - the user can set the maximum number of versions in a version set.

> (i).b Time - the user can set the maximum amount of time to retain the versions.

> (i).c Space - the user can set the maximum amount of space that a version set can consume.

> (i).d Frequency - the user can set the period of time for which only the newest version of a file will be stored. That is, if the last modification of the file was made before the specified period, then the new version of the file will overwrite the current version.

> For (i).a, (i).b and (i).c, if the defined limits are surpassed, the versions will be discarded one by one starting from the oldest until the limit is satisfied or until there is no other version than the current one.

(ii) User selects system-wide retention policies in terms of:

> (ii).a Location - the user can select a list of file locations marked either to be versioned or to be ignored from versioning.

> (ii).b Extension - the user can select a list of file extensions marked either to be versioned or to be ignored from versioning.

> (ii).c Size - the user can select a list of file sizes marked either to be versioned or to be ignored from versioning.

(iii) MalcolmFS saves retention policy information in the following ways:

> (iii).a For a file - if it does not exist, a new hidden meta-data file, named `.<filename>`.MMFS (where `<filename>` states for the file for which the retention policies are created) is created with the information on retention policies of that file. If such a file exists, the information is updated.

> (iii).b For a directory - the information is stored in a meta-data file named `..<parentdirectoryname>`.MMFS, and each time the files are affected, the same actions as in (iii).a are applied for files within that directory.

(iv) User overwrites the autostart behavior of versioning file system by manually enabling and disabling the versioning behavior.

(v) Updating policies.

3.2.2. Handle `write()` action

(i) User (external application) performs some operations with files that invoke the write() function.

(ii) FUSE intercepts the write and passes its arguments to the MalcolmFS handler (namely, MFSComFUSE).

(iii) MSFComFUSE forwards the parameters to respective procedures in MFSCore that act according to

> (iii).a retention policies (either file or directory)

> (iii).b storage policies (either file or directory)

(iv) `.<filename>`.MMFS is updated with the new version information.

(v) A file named `.<filename>-<timestamp>`.MFS is created containing the new version content.

3.2.3. User (external application) requests information on previous versions of a particular `<filename>`.

(i) User invokes such calls through command line tools while applications use the MFSAPI APIlib.

(ii) MFSAPI prepares and passes the query for MFSCore.

(iii) MFSCore parses `.<filename>`.MMFS file and creates a report on provided criteria.

(iv) MFSAPI presents user/application `<filename>` version data.

3.2.4. User (external application) consults the content of a previous version of a particular `<filename>`.

(i) User invokes such calls through command line tools while applications use the MFSAPI APIlib.

(ii) MFSAPI prepares and passes the query for MSFCore.

(iii) MFSCore parses `.<filename>`.MMFS file and, based on provided criteria, creates a temporary file with the content of the requested version of `<filename>`.

(iv) MFSAPI presents user/application the content of the `.<filename>-<timestamp>`.MFS version of `<filename>` through the temporary file created in the previous step.

3.2.5. User (external application) reverts to a previous version of particular `<filename>`.

(i) User invokes such calls through command line tools while applications use MFSAPI APIlib.

(ii) MFSAPI prepares and passes the query for MSFCore.

(iii) MFSCore parses the `.<filename>`.MMFS file and acts according to the retention and access policies of that `<filename>`. In this case, the frequency limit is not taken into account.

(iv) `<filename>` is updated with the information contained in the `.<filename>`.MMFS file.

3.2.6. Administrator sets access rights and global retention policies.

(i) Administrator invokes such calls through command line tools.

(ii) MFSAPI prepares and passes the query for MFSCore.

(iii) MFSCore sets the storage and retention policies parameters of `<filename>` in the `.<filename>`.MMFS file.

(iv) Updating policies.

3.3 System Architecture

**_MFS\_architecture.png_**

MalcolmFS architecture will itself be formed out of three logical modules:

**MFSCore**- a module which contains all versioning logic of the system.

**MFSComFUSE**- a communication layer between MFSCore and FUSElib that will forward calls and receive data from FUSE library.

**MFSAPI** - a module, responsible for communication between product and external world. It contains functions of API for external application and command line tools support for the everyday user.

**_mfs\_fuse\_structure.png_**

The FUSE kernel module and the FUSE library communicate via a special file descriptor which is obtained by opening /dev/fuse. This file can be opened multiple times, and the obtained file descriptor is passed to the mount syscall, to match up the descriptor with the mounted filesystem.

The FUSE library and MalcolmFS, as stated before, communicate through the interface which is formed out of the FUSE API library and the MFSComFUSE module that uses it.

3.3.1. MFSCore

A module that implements the core logic of the MalcolmFS, and is itself organised into three sub-modules. MFSCore handles the logic of file versions. MalcolmFS is based on copy-on-write transactions. Each time it gets a notification from the MFSComFUSE module about a new `write` action, MalcolmFS acts according to the established criteria through the Versioning Policy Sub-module. In general, MalcolmFS creates multiple hidden files next to each of the versioned files. The metadata information is stored in a hidden file, named `.<filename>`.MMFS. This file contains the retention policies for the file and information such as timestamp and filesize for each version of the file. The data for each version of the file is contained in `.<filename>-<timestamp>`.MFS.


**The Versioning Policy Sub-module**

Handles retention policies. MFSCore contains all the needed logic for managing files state depending on their retention policies. The Versioning Policy Submodule is responsible for establishing if a modified file is to be versioned or not. The component takes this decision based on the metadata stored for the specified file, which contains information regarding the location, size and extension policies, storage policies, and the limits in number, time, space and frequency for a particular file. (See Section 3.2.1. for details on retention policies)

**The Properties Inspection Sub-module**

Provides the user with the facility of viewing the versioning properties of a file. The properties are stored in the metadata of the specified file, which contains information regarding the versioning policies, the versioning frequency and the other limits, and each version's creation date and size. (See Section 3.2.1. for details on retention policies, and Section 3.2.3. on requesting information about previous versions of files)

**The Version Creation Sub-module**

Handles file versions creation and is closely integrated with the Versioning Policy and Properties Inspection sub-modules. Before creating a new version, the sub-module sends a request to the Versioning Policy Sub-module to find out if a new version should be created according to the file's retention policies.

**The Restore Sub-module**

The sub-module is responsible for two main functionalities: providing the user with the facility to view the content of a previous version of a file, and restoring a specified version of a file. When restoring, any retention policy is overridden so that the restore process can continue without any unwanted data-loss. In order to provide the content of a previous version of a file, but without reverting, a temporary file will be used for displaying the requested content. (See Sections 3.2.4. and 3.2.5. on consulting and restoring previous versions of files)

3.3.2. MFSComFUSE

A specialized module for handling communication between MalcolmFS and FUSE. A layer that integrates MalcolmFS logic into the underlying kernel filesystem by using FUSE API.

3.3.3. MFSAPI

A module for interfacing MalcolmFS to the external environment, namely applications and users. It provides command line tools which allow the usage of the standard features (e.g. get previous version, set retention policies, set access rights) of MalcolmFS for external users.

3.4 Software System Attributes / Nonfunctional requirements

3.4.1 Reliability

One of the functionalities of the system is reverting to previous versions of a particular file.
The user should in no case find himself/herself losing data, and therefore, even if one version of the file becomes corrupt, the other versions will still be available.
Another important reliability feature is that all versions and files will be available without the need of running MalcolmFS, but just using the underlying file system.

3.4.2 Availability

MalcolmFS should be available at any time during the usage of the file system. That is, MalcolmFS should be started at the startup of operating system and closed properly on its shut down, unless the user chooses to manually enable and disable the versioning. All these actions should be transparent for the user as his only concern should be the traditional usage of file system rather than thinking about versioning shading.

3.4.3 Security

In order to fulfil security requirements, MalcolmFS introduces the administrator user property. The administrator of the underlying OS is responsible for setting global retention policies (for managing performance issues) and access rights on versioning for files. An ordinary user may overwrite retention policies, however may not change access rights.

3.4.4 Maintainability

The program is build to work as a transparent agent. In a good configured environment, with a reliable administration setting, this should imply that no special maintenance is needed to keep MalcolmFS running.

3.4.5 Portability

MalcolmFS will be designed on a GNU/Linux platform with portability in mind to run this application on this platform or one of its variants. As FUSE is also supported in Mac OS X, the implementation part is oriented on abstraction. That is, the logical distribution of the system into 3 modules states, that there is a module for handling logic (which will not change from platform to platform, as well as from one version to another version of FUSE) while modules MFSComFUSE and MFSAPI are targeted to provide platform specific (MFSAPI) and version-dependent (MFSComFUSE) implementations.

3.4.6 Performance

Considering the fact that snapshots are used instead of deltas, the performance impact should be considerably better than of a versioning file system that uses logs. In this context, a less than 15% performance impact is expected. {5}

3.5 Design Decisions

**Languages and Bindings**

The programming languages in which MalcolmFS must be implemented are C and Python. The C implemented components must be those that are computationally intensive, such as the  MFSCore's Version Creation and Restore sub-modules, and the MFSComFUSE module. For the less computationally intensive modules, the implementation should be done in Python, because of the language's fast development properties and its ability to closely cooperate with the C applications. {6}

Python has a large and comprehensive set of libraries that will facilitate the fast development of a prototype. After implementing the prototype, various performance aspects will be tested for compliance with the non-functional requirements, and in the case where the performance is evaluated as not satisfactory and a re-implementation in C would solve the performance problems, a new iteration in the development cycle will be planned including the new implementation strategy. {7}

Both C and Python have implementations on every of the platforms on which FUSE can run.

**Stackable File System**

The design of MalcolmFS will closely follow that of a stackable file system. Specifically, we are not interested in writing a complete file system, but one that extends any existing file system. This approach has two main advantages. The first is that the user does not have to migrate his data in order to use versioning capabilities of our file system. Another important advantage is that the user could read and write versioned data using just the underlying file system (in the case in which the user wants to read or write data on a computer that does not have MalcolmFS installed, he could do so without problems, the only setback being that no new versions of files will be created without MalcolmFS). {5}

**FUSE**

FUSE is the most widely used and the best tested file system in user space library. It is available on a number of Unix compatible platforms, such as Linux, for which it was originally developed, and also MacOS X, FreeBSD and NetBSD {8}. One important decision for choosing FUSE is that there are a number of successful implementations of file systems that use it {8}, even some versioning file systems {5}. Moreover, there are several stackable file systems implemented using FUSE, so it is tested for the scenario we are interested in. Furthermore, FUSE has bindings for many programming languages, including Pyhton {3}. On the other hand, the most important disadvantage is that writing a file system on top of FUSE, although easier for the programmer, is not as good in terms of performance as writing the file system in kernel {9}.

**Existing Revision Control Systems**

Some of the revision control systems work best only with text files {10}, but our system has to handle all types of files. The most important aspect that we are interested in, that is not supported by some revision control libraries {11}, is the deletion of a specific version of a file. This is very important for security reasons {12}.
For our system, it is very important that the user can access the versioned files without the need of MalcolmFS, but also by using just the underlying file system. This behavior would not be possible using an existing version control system, because these systems store versioned data in data structures that are not transparent to the underlying file system {13}.


## 4 PROTOTYPE DESIGN ##

4.1 General Overview

We have decided to use the evolutionary prototyping development strategy which consists of building a robust prototype using a well-structured design that is established prior to writing any code. The first prototype in such a development strategy implements a very limited number of requirements, but nevertheless strictly follows the established structure and design, allowing future prototypes to refine and build on top of the first prototype.

4.2 Prototype Architecture

The architecture of the prototype closely follows the full system's design as described in Section 3.3, but skips through all but the most minimum requirements for a minimal versioning file system.

4.3 Specific Requirements

The requirements were prioritized according to their role, significance and value for the versioning file system. From the set of selected requirements, a classification was performed in order to establish the importance of each requirement inside the prototype design. These internal priorities are marked by the action verbs “must” and “should”.

The prototype's requirements follow the system's requirements specified under section 3.2 and thus for each prototype's requirement, a reference to the corresponding requirement in the system specifications is given.

4.3.1. Create a retention policy

> (i) The user _should_ be able to select the retention policy for a specific file or directory. By retention policy it is understood the maximum number of versions to be stored in a version set. (System Requirement 3.2.1.i.a)

> (ii) MalcolmFS _should_ save the retention policy information for files (System Requirement 3.2.1.iii)

> (iii) The user _must_ be able to manually enable and disable the versioning behavior. (System Requirement 3.2.1.iv)

4.3.2. The system _must_ handle write() action as specified in System Requirement 3.2.2

4.3.3. The user _must_ be able to request information on previous versions of a particular `<filename>`, which is handled as specified in System Requirement 3.2.3

4.3.4. The user _must_ be able to consult the content of a previous version of a particular `<filename>`, which is handled as specified in System Requirement 3.2.4

4.3.5. The user _should_ be able to revert to a previous version of particular `<filename>`, which is handled as specified in System Requirement 3.2.5

The prototype will implement only a limited number of requirements from the entire set of requirements specified for MalcolmFS in Section 3.2. The prototype keeps the minimum set of requirements needed for a working versioning file system. The administrator privileges, for setting access rights and global retention policies (System Requirement 3.2.6) were left out, as they were not considered a priority for the prototype. Likewise, the user-specified retention policies specifications (described in Section 3.2.1) were limited in number, and reduced to the one considering the maximum number of versions to be stored.