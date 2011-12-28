from PySide.QtCore import QObject
from databackend import constants


class DataAxis(QObject):
    """
    Represents a single axis inside a (multi-dimensional) DataSet.
    This class is basically an enhanced list of items.

    It can hold timepoints as well as a list of string IDs.

    @since:2011-12-28
    @author: Moritz Wade
    @copyright: Zuse Institute Berlin, 2011
    """

    def __init__(self, items=None, type=None):
        self.data = items
        self.meta = DataMeta() # automatically sets common meta info like CREATED, LAST_MODIFIED, etc.
        self.meta[constants.TYPE] = type