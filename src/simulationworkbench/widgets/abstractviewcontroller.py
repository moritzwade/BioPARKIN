from collections import OrderedDict
import logging
from PySide.QtCore import SIGNAL, Slot, Qt
#from basics.widgets.selectabletableheader import SelectableTableHeader
from PySide.QtGui import QTableView, QWidget
from basics.widgets.selectabletableheader import SelectableTableHeader
from simulationworkbench.datasourcestablemodel import DataSourcesTableModel
from services.dataservice import DataService


__author__ = 'bzfwadem'

class AbstractViewController(QWidget):
    '''
    Provides a base class for the individual data views (plot/table/sensitiviy table).
    Each of the views can have its own UI. This class here is just a set of common methods.
    '''

    def __init__(self, parent):
        super(AbstractViewController, self).__init__(parent)
    #        self.dataView = None

    def _initialize(self):
        self.dataService = DataService()
        self.experimentalData = None
        self.simulationData = None
        self.dataSourceTableModel = None
#        self.dataSourceTableView = QTableView(None)
#        self.DataIndexToDataID = {}
        self.dataSourceIDs = []
        self.allData = None
        self.dataSources = None

    def updateDataSources(self, dataSources, dataID=None):
        '''

        Gets the data files that were produced by the last integration run
        and invokes updating the data source table and the data tabs (plot/table).

        The data structure for the data model is a dict:
        {'source ID': [list of data IDs, e.g. GnrH, ...]}
        '''
        self.dataSources = dataSources
        if not self.dataSources:
            logging.info("No data sources, nothing to be shown.")
            return
            
        logging.debug("Updating data sources...")

        #        dataSources = self.dataService.get_data_sources_with_dataIDs()
        #dataSources = self.dataService.get_all_data()

        self.dataSourceIDs = []

        if type(self.dataSources) is list:
            try:
                combinedDataSource = OrderedDict()
                for source in self.dataSources:
                    for key, value in source.items():
                        if not value.isSelected():
                            continue
                        origin = value.getId()
                        if not origin in self.dataSourceIDs:
                            self.dataSourceIDs.append(origin)

                        if key in combinedDataSource:
                            logging.debug("AbstractViewController: Duplicate key encountered while merging data sources for display.")
                        combinedDataSource[key] = value
                self.dataSources = combinedDataSource
            except:
                logging.error("AbstractViewController: Could not combine several datasource dictionaries into one.")

        if dataID:
            singledataSource = OrderedDict()
            singledataSource[dataID] = self.dataSources[dataID]
            self.dataSources = singledataSource

        if self.dataSourceTableModel:
            self.dataSourceTableModel.dataChanged.disconnect(self.on_dataSourcesChanged)

        self.dataSourceTableModel = DataSourcesTableModel(self.dataSources)
        self.dataSourceTableView.setModel(self.dataSourceTableModel)

        # use header with checkboxes
        selectableTableHeaderHorizontal = SelectableTableHeader(Qt.Horizontal, self.dataSourceTableView)
        selectableTableHeaderHorizontal.setNonSelectableIndexes([0])
        selectableTableHeaderHorizontal.sectionSelectionChanged.connect(self.on_columnSelectionChanged)
        selectableTableHeaderHorizontal.connectSelectionModel(self.dataSourceTableModel)
        self.dataSourceTableView.setHorizontalHeader(selectableTableHeaderHorizontal)

        selectableTableHeaderVertical = SelectableTableHeader(Qt.Vertical, self.dataSourceTableView)
        selectableTableHeaderVertical.sectionSelectionChanged.connect(self.on_rowSelectionChanged)
        selectableTableHeaderVertical.connectSelectionModel(self.dataSourceTableModel)
        self.dataSourceTableView.setVerticalHeader(selectableTableHeaderVertical)

        self.dataSourceTableView.resizeColumnsToContents()

