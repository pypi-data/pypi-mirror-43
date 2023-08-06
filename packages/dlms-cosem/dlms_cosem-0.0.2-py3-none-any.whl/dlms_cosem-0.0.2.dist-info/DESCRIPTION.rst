==========
dlms-cosem
==========

A Python library for DLMS/COSEM.


We are developing this library as an ongoing project to support DLMS/COSEM in
our AMR (Automatic Meter Reading) system Utilitarian.

As of now we support:

    * Receiving DataNotification via UDP.

Future Work:

    * GET, SET, ACTION over pre-established associations.
    * Interface classes implementation.
    * DLMS Client to handle communication.
    * GBT, ACCESS.
    * Establish Connections.
    * More Security options.


Tested with Italian Gas meters that are using a companion standard to DLMS. If
you notice an error using the library please raise an issue.


=========
Changelog
=========

The format is based on `Keep a Changelog: https://keepachangelog.com/en/1.0.0/`,
and this project adheres to `Semantic Versioning: https://semver.org/spec/v2.0.0.html`

Unreleased
----------

Added
^^^^^

Changed
^^^^^^^

Deprecated
^^^^^^^^^^

Removed
^^^^^^^

Fixed
^^^^^

Security
^^^^^^^^


v0.0.2
------

Changed
^^^^^^^
-   UDP messages are now based WrapperProtocolDataUnit to be able to reuse
    WrapperHeader for TCP messages.
-   Parsing of DLMS APDUs


v0.0.1
------

Initial implementation.


