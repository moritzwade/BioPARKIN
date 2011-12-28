from basics.helpers.enum import enum

"""
This file defines constants (especially ENUMs) for use throughout
the data backend.

@since: 2011-12-28
@author: Moritz Wade
@copyright: Zuse Institute Berlin, 2011
"""

TYPE = "TYPE"
TYPES = enum("TYPE", "NONE, SIM_TIMELINE, MEAS_TIMELINE, SENS_OVERVIEW, SENS_DETAILS_JACOBIAN, SENS_DETAILS_SUBCONDITION, PARAMETER_IDENTIFICATION")

# fixed meta keys (used in every meta dict)
META_KEYS = enum("META", "CREATED, LAST_MODIFIED, %s" % TYPE)

