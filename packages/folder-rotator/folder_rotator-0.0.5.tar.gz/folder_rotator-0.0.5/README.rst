==============
Folder Rotator
==============
 
This rotates the output paths so that write limitations are not exceeded. This
is mostly for writing lots of sound files for an IOx app I created.

The actual problem
++++++++++++++++++

Look, I really don't know that much about it, but apparently in the Linux
filesystem there is a data-structure called an inode that describes things like
files and folders. The inode stores things like the attributes of the object
and where it is located on disk. Anyway, you have a limit of these per folder,
so when you write too many files per folder (in my particular case this was
~13000) you suddenly get an error saying the disk is full. The disk is not full
you just ran out of inodes. You can solve this by creating more directories...
here we are :fire:
