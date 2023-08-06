django-mogilefs-explorer
========================
django-mogilefs-explorer is a Django application, which helps interacting with
[MogileFS](https://github.com/mogilefs) installation. Basic usage includes:
- listing of files in MogileFS on per-directory basis
- showing images on admin page
- downloading files
- uploading files

Rationale for application
-------------------------
Currently, as of version 2.73, MogileFS lacks full WebDAV support, namely
listing of files (via OPTIONS) and any concept of collections.
This makes it impossible to use existing API to navigate in filesystem.

Consequently, this app is a bit hacky, because it violates an isolation of
services: it connects to internal MogileFS metadata database, and uses it
for discovering stuff inside MogileFS.

Development roadmap
-------------------
- 0.1
  - installation, pypi distribution
- 0.2
  - initial django application structure
  - application configuration
  - plain listing of files, not directory-wise
- 0.3
  - direcotries: with help of functional indexes and some complex queries
    implement a virtual surrogate of collections
  - dual implementation for MySQL and PostgreSQL as MogileFS databases
  - navigate in these directories, list files
- 0.4
  - links to download file from MogileFS directly with browser
  - proxying download requests if MogileFS is not directly accessible
  - in-page display of images using above techniques
- 0.5
  - uploading files
- 0.6
  - archiving entire directory for downloading (?)
- ?.?
  - ???