#        self.connect(self.dataSourceTableModel, SIGNAL("dataChanged(QModelIndex, QModelIndex)"),
#                     self.on_dataSourcesChanged)
        self.dataSourceTableModel.dataChanged.connect(self.on_dataSourcesChanged)

        self.on_dataSourcesChanged(None, None)


    def on_dataSourcesChanged(self, upperLeftIndex, lowerRightIndex):
    #        if upperLeftIndex != lowerRightIndex:
    #            logging.debug("Updating ranges of changes in the sources table is currently unsupported.")

        # for now, we disregard lowerRightIndex
        self._updateDataView() # update everything

    def getNumberOfDataItems(self):
        if self.dataSourceTableModel:
            return self.dataSourceTableModel.getNumberOfDataItems()

    def getEntityIDs(self):
        if self.dataSourceTableModel:
            return self.dataSourceTableModel.getEntityIDs()



    def getSourceIDs(self):
        if self.dataSourceTableModel:
            return self.dataSourceTableModel.getSourceIDs()

    def getSelectedCombinations(self):
        if self.dataSourceTableModel:
            return self.dataSourceTableModel.getSelectedCombinations()

    def hasData(self, dataSet):
        if not self.dataSources:
            return False
        return True if dataSet in self.dataSources.values() else False


    def _updateDataView(self):
        if not self.dataSourceTableModel:
            return
        
        selectedData = self._getSelectedData()
        if not selectedData:
            logging.info("No data, nothing to be shown.")
            self._clearView()
            return

        self._updateView(selectedData)
        #self._updateDataTable(data)    # TODO

        # does not (yet) use the selected data
        #self._updateSensitiviesTable() # TODO


    def _getSelectedData(self):
        #return self.dataService.get_simulation_data()

        #        allSimulationData = self.dataService.get_simulation_data()
        #        allExperimentalData = self.dataService.get_experimental_data()
#        self.DataIndexToDataID = {}
        if not self.allData:    # only get actual data the first time
            self.allData = self.dataService.get_all_data()

        selectedIDs = self.dataSourceTableModel.getSelectedIDs() # this returns a dict {ID: ("Simulation", "filename1", ...)}
        selectedData = {}
        for i, (selectedID, sources) in enumerate(selectedIDs.items()):
#            self.DataIndexToDataID[i] = selectedID
#            self.DataIndexToDataID[selectedID] = i
            for source in sources:
                #if source == services.dataservice.SIMULATION:
                if not self.allData.has_key(source):
                    continue
                dataOfSource = self.allData[source]
                #dataOfID = dataOfSource[selectedID]
                dataOfID = dataOfSource.getData(selectedID)
                if not dataOfID:
                    continue
                if selectedID in selectedData:
                    selectedData[selectedID].append(dataOfID)
                else:
                    selectedData[selectedID] = [dataOfID]

        return selectedData


    def _updateView(self, data):
        """
        Needs to be overridden.

        Should update the data view (plot, table, ...).
        """
        logging.debug("The _updateView method has not been overridden.")

    def _clearView(self):
        """
        Needs to be overridden.

        Should clear the data view (plot, table, ...).
        """
        logging.debug("The _clearView method has not been overridden.")

    def _selectAllSources(self, doSelect, column=None, row=None):
        if self.dataSourceTableModel:
            self.dataSourceTableModel.selectAllSources(doSelect, column, row)


    def _invertSourceSelection(self):
        if self.dataSourceTableModel:
            self.dataSourceTableModel.invertSelection()


    @Slot("")
    def on_actionSave_triggered(self):
        '''
        Needs to be overriden.

        Should show a dialog to save the currently shown data (table, plot, ...).
        '''
        logging.debug("The on_actionSave_triggered method has not been overridden.")


    @Slot("")
    def on_actionSelectAll_triggered(self):
        """
        Selects all sources.

        NOTE: Repeat this method in the actual class implementation!
        The self.setupUi() in the actual class doesn't seem to be able
        to wire the base classe (this class). This worked in PyQT but
        doesn't work in PySide.
        """
        self._selectAllSources(True)

    @Slot("")
    def on_actionDeselectAll_triggered(self):
        """
        Deselects all sources.

        NOTE: Repeat this method in the actual class implementation!
        The self.setupUi() in the actual class doesn't seem to be able
        to wire the base classe (this class). This worked in PyQT but
        doesn't work in PySide.
        """
        self._selectAllSources(False)

    @Slot("")
    def on_actionInvertSelection_triggered(self):
        """
        Inverts the current source selection.

        NOTE: Repeat this method in the actual class implementation!
        The self.setupUi() in the actual class doesn't seem to be able
        to wire the base classe (this class). This worked in PyQT but
        doesn't work in PySide.
        """
        self._invertSourceSelection()

    def on_columnSelectionChanged(self, index, selectionState):
        if selectionState == Qt.Checked:
            selected = True
        elif selectionState == Qt.Unchecked:
            selected = False
        else:   # selection is Qt.PartiallyChecked -> no update of selections here
            return
        self._selectAllSources(selected, column=index)

    def on_rowSelectionChanged(self, index, selectionState):
        if selectionState == Qt.Checked:
            selected = True
        elif selectionState == Qt.Unchecked:
            selected = False
        else:   # selection is Qt.PartiallyChecked -> no update of selections here
            return
        self._selectAllSources(selected, row=index)

#    def closeEvent(self, *args, **kwargs):
#        if self.dataService: #should always be the case at this point
#            for dataSet in self.allData.values():
#                self.dataService.remove_data(dataSet)
#        QWidget.closeEvent(self, *args, **kwargs)

