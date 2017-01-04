# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hardsubhWnd.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import base64
import json
import os
import sys

import pysrt as pysrt
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QDialog

from modules.MainWindowUI import Ui_MainWindow
from modules.SubtitleTableModel import SubtitleTableModel

from modules.SubtitleWindowUI import Ui_SubtitleDialog
from modules.qt_videoframe import QtCapture

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class SubtitleApp(QtGui.QDialog, Ui_SubtitleDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent=parent)
        Ui_SubtitleDialog.__init__(self)
        self.setupUi(self)
        self.btn_save.clicked.connect(self.save_subtitles)
        self.btn_concatenate.clicked.connect(self.concatenate_subtitle)
        self.btn_delete.clicked.connect(self.delete_subtitle)

        # Variables scope
        self.output_srt = None

    def open_subtitle(self, subtitle_file):
        """

        :return:
        """
        self.subtitle_file = subtitle_file
        subs = pysrt.open(self.subtitle_file)
        self.sub_data = subs
        self.table_model = SubtitleTableModel(self.sub_data, headers=['idx', 'Time codes', 'Subtitle Text'])
        self.table_subtitles.setModel(self.table_model)

    def save_subtitles(self):
        """

        :param file_name:
        :return:
        """
        if not self.output_srt:
            fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save srt', '/home/saad/',
                                                         selectedFilter='*.srt')

            if str(fileName):
                self.output_srt = fileName

        if self.output_srt:
            self.sub_data.save(path=self.output_srt, encoding='utf-8')

    def concatenate_subtitle(self):
        """

        :return:
        """
        selected_subs = self.table_subtitles.selectedIndexes()
        rows = [sub.row() for idx, sub in enumerate(selected_subs) if idx % 3 == 0]
        rows = sorted(rows)
        self.sub_data[rows[0]].end = self.sub_data[rows[-1]].end
        del self.sub_data[rows[1]:rows[-1] + 1]

    def delete_subtitle(self):
        """

        :return:
        """
        selected_subs = self.table_subtitles.selectedIndexes()
        rows = [sub.row() for idx, sub in enumerate(selected_subs) if idx % 3 == 0]
        del self.sub_data[rows[0]:rows[-1]+1]


class MainApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.initialize_components()

        """
        Code Start
        """

    def initialize_components(self):
        """
        Initialize Components and add event handlers
        :return:
        """

        self.actionExit.triggered.connect(QtGui.qApp.quit)
        self.actionOpen.triggered.connect(self.btn_click_open)
        self.actionSave_Profile.triggered.connect(self.action_save_profile)
        self.actionLoad_Profile.triggered.connect(self.action_load_profile)
        self.actionOpen_SRT_file.triggered.connect(self.action_load_subtitle)
        self.actionAuto_Tesseract.triggered.connect(self.auto_tesseract_changed)
        self.wordspace_checkbox.stateChanged.connect(self.wordspace_checkbox_changed)
        self.autotranslate_checkbox.stateChanged.connect(self.checkbox_autotranslate_changed)
        self.actionSet_Output_SRT.triggered.connect(self.btn_click_set_output_srt)
        self.spin_height.valueChanged.connect(self.spin_changed_rect)
        self.spin_xoffset.valueChanged.connect(self.spin_changed_rect)
        self.spin_lines.valueChanged.connect(self.spin_changed_rect)
        self.spin_yoffset.valueChanged.connect(self.spin_changed_rect)
        self.spin_line_distance.valueChanged.connect(self.spin_changed_rect)
        self.spin_space_cond.valueChanged.connect(self.wordspace_checkbox_changed)
        self.spin_space.valueChanged.connect(self.wordspace_checkbox_changed)
        self.threshold_slider.valueChanged.connect(self.pre_processing_attrs_changed)
        self.fill_threshold_slider.valueChanged.connect(self.post_process_attrs_update)
        self.next_frame_btn.clicked.connect(self.next_frame)
        self.restart_btn.clicked.connect(self.play_again)
        self.btn_run.clicked.connect(self.run_simulation)
        self.btn_stop.clicked.connect(self.stop_simulation)
        self.actionExport_Post_Processing_Image.triggered.connect(self.export_pp_image)
        self.btn_tesseract.clicked.connect(self.ocr_tessract)
        self.btn_use_google.clicked.connect(self.translate_via_google)
        self.btn_use_microsoft.clicked.connect(self.translate_via_microsoft)
        self.OK_btn.clicked.connect(self.OK_btn_clicked)
        self.actionSubtitle_Window.triggered.connect(self.open_subtitle_dialoge)

        self.subtitle_dialoge = SubtitleApp(self)
        self.subtitle_dialoge.table_subtitles.doubleClicked.connect(self.subtitle_clicked)

        self.capture = None
        self.output_srt = None

    def closeEvent(self, QCloseEvent):
        self.subtitle_dialoge.close()

    def open_subtitle_dialoge(self):
        self.subtitle_dialoge.show()

    def subtitle_clicked(self):
        selected_row = self.subtitle_dialoge.table_subtitles.selectedIndexes()[0].row()
        subtitle = self.subtitle_dialoge.sub_data[selected_row]
        # Time in miliseconds
        _time = subtitle.start.hours * 60 * 60 * 1000 + subtitle.start.minutes * 60 * 1000 + subtitle.start.seconds * 1000 + subtitle.start.milliseconds
        self.capture.seek_video(_time, subtitle.text)

    def btn_click_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            '/home/saad/videos/', "Media files (*.jpg *.png *.mp4 *.avi)")

        # # # TODO: remove this
        # fname = '/home/saad/Videos/Kiralik Ask Episode 4.MP4'

        self.setWindowTitle(os.path.basename(str(fname)))

        if str(fname):
            self.capture = QtCapture(fname)
            self.capture.reference_components(video_frame=self.label, pre_processing_frame=self.pre_processing_frame,
                                              post_processing_frame=self.post_processing_frame,
                                              guess_label=self.guess_by_tesseract,
                                              google_label=self.label_google,
                                              microsoft_label=self.label_microsoft,
                                              hWnd_subtitle=self.subtitle_dialoge,
                                              hWnd_main=self)
            self.pre_processing_attrs_changed()
            self.post_process_attrs_update()
            self.spin_changed_rect()
            self.wordspace_checkbox_changed()
            self.checkbox_autotranslate_changed()
            self.auto_tesseract_changed()
            self.capture.start()

    def wordspace_checkbox_changed(self):
        if not self.capture:
            return

        self.capture.wordspace_checked(self.wordspace_checkbox.isChecked(), self.spin_space.value(),
                                       self.spin_space_cond.value())

    def btn_click_set_output_srt(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save srt', '/home/saad/Videos',
                                                     selectedFilter='*.srt')
        if str(fileName):
            self.subtitle_dialoge.output_srt = fileName
            # If there is no file, create it...Otherwise load it..
            if not os.path.isfile(fileName):
                with open(fileName, mode='w'):
                    pass
            self.subtitle_dialoge.open_subtitle(fileName)
            self.update_srt_data()

    def update_srt_data(self):
        self.capture.update_srt_data(self.subtitle_dialoge.sub_data)

    def spin_changed_rect(self):
        if not self.capture:
            return
        self.capture.set_rect(self.spin_yoffset.value(), self.spin_xoffset.value(), self.spin_height.value(),
                              self.spin_lines.value(), self.spin_line_distance.value())

    def pre_processing_attrs_changed(self):
        self.thresold_slider_label.setText(str(self.threshold_slider.value()))
        self.fill_threshold_slider.setMaximum(self.threshold_slider.value())
        self.post_process_checkbox.setText('Post-Processing (0-{})'.format(self.threshold_slider.value()))
        if not self.capture:
            return
        self.capture.set_pre_processing_attrs(self.threshold_slider.value(), self.spin_min_pixels.value())

    def post_process_attrs_update(self):
        self.capture.set_post_processing_attrs(self.fill_threshold_slider.value(), self.post_process_checkbox.isChecked())

    def next_frame(self):
        self.capture.next_frame()

    def play_again(self):
        self.capture.play_again()

    def run_simulation(self):
        self.capture.run_simulation()

    def stop_simulation(self):
        self.capture.stop_simulation()

    def export_pp_image(self):
        self.capture.export_pp_image()

    def ocr_tessract(self):
        self.capture.ocr_tessract()

    def OK_btn_clicked(self):
        self.capture.commit_subtitle()

    def checkbox_autotranslate_changed(self):
        self.capture.auto_translate(self.autotranslate_checkbox.isChecked())

    def action_save_profile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, 'Save Profile', '/home/saad/',
                                                     selectedFilter='*.hde')

        if str(fileName).strip():
            data = {
                'height_value': self.spin_height.value(),
                'yoffset_value': self.spin_yoffset.value(),
                'xoffset_value': self.spin_xoffset.value(),
                'line_distance_value': self.spin_line_distance.value(),
                'min_pixels': self.spin_min_pixels.value(),
                'post_processing_check': self.post_process_checkbox.isChecked(),
                'post_processing_value': self.fill_threshold_slider.value(),
                'auto_tesseract': self.actionAuto_Tesseract.isChecked(),
                'pre_processing_value': self.threshold_slider.value(),
                'auto_translate': self.autotranslate_checkbox.isChecked(),
                'space_value': self.spin_space.value(),
                'space_value_cond': self.spin_space_cond.value(),
                'word_spacing_check': self.wordspace_checkbox.isChecked(),
                'lines_value': self.spin_lines.value()
            }
            with open(fileName, 'w') as output_file:
                output_file.write(base64.encodestring(json.dumps(data)))

    def action_load_profile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Profile',
                                            '/home/saad/Videos', "Profile files (*.hde)")
        # fname = '/home/saad/Videos/KA_Ep_4.hde'
        if str(fname).strip():
            try:
                with open(fname) as input_file:
                    data = json.loads(base64.decodestring(input_file.read()))
                    self.spin_lines.setValue(data['lines_value'])
                    self.spin_line_distance.setValue(data['line_distance_value'])
                    self.spin_xoffset.setValue(data['xoffset_value'])
                    self.spin_yoffset.setValue(data['yoffset_value'])
                    self.spin_height.setValue(data['height_value'])
                    self.spin_min_pixels.setValue(data['min_pixels'])
                    self.spin_space.setValue(data['space_value'])
                    self.spin_space_cond.setValue(data['space_value_cond'])
                    self.wordspace_checkbox.setChecked(data['word_spacing_check'])
                    self.post_process_checkbox.setChecked(data['post_processing_check'])
                    self.actionAuto_Tesseract.setChecked(data['auto_tesseract'])
                    self.fill_threshold_slider.setValue(data['post_processing_value'])
                    self.threshold_slider.setValue(data['pre_processing_value'])

                    # Update
                    self.spin_changed_rect()
                    self.pre_processing_attrs_changed()
                    self.post_process_attrs_update()
                    self.wordspace_checkbox_changed()
                    self.checkbox_autotranslate_changed()
                    self.auto_tesseract_changed()
            except Exception as e:
                print e.message

    def action_load_subtitle(self):
        fname = QFileDialog.getOpenFileName(self, 'Open Profile',
                                            '/home/saad/Videos/', "Profile files (*.srt)")

        if str(fname).strip():
            self.subtitle_dialoge.open_subtitle(fname)

    def auto_tesseract_changed(self):
        self.capture.auto_tesseract_checked(self.actionAuto_Tesseract.isChecked())

    def translate_via_google(self):
        self.capture.translate_via_google()

    def translate_via_microsoft(self):
        self.capture.translate_via_microsoft()


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
