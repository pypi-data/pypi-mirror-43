v0.1.1 (2019-03-25)
======================

- Build SailfishOS RPM package for Python 3.7

v0.1.0 (2019-02-21)
======================

- Update documentation and indicate that we're out of the alpha phase

v0.0.11 (2018-11-22)
======================

- Make using CacheControl possible to cache public API requests
- Fix bug when uploading new box removed the description
- Use Black code format and ensure PEP8 conformity

v0.0.10 (2018-10-12)
======================

- Fix bug not adding the account itself to a new uploaded box

v0.0.9 (2018-10-11)
======================

- Fix bug with the interfering caches of equal accounts on different APIs
- add possibility to clear the whole cache

v0.0.8 (2018-10-10)
======================

- add class for applications using sensemapi

v0.0.7 (2018-09-28)
======================

- implement cache for authentication
- implement transparent handling of both email and username
- fix bug with setting location when retrieving a box
- add uploading multiple sensor measurement of a senseBox at once

v0.0.6 (2018-09-19)
======================

- drop iso8601 dependency
- make pandas an optional dependency
- add changelog to the RPM package

v0.0.5 (2018-09-15)
======================

- handle HTTP 429 "Too Many Requests"-errors by waiting and retrying
- fix a bug in uploading a sensor measurement of "0" value
- add deletion of sensor measurements

v0.0.4 (2018-08-29)
======================

- add retrieval of sensor measurement timeseries
- improve test suite

v0.0.3 (2018-08-28)
======================

- simplify deletion of a sensor from a senseBox
- update documentation

v0.0.2 (2018-08-27)
======================

- fix README Markdown rendering on PyPi

v0.0.1 (2018-08-27)
======================

- initial version with basic functionality
    - account sign in/out
    - handling authentication tokens
    - creating senseBoxes/sensors
    - uploading senseBoxes/sensors
    - modifying senseBoxes/sensors
    - posting sensor measurements
    - documentation
