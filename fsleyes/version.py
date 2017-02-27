#!/usr/bin/env python
#
# version.py - FSLeyes version information.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""The sole purpose of this module is as a container for the *FSLeyes*
version number and information.

.. autosummary::

   __version__
   __vcs_version__
"""


__version__ = '0.9.13'
"""Current version number, as a string. The FSLeyes version number consists
of three numbers, separated by a period:

 1. The major release number. This gets updated for major releases.
 2. The minor release number. This gets updated for minor releases.
 3. The point release number. This gets updated for all other changes.

The point release number may optionally end with a single lower-case
alphabetical character (e.g. 'a'), whcih implies that the version is a
hot-fix release.
"""


__vcs_version__ = 'dev'
"""VCS (Version Control System) version number, for internal use. """


def parseVersionString(versionString):
    """Parses the given version string, and returns a tuple containing
    the individual components of the version number (see the description
    of the :attr:`__version__` attribute).

    An error is raised if the ``versionString`` is invalid.
    """

    components = versionString.split('.')

    # Major and minor version are always numeric,
    # but the point release might contain an 
    # alphabetical character implying a hotfix
    # release.
    major, minor = map(int, components[:2])
    point        = components[2]

    # The final component is a number which
    # may end with a single alpha character.
    # If present, the hotfix release gets
    # converted into a number.
    if point.isdigit():
        hotfix = 0
        point  = int(point)
    else:
        hotfix = ord(point[ -1])
        point  = int(point[:-1])

    return major, minor, point, hotfix


def compareVersions(v1, v2):
    """Compares the given FSLeyes version numbers.

    :returns: One of the following:

                - -1 if ``v1`` < ``v2`` (i.e. ``v1`` is older than ``v2``)
                -  0 if ``v1`` == ``v2``
                -  0 if ``v1`` > ``v2``
    """

    v1 = parseVersionString(v1)
    v2 = parseVersionString(v2)

    for p1, p2 in zip(v1, v2):

        if p1 > p2: return  1
        if p1 < p2: return -1

    return 0
