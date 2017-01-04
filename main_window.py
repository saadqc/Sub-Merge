# -*- coding: utf-8 -*-


"""

Main Window app to render and execute user actions.

Author: Saad Abdullah
Email: saad_lah@hotmail.com
       saadfast.qc@gmail.com

This file is part of Sub-Merge app.

Sub-Merge is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sub-Merge is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

import copy
import os

from pysrt import SubRipTime
from PyQt4 import QtCore, QtGui

import sys

from PyQt4.QtGui import QStandardItemModel, QStandardItem, QMessageBox

from ConcatenateDialoge import Ui_ConcatenateDialog
from Messenger import Messenger
from SubMergeUI import Ui_MainWindow
from SubtitleTab import SubtitleTabHelper
from VideoPlayer import Player

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ConcatenateDialog(QtGui.QDialog, Ui_ConcatenateDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        Ui_ConcatenateDialog.__init__(self)
        self.setupUi(self)


class MainApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Update UI
        self.menubar.setStyleSheet("QMenuBar::item { background-color: rgb(77, 77, 77); }")
        self.subtitleTabs.setStyleSheet("QTabBar::item { background-color: rgb(77, 77, 77); }")
        styles = [x for x in QtGui.QStyleFactory.keys()]
        QtGui.qApp.setStyle(str(styles[-1]))

        self.initialize_components()

        """
        Code Start
        """

    def initialize_components(self):
        """
        Initialize Components and add event handlers
        :return:
        """

        self.actionOpen_Video.triggered.connect(self.open_media)
        self.actionOpen_Subtitle.triggered.connect(self.open_subtitle)
        self.actionConcatenate.triggered.connect(self.concatenate_tabs)
        self.actionDelete.triggered.connect(self.delete_subtitles)
        self.actionBreak_Selected_Subtitles.triggered.connect(self.create_subtitles)
        self.actionSet_to_Current_Position.triggered.connect(self.set_to_current_video_position)
        # self.actionSave.triggered.connect(self.save_subtitle)
        self.actionSave_As.triggered.connect(self.save_subtitle_as)
        self.actionAbout.triggered.connect(self.about_message)
        self.actionExit.triggered.connect(self.exit_app)

        self.tab_helper = SubtitleTabHelper(self.subtitleTabs)
        self.subtitleTabs.tabCloseRequested.connect(self.on_tab_close)

        self.filename = None
        self.player = None
        self.current_subtitle_data = None
        self.timer = None

        Messenger.main_window = self

    def exit_app(self):
        """
        Close app
        :return:
        """
        self.close()

    def closeEvent(self, QCloseEvent):
        """
        Release vlc resources
        :param QCloseEvent:
        :return:
        """

        if self.player:
            self.player.close()
            self.player = None

    def open_media(self):
        """
        Open media file in vlc player
        :return:
        """
        self.filename = QtGui.QFileDialog.getOpenFileName(self, "Open Media File", os.path.expanduser('~'),
                                                          "Media files (*.mp4 *.mp3 *.avi *.MP4 *.mkv *.flv)")
        if not self.filename:
            return

        if self.player:
            self.player.close()
            self.player = None

        self.player = Player()
        self.player.OpenFile(self.filename)

        Messenger.media_player = self.player

        _size = self.player.getVideoSize()

        self.player.resize(*_size)
        self.player.show()

        # Reset volume to zero
        self.player.setVolume(0)

        self.update_subtitle_view()

        if self.timer:
           self.timer.stop()
           self.timer = None

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_subtitle_selection)
        self.timer.start(50)

    def open_subtitle(self):
        """
        Open subtitle file in a tab
        :return:
        """
        sub_filename = QtGui.QFileDialog.getOpenFileName(self, "Open Subtitle File", os.path.expanduser('~'),
                                                         "SubRip files (*.srt)")
        if not sub_filename:
            return
        tab = self.tab_helper.create_tab_from_file(sub_filename)
        tab.findChild(QtGui.QTableView).doubleClicked.connect(self.on_subtitle_select)

    def save_subtitle(self):
        """
        Save subtitle to file
        :return:
        """
        pass

    def save_subtitle_as(self):
        """
        Save subtitle to file and enforce save dialog
        :return:
        """
        table = self.tab_helper.get_selected_table()

        if not table:
            return

        sub_data = table.model().get_data()
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save srt', os.path.expanduser('~'),
                                                     selectedFilter='*.srt')

        if not fileName:
            return

        sub_data.save(fileName)

    def about_message(self):
        """
        Show about message box of developer
        :return:
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This app is developed by Saad Abdullah. In case of any queries, please send an email to saad_lah@hotmail.com.")
        msg.setWindowTitle("Developer!")
        msg.exec_()

    def on_subtitle_select(self, index):
        """
        On subtitle select, set video time to subtitle
        :return:
        """
        row = index.row()
        sub_item = self.tab_helper.get_selected_table().model().get_data()[row]
        _time = sub_item.start

        if self.player:
            self.player.setTime(_time.ordinal)

    def on_tab_close(self, index):
        """
        Event handler..remove tab on tab close
        :param index:
        :return:
        """
        self.tab_helper.remove_tab(index)

    def concatenate_tabs(self):
        """
        Concatenate two or more tabs and create another tab as a combination
        :return:
        """
        dialoge = ConcatenateDialog(self)
        dialoge.accepted.connect(self.concatenate_tabs_ok)
        model = QStandardItemModel(dialoge.listView)
        [model.appendRow(QStandardItem(_entry)) for _entry in self.tab_helper.tabs]
        dialoge.listView.setModel(model)
        dialoge.show()
        self.concatenate_listview = dialoge.listView

    def concatenate_tabs_ok(self):
        """
        Event handler after user presses OK in concatenate dialog. Concatenate those tab and generate a new tab
        :return:
        """
        selected_indexes = sorted(list(set([index.row() for index in self.concatenate_listview.selectedIndexes()])))
        if len(selected_indexes) >= 2:
            tab_names = [item for idx, item in enumerate(self.tab_helper.tabs) if idx in selected_indexes]
            table_views = self.tab_helper.get_tabs(_filter=tab_names)
            sub_data = [table_view.model().get_data() for table_view in table_views]
            sub_data = copy.deepcopy(sum(sub_data, []))
            sub_data = sorted(sub_data, key=lambda x: x.start)

            # Re-index all subtitles
            _index = 1
            for idx, item in enumerate(sub_data):
                item.index = _index
                _index += 1

            self.tab_helper.create_tab('output', sub_data)

    def create_subtitles(self):
        """
        Create subtitles tab from selected subtitles
        :return:
        """
        table = self.tab_helper.get_selected_table()
        if not table:
            return None
        selected_indexes = sorted(list(set([index.row() for index in table.selectedIndexes()])))

        if len(selected_indexes) >= 2:
            sub_data = table.model().get_data()[selected_indexes[0]:selected_indexes[-1]+1]
            self.tab_helper.create_tab('output', sub_data)

    def delete_subtitles(self):
        """
        Delete selected subtitles rows in a tab
        :return:
        """
        table = self.tab_helper.get_selected_table()
        if not table:
            return None
        selected_indexes = sorted(list(set([index.row() for index in table.selectedIndexes()])))

        if selected_indexes:
            table.model().removeRows(selected_indexes[0], len(selected_indexes))

    def set_to_current_video_position(self):
        """
        Set the current selected subtitles to current video location
        :return:
        """
        table = self.tab_helper.get_selected_table()
        if not table or not self.player:
            return None
        selected_indexes = sorted(list(set([index.row() for index in table.selectedIndexes()])))

        if len(selected_indexes) >= 1:
            sub_data = table.model().get_data()[selected_indexes[0]:selected_indexes[-1] + 1]
            current_video_time = SubRipTime.coerce(int(self.player.getPosition()))

            # Find delta between current video time and current selected subtitle time. Then add delta to all subtitle
            # start and end
            delta = current_video_time - sub_data[0].start
            for item in sub_data:
                item.start = item.start + delta
                item.end = item.end + delta

            self.update_subtitle_view()

    def update_subtitle_view(self):
        """

        :return:
        """
        table = self.tab_helper.get_selected_table()
        if not self.player or not table:
            return
        self.current_subtitle_data = table.model().get_data()
        self.current_subtitle_data = sorted(self.current_subtitle_data, key=lambda x: x.start)
        media_position = self.player.getPosition()
        _time = SubRipTime.coerce(media_position)
        indicies = [idx for idx, item in enumerate(self.current_subtitle_data) if item.start <= _time <= item.end]
        self.current_idx = indicies[0] if indicies else None

    def update_subtitle_selection(self):
        """
        Set the subtitle selection to current video time.
        :return:
        """
        table = self.tab_helper.get_selected_table()
        if not self.player or not table:
            return

        media_position = self.player.getPosition()
        _time = SubRipTime.coerce(media_position)

        if not self.current_idx:
            self.update_subtitle_view()
            return

        item = self.current_subtitle_data[self.current_idx]
        if item.start <= _time <= item.end:
            table.selectRow(self.current_idx)
        elif item.end < _time:
            self.current_idx += 1


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
