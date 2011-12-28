from PySide.QtCore import QObject
import time
import datetime
from databackend import constants

class DataMeta(QObject):
    """
    Encapsulates meta information for use throughout the data backend
    by conveniently wrapping a simple dict.
    """

    def __init__(self):
        self.info = {}
        self.info[constants.META_KEYS.CREATED] = "now" #TODO...
