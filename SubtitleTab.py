import os

import pysrt
from PyQt4 import QtGui

from SubMergeUI import _fromUtf8, _translate
from SubtitleTableModel import SubtitleTableModel


class SubtitleTabHelper(object):
    """

    """
    def __init__(self, tab_widget):
        """

        :return:
        """
        self.tab_widget = tab_widget
        self.tabs = []

    def _add_tab(self, tab):
        """

        :param tab:
        :return:
        """
        self.tab_widget.addTab(tab, _fromUtf8(""))

    def remove_tab(self, tabIndex):
        """
        Remove tab from tab list.
        :param tabIndex:
        :return:
        """
        self.tabs.remove(str(self.tab_widget.tabText(tabIndex)))
        self.tab_widget.removeTab(tabIndex)

    def create_tab_from_file(self, sub_filename):
        """
        Create a subtitle tab using srt file
        :param sub_filename:
        :return:
        """
        # Get name of subtitle for tab title
        name = os.path.basename(os.path.splitext(unicode(sub_filename))[0])

        try:
            subs = pysrt.open(unicode(sub_filename))
        except Exception as e:
            print e.message
            subs = pysrt.open(unicode(sub_filename), encoding='latin')
        return self.create_tab(name, subs)

    def create_tab(self, name, sub_data):
        """
        Create a widget and add it in tab container

        :param name: name of subtitle file
        :param sub_data:
        :return:
        """

        tab = QtGui.QWidget()
        tab.setObjectName(_fromUtf8(name))
        verticalLayout = QtGui.QVBoxLayout(tab)
        verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        tableSubtitle = QtGui.QTableView(tab)
        tableSubtitle.setObjectName(_fromUtf8("tableWidget"))
        tableSubtitle.horizontalHeader().setStretchLastSection(True)
        tableSubtitle.verticalHeader().setVisible(False)
        tableSubtitle.horizontalHeader().setCascadingSectionResizes(True)
        tableSubtitle.horizontalHeader().setDefaultSectionSize(200)
        tableSubtitle.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        tableSubtitle.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        tableSubtitle.setStyleSheet(_fromUtf8("background-color: rgb(61, 61, 61);\n"
                                                   "selection-color: rgb(245, 245, 245);\n"
                                                   "selection-background-color: rgb(135, 167, 82);\n"
                                                   "font: 10pt Saab;\n"
                                                   "color: rgb(245, 245, 245);"))

        tableSubtitle.horizontalHeader().setStyleSheet("::section{background-color: rgb(121, 121, 121);}")
        tableSubtitle.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        verticalLayout.addWidget(tableSubtitle)
        self._add_tab(tab)

        # If a tab name already exist then append the name string with (0), (1), (2) ... tab (1), tab (2), tab (3)
        _name = name
        if _name in self.tabs:
            _format = '%s ({})' % _name
            index = 1
            while _format.format(index) in self.tabs:
                index += 1
            _name = _format.format(index)

        self.tabs.append(_name)
        self.tab_widget.setTabText(self.tab_widget.indexOf(tab), _translate("MainWindow", _name, None))

        table_model = SubtitleTableModel(sub_data, headers=['idx', 'Time codes', 'Subtitle Text'])
        tableSubtitle.setModel(table_model)

        return tab

    def get_selected_table(self):
        """

        :return:
        """
        current_tab = self.tab_widget.currentWidget()
        if not current_tab:
            return None
        return current_tab.findChildren(QtGui.QTableView)[0]

    def get_tabs(self, _filter=None):
        """
        Return all tabs if filter is none, otherwise return tabs whose name are in filter tuple
        :param _filter:
        :return:
        """
        count = self.tab_widget.count()

        # Filter tabs model with w.r.t. name otherwise return all tabs
        if _filter:
            return [self.tab_widget.widget(idx).findChildren(QtGui.QTableView)[0] for idx in xrange(0, count)
                    if self.tab_widget.tabText(idx) in _filter]
        return [self.tab_widget.widget(idx).findChildren(QtGui.QTableView)[0] for idx in xrange(0, count)]
