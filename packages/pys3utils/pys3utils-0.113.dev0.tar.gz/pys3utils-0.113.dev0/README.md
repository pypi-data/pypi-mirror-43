# pys3utils

Python s3 scripts and utilities. This library is intended to 
help push/pull resources from s3.

## Usage

To recursively sync a directory to s3 -- only syncing those files 
have been recently updated, write the following in python:

```python
from pys3utils import utils
utils.push_project_to_s3('my/path', 'my-bucket-name') 
``` 

This will recursively walk through all files listed under ``my/path``, 
and upload a copy to s3. After ``push_project_to_s3`` has been called, 
it creates and updates a hidden timestamp file in ``my/path``, called
 ``.s3_sync_timestamp``, which will
carry the last time (in ms) when an update/push occured. 

On a second call to ``push_project_to_s3``, all files that
have modified ``mtime`` before this  time stamp file will be ignored. 