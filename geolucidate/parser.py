# -*- coding: utf-8 -*-

"""
This module contains the regular expression which is used by
geolucidate to identify and extract geographic coordinates.

It is a point of some pride for the author that despite the
diversity of formats accepted by geolucidate, only a single regular
expression is needed to parse all of them.  This has, however,
resulted in a rather lengthy and complex regular expression.

"""

import re

decimal_degree_re = re.compile(r"""
    ^
    \(?
    (?P<latdir>NORTH|SOUTH|[NS-])?\s?
    (?P<latitude>([0-8][0-9]|90)(?P<latpoint>\.)?(?(latpoint)(\d+)|[^\d]))\s?
    (degrees|°)?\s?
    (?P<latdir2>NORTH|SOUTH|[NS])?
    ([\s,]+)?
    (?P<longdir>EAST|WEST|[EW-])?\s?
    (?P<longitude>((1(([0-7][0-9]|80))|(0?[0-9][0-9])))(?P<longpoint>\.)?(?(longpoint)(\d+)|[^\d]))\s?
    (degrees|°)?\s?
    (?P<longdir2>EAST|WEST|[EW])?
    \)?
    $
  """, re.VERBOSE | re.UNICODE | re.IGNORECASE)

degree_min_sec_re = re.compile(r"""
    ^
    \(?
    # Latitude direction, first position: one of N, S, NORTH, SOUTH
    (((?P<latdir>NORTH|SOUTH|[NS])\ ?)|(?P<latsign>-))?
    # Latitude degrees: two digits 0-90
    (?P<latdeg>([0-8]?[0-9])|90)
    # Optional space, degree mark, period,
    # or word separating degrees and minutes
    (\ |(?P<degmark>\ ?(º|°)\ ?|(?P<degpd>\.)|-|\ DEGREES,\ ))?
    (?P<latminsec>
    # Latitude minutes: two digits 0-59
    (?P<latmin>([0-5]?)[0-9])
    # If there was a degree mark before, look for punctuation after the minutes
    (\ |(?(degmark)('|"|\ MINUTES,?)\ ?))?
    (
    # Latitude seconds: two digits
    (
    ((?(degpd)\.?)(?P<latsec>(\d{1,2}(\.\d+)?)))|
    # Decimal fraction of minutes
    (?P<latdecsec>\.\d{1,3}))?)
    (?(degmark)("|'|\ SECONDS\ )?)
    )?
    # Latitude direction, second position, optionally preceded by a space
    \ ?(?P<latdir2>(NORTH|SOUTH|[NS]))?
    # Latitude/longitude delimiter: space, forward slash, comma, or none
    (\ ?[ /]\ ?|,\ )?
    # Longitude direction, first position: one of E, W, EAST, WEST
    ((?(latdir)((?P<longdir>EAST|WEST|[EW])\ ?))|(?P<longsign>-)?)
    # Longitude degrees: two or three digits
    (?P<longdeg>((1(([0-7][0-9]|80))|(0?[0-9][0-9]))))
    # If there was a degree mark before, look for another one here
    (\ |(?(degmark)(\ ?(º|°)\ ?|\.|-|\ DEGREES,\ )))?
    (?(latminsec)   #Only look for minutes and seconds in the longitude
    (?P<longminsec> #if they were there in the latitude
    # Longitude minutes: two digits
    (?P<longmin>([0-5]?)[0-9])
    # If there was a degree mark before, look for punctuation after the minutes
    (\ |(?(degmark)('|"|\ MINUTES,?)\ ?))?
    # Longitude seconds: two digits
    (
    ((?(degpd)\.?)(?P<longsec>(\d{1,2}(\.\d+)?)))|
    # Decimal fraction of minutes
    (?P<longdecsec>\.\d{1,3}))?)
    (?(degmark)("|'|\ SECONDS\ )?)
    )
    #Longitude direction, second position: optionally preceded by a space
    (?(latdir2)(\ ?(?P<longdir2>(EAST|WEST|[EW]))))
    \)?
    $
    """, re.VERBOSE | re.UNICODE | re.IGNORECASE)
"""The coordinate-parsing regular expression,
compiled with :func:`re.compile`"""

all_re = [
    decimal_degree_re,
    degree_min_sec_re,
]
