A content hash based data store with a filesystem layer, using variable sized blocks, arbitrarily sized data and utilising some domain knowledge to aid efficient block boundary selection.


A content hash based data store with a filesystem layer, using
variable sized blocks, arbitrarily sized data and utilising some
domain knowledge to aid efficient block boundary selection.

*Note*: the "mount" filesystem facility uses FUSE,
which may need manual OS installation.
On MacOS this means installing `osxfuse`
for example from MacPorts.
You will also need the `llfuse` Python module,
which is not automatically required by this package.

The package provides the `vt` command to access
these facilities from the command line.

This system has two main components:
* Stores: storage areas of variable sized data blocks
  indexed by the cryptographic hashcode of their content
* Dirents: references to filesystem entities
  containing hashcode based references to the content

These are logically disconnected.
Dirents are not associated with particular Stores;
it is it sufficient to have access to any Store
containing the required blocks.

The other common entity is the Archive,
which is just a text file containing
a timestamped log of revisions of a Dirent.
These can be mounted as a FUSE filesystem,
and the `vt pack` command simply stores
a directory tree into the current Store,
and records the stored reference in an Archive file.

See also the Plan 9 Venti system:
(http://library.pantek.com/general/plan9.documents/venti/venti.html,
http://en.wikipedia.org/wiki/Venti)
which is also a system based on variable sized blocks.
