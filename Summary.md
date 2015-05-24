Principles of Computer System Design

A Version Controlled File system
Part IIa: Design

File System Design Summary


### Product Overview and Purpose ###

MalcolmFS is a stackable file system that integrates versioning of files on top of traditional file system behavior. The primary goal of such a system is to transparently provide assistance for the user who has difficulties in understanding the versioning concept. From the user's point of view, it is an ordinary operations supporting file system, but which adds the benefits of minimizing the impact of data-loss which may arise from the actions of an unexperienced computer user, and by simplifying the recovery from such an event.

### System Specifications ###

The product will use FUSE (Filesystem in Userspace) as an in-between layer that forwards product's calls to the operating system's kernel. (See Section 3.1. describing FUSE's external interface.)

The version controlled file system should be able satisfy the following requirements:
  * The user can select which files are to be versioned and which ones are restricted to traditional behavior. (See Section 3.2.1.(ii) on system-wide retention policies.)
  * The user can setup the rules under which the versioning engine operates. (See Section 3.2.1 for the specific requirements on creating retention policies.)
  * The user can retrieve and use the working copy of a file's previous version. (See Sections 3.2.4 and 3.2.5 on consulting and reverting previous versions of files.)
  * The user can visualize the information regarding previous versions of a file. (Section 3.2.3 describes how this works.)
  * The administrator can set the general retention policies and access rights on versions for users. (See Section 3.2.6.)
  * MalcolmFS should act in background and be transparent for users in terms of usage. (Section 3.2.2 describes how versioning is handled)

The most important non-functional requirements are reliability and availability, but security, maintainability and portability also need to be considered  (see Section 3.4).

### System Architecture ###

MalcolmFS architecture will be formed out of three logical modules: MFSCore, MFSComFUSE and MFSAPI. MFSCore is a module containing the versioning logic of the system, and which itself consists of four sub-modules that handle the versioning policies, the file versioning properties, the version creation, and the actual restoring. (A detailed description of these sub-modules is given in Section 3.3.1.) MSFComFUSE is the communication layer between MFSCore and the FUSE library, and MFSAPI is the module responsible for the communication between the product and the external world. (The system's architecture is described in Section 3.3. and pictured in the above figure.)

### Prototype Specifications ###

The architecture of the prototype closely follows the full system's design specifications described in Section 3.3, but implements only a limited number of requirements selected from the large set. The selected requirements represent the minimum demand for a working versioning file system. These are described in Section 4.3, and they were prioritized according to their value for the MalcolmFS.

The requirements that must or should be implemented in the prototype include:

  * The user should be able to select the maximum number of versions to be stored in a version set.
  * MalcolmFS should save the retention policy information for files.
  * The user must be able to manually enable and disable the versioning behavior.
  * The user must be able to request information on previous versions of a file.
  * The user must be able to consult the content of a previous version of a file.
  * The user should be able to revert to a previous version of particular.

### Design Decisions ###

The programming languages in which MalcolmFS will be implemented are C and Python. The C implemented components must be those that are computationally intensive, but in what regards the rest of the modules, the implementation should be done in Python, because of the language's fast development properties and its ability to closely cooperate with the C applications.

In our system, we are using FUSE, the most widely used and the best tested file system in user space library. It has bindings for many programming languages, including Pyhton and C, and is available on multiple platforms. Moreover, several successful stackable file systems implementations use FUSE, so it is tested for the scenario we are interested in.

These design decisions, as well as justifications for not using existing revision control systems, but rather designing our own, are presented in Section 3.5.

### Development Strategy ###

We have decided to use the evolutionary prototyping development strategy which basically consists of building a robust prototype by thinking ahead the structure and design of the application, and then constantly refining the prototype until all the requirements are satisfied. In this context, the described prototype is thus the first step in completing the MalcolmFS specifications.

Given that the implementation period of the prototype is limited to one week, the weeks preceding it should be efficiently exploited by investigation activities in how to use the FUSE functionalities from Python. At the beginning of the respective week, we should have the basic knowledge to successfully split up the coding of the MFSCore and MFSComFUSE modules.