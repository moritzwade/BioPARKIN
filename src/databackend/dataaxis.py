from PySide.QtCore import QObject, Signal
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


    def getData(self):
        return self.__data

    def setData(self, data):
        assert isinstance(data, list)
        self.__data = data
        self.newData.emit()

    def delData(self):
        del self.__data

    data = property(getData, setData, delData, "The list of data items/values.")
    newData = Signal()

    def __init__(self, items=None, type=None):
        self.data = items
        self.meta = DataMeta() # automatically sets common meta info like CREATED, LAST_MODIFIED, etc.
        self.meta[constants.TYPE] = type

