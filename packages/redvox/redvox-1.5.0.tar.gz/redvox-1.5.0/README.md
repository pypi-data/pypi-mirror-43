### RedVox Python SDK

This repository contains code for reading and working with the RedVox API 900 data format.

See: https://bitbucket.org/redvoxhi/redvox-api900-python-reader/src/master/docs/v1.5.0/redvox-api900-docs.md for SDK documentation.

### Changelog

#### 1.5.0 (2019-3-11)

* Add setters for all fields
* Add the ability to easily create sensor channels and RedVox packets
* Add CLI that
  * Converts .rdvxz files to .json files
  * Displays the contents of .rdvxz files

#### 1.4.1 (2019-2-15)

* Update required libraries
* Add ability to get original compressed buffer from WrappedRedvoxPacket
* Add utility functions for LZ4 compression

##### v1.4.0 (2018-12-5)

* Added support for serializing to/from JSON
* Fixed bug where has_time_synchronization_channel() would return true even if the payload was empty