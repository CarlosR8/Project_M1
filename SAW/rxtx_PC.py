#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: GNU Spectrum Analyzer by Carlos RIVERA
# Author: cmrivera
# GNU Radio version: v3.8.5.0-5-g982205bd

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import zeromq
import epy_module_client  # embedded python module
import epy_module_sweep  # embedded python module

from gnuradio import qtgui

class rxtx_PC(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "GNU Spectrum Analyzer by Carlos RIVERA")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("GNU Spectrum Analyzer by Carlos RIVERA")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "rxtx_PC")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.sample_rate_osmosdr = sample_rate_osmosdr = 1.152e6
        self.waveform_ = waveform_ = 2
        self.vector_data = vector_data = range(512)
        self.start_freq = start_freq = 300e-3
        self.span_freq = span_freq = 0.5
        self.sample_rate_gr = sample_rate_gr = 200e3
        self.sample_rate = sample_rate = sample_rate_osmosdr
        self.record = record = "False"
        self.offset_ = offset_ = 0.5
        self.measured_frequency = measured_frequency = 434e6
        self.frequency_ = frequency_ = 10e3
        self.end_freq = end_freq = 0.5
        self.carrying_frequency = carrying_frequency = 86.8e6
        self.btn_start = btn_start = 0
        self.amplitude_ = amplitude_ = 300e-3

        ##################################################
        # Blocks
        ##################################################
        self.tab_widget_0 = Qt.QTabWidget()
        self.tab_widget_0_widget_0 = Qt.QWidget()
        self.tab_widget_0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0_widget_0)
        self.tab_widget_0_grid_layout_0 = Qt.QGridLayout()
        self.tab_widget_0_layout_0.addLayout(self.tab_widget_0_grid_layout_0)
        self.tab_widget_0.addTab(self.tab_widget_0_widget_0, 'Noise source')
        self.tab_widget_0_widget_1 = Qt.QWidget()
        self.tab_widget_0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_0_widget_1)
        self.tab_widget_0_grid_layout_1 = Qt.QGridLayout()
        self.tab_widget_0_layout_1.addLayout(self.tab_widget_0_grid_layout_1)
        self.tab_widget_0.addTab(self.tab_widget_0_widget_1, 'Frequency sweep')
        self.top_grid_layout.addWidget(self.tab_widget_0, 1, 0, 1, 4)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._measured_frequency_tool_bar = Qt.QToolBar(self)
        self._measured_frequency_tool_bar.addWidget(Qt.QLabel('Measured Frequency  ' + ": "))
        self._measured_frequency_line_edit = Qt.QLineEdit(str(self.measured_frequency))
        self._measured_frequency_tool_bar.addWidget(self._measured_frequency_line_edit)
        self._measured_frequency_line_edit.returnPressed.connect(
            lambda: self.set_measured_frequency(eng_notation.str_to_num(str(self._measured_frequency_line_edit.text()))))
        self.top_grid_layout.addWidget(self._measured_frequency_tool_bar, 7, 0, 1, 2)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://192.168.137.8:5555', 100, False, -1)
        # Create the options list
        self._waveform__options = [0, 1, 2, 3, 4, 5]
        # Create the labels list
        self._waveform__labels = ['Constant', 'Sine', 'Cosine', 'Square', 'Triangle', 'Saw Tooth']
        # Create the combo box
        self._waveform__tool_bar = Qt.QToolBar(self)
        self._waveform__tool_bar.addWidget(Qt.QLabel('Waveform                  ' + ": "))
        self._waveform__combo_box = Qt.QComboBox()
        self._waveform__tool_bar.addWidget(self._waveform__combo_box)
        for _label in self._waveform__labels: self._waveform__combo_box.addItem(_label)
        self._waveform__callback = lambda i: Qt.QMetaObject.invokeMethod(self._waveform__combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._waveform__options.index(i)))
        self._waveform__callback(self.waveform_)
        self._waveform__combo_box.currentIndexChanged.connect(
            lambda i: self.set_waveform_(self._waveform__options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._waveform__tool_bar, 4, 2, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._start_freq_tool_bar = Qt.QToolBar(self)
        self._start_freq_tool_bar.addWidget(Qt.QLabel('Start frequency' + ": "))
        self._start_freq_line_edit = Qt.QLineEdit(str(self.start_freq))
        self._start_freq_tool_bar.addWidget(self._start_freq_line_edit)
        self._start_freq_line_edit.returnPressed.connect(
            lambda: self.set_start_freq(eng_notation.str_to_num(str(self._start_freq_line_edit.text()))))
        self.tab_widget_0_grid_layout_1.addWidget(self._start_freq_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self._span_freq_tool_bar = Qt.QToolBar(self)
        self._span_freq_tool_bar.addWidget(Qt.QLabel('Span' + ": "))
        self._span_freq_line_edit = Qt.QLineEdit(str(self.span_freq))
        self._span_freq_tool_bar.addWidget(self._span_freq_line_edit)
        self._span_freq_line_edit.returnPressed.connect(
            lambda: self.set_span_freq(eng_notation.str_to_num(str(self._span_freq_line_edit.text()))))
        self.tab_widget_0_grid_layout_1.addWidget(self._span_freq_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self._sample_rate_osmosdr_tool_bar = Qt.QToolBar(self)
        self._sample_rate_osmosdr_tool_bar.addWidget(Qt.QLabel('Sample rate Osmosdr' + ": "))
        self._sample_rate_osmosdr_line_edit = Qt.QLineEdit(str(self.sample_rate_osmosdr))
        self._sample_rate_osmosdr_tool_bar.addWidget(self._sample_rate_osmosdr_line_edit)
        self._sample_rate_osmosdr_line_edit.returnPressed.connect(
            lambda: self.set_sample_rate_osmosdr(eng_notation.str_to_num(str(self._sample_rate_osmosdr_line_edit.text()))))
        self.top_grid_layout.addWidget(self._sample_rate_osmosdr_tool_bar, 7, 2, 1, 2)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._sample_rate_gr_tool_bar = Qt.QToolBar(self)
        self._sample_rate_gr_tool_bar.addWidget(Qt.QLabel('Sample rate gr-rpitx  ' + ": "))
        self._sample_rate_gr_line_edit = Qt.QLineEdit(str(self.sample_rate_gr))
        self._sample_rate_gr_tool_bar.addWidget(self._sample_rate_gr_line_edit)
        self._sample_rate_gr_line_edit.returnPressed.connect(
            lambda: self.set_sample_rate_gr(eng_notation.str_to_num(str(self._sample_rate_gr_line_edit.text()))))
        self.top_grid_layout.addWidget(self._sample_rate_gr_tool_bar, 6, 2, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            512,
            0,
            1.0,
            "Frequency (Hz)",
            "Relative Gain (dB)",
            "",
            1 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(-140, 10)
        self.qtgui_vector_sink_f_0.enable_autoscale(True)
        self.qtgui_vector_sink_f_0.enable_grid(False)
        self.qtgui_vector_sink_f_0.set_x_axis_units("Hz")
        self.qtgui_vector_sink_f_0.set_y_axis_units("dB")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_0_grid_layout_1.addWidget(self._qtgui_vector_sink_f_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 4):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            sample_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1.25, 1.25)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.4, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            4096, #size
            firdes.WIN_HAMMING, #wintype
            measured_frequency, #fc
            sample_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-77, -5)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, -14, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_0_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 4)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 4):
            self.tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self._offset__tool_bar = Qt.QToolBar(self)
        self._offset__tool_bar.addWidget(Qt.QLabel('Offset                        ' + ": "))
        self._offset__line_edit = Qt.QLineEdit(str(self.offset_))
        self._offset__tool_bar.addWidget(self._offset__line_edit)
        self._offset__line_edit.returnPressed.connect(
            lambda: self.set_offset_(eng_notation.str_to_num(str(self._offset__line_edit.text()))))
        self.top_grid_layout.addWidget(self._offset__tool_bar, 5, 2, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._frequency__tool_bar = Qt.QToolBar(self)
        self._frequency__tool_bar.addWidget(Qt.QLabel('Test frequency           ' + ": "))
        self._frequency__line_edit = Qt.QLineEdit(str(self.frequency_))
        self._frequency__tool_bar.addWidget(self._frequency__line_edit)
        self._frequency__line_edit.returnPressed.connect(
            lambda: self.set_frequency_(eng_notation.str_to_num(str(self._frequency__line_edit.text()))))
        self.top_grid_layout.addWidget(self._frequency__tool_bar, 4, 0, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._end_freq_tool_bar = Qt.QToolBar(self)
        self._end_freq_tool_bar.addWidget(Qt.QLabel('End frequency' + ": "))
        self._end_freq_line_edit = Qt.QLineEdit(str(self.end_freq))
        self._end_freq_tool_bar.addWidget(self._end_freq_line_edit)
        self._end_freq_line_edit.returnPressed.connect(
            lambda: self.set_end_freq(eng_notation.str_to_num(str(self._end_freq_line_edit.text()))))
        self.tab_widget_0_grid_layout_1.addWidget(self._end_freq_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self._carrying_frequency_tool_bar = Qt.QToolBar(self)
        self._carrying_frequency_tool_bar.addWidget(Qt.QLabel('Carrying frequency     ' + ": "))
        self._carrying_frequency_line_edit = Qt.QLineEdit(str(self.carrying_frequency))
        self._carrying_frequency_tool_bar.addWidget(self._carrying_frequency_line_edit)
        self._carrying_frequency_line_edit.returnPressed.connect(
            lambda: self.set_carrying_frequency(eng_notation.str_to_num(str(self._carrying_frequency_line_edit.text()))))
        self.top_grid_layout.addWidget(self._carrying_frequency_tool_bar, 6, 0, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        _btn_start_push_button = Qt.QPushButton("Start")
        _btn_start_push_button = Qt.QPushButton("Start")
        self._btn_start_choices = {'Pressed': 1, 'Released': 0}
        _btn_start_push_button.pressed.connect(lambda: self.set_btn_start(self._btn_start_choices['Pressed']))
        _btn_start_push_button.released.connect(lambda: self.set_btn_start(self._btn_start_choices['Released']))
        self.tab_widget_0_grid_layout_1.addWidget(_btn_start_push_button, 1, 3, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(3, 4):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self.blocks_vector_source_x_0 = blocks.vector_source_f(vector_data, True, 512, [])
        self._amplitude__tool_bar = Qt.QToolBar(self)
        self._amplitude__tool_bar.addWidget(Qt.QLabel('Amplitude                   ' + ": "))
        self._amplitude__line_edit = Qt.QLineEdit(str(self.amplitude_))
        self._amplitude__tool_bar.addWidget(self._amplitude__line_edit)
        self._amplitude__line_edit.returnPressed.connect(
            lambda: self.set_amplitude_(eng_notation.str_to_num(str(self._amplitude__line_edit.text()))))
        self.top_grid_layout.addWidget(self._amplitude__tool_bar, 5, 0, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rxtx_PC")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sample_rate_osmosdr(self):
        return self.sample_rate_osmosdr

    def set_sample_rate_osmosdr(self, sample_rate_osmosdr):
        self.sample_rate_osmosdr = sample_rate_osmosdr
        self.set_sample_rate(self.sample_rate_osmosdr)
        Qt.QMetaObject.invokeMethod(self._sample_rate_osmosdr_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.sample_rate_osmosdr)))

    def get_waveform_(self):
        return self.waveform_

    def set_waveform_(self, waveform_):
        self.waveform_ = waveform_
        self._waveform__callback(self.waveform_)

    def get_vector_data(self):
        return self.vector_data

    def set_vector_data(self, vector_data):
        self.vector_data = vector_data
        self.blocks_vector_source_x_0.set_data(self.vector_data, [])

    def get_start_freq(self):
        return self.start_freq

    def set_start_freq(self, start_freq):
        self.start_freq = start_freq
        Qt.QMetaObject.invokeMethod(self._start_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.start_freq)))

    def get_span_freq(self):
        return self.span_freq

    def set_span_freq(self, span_freq):
        self.span_freq = span_freq
        Qt.QMetaObject.invokeMethod(self._span_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.span_freq)))

    def get_sample_rate_gr(self):
        return self.sample_rate_gr

    def set_sample_rate_gr(self, sample_rate_gr):
        self.sample_rate_gr = sample_rate_gr
        Qt.QMetaObject.invokeMethod(self._sample_rate_gr_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.sample_rate_gr)))

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(self.measured_frequency, self.sample_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.sample_rate)

    def get_record(self):
        return self.record

    def set_record(self, record):
        self.record = record

    def get_offset_(self):
        return self.offset_

    def set_offset_(self, offset_):
        self.offset_ = offset_
        Qt.QMetaObject.invokeMethod(self._offset__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.offset_)))

    def get_measured_frequency(self):
        return self.measured_frequency

    def set_measured_frequency(self, measured_frequency):
        self.measured_frequency = measured_frequency
        Qt.QMetaObject.invokeMethod(self._measured_frequency_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.measured_frequency)))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.measured_frequency, self.sample_rate)

    def get_frequency_(self):
        return self.frequency_

    def set_frequency_(self, frequency_):
        self.frequency_ = frequency_
        Qt.QMetaObject.invokeMethod(self._frequency__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.frequency_)))

    def get_end_freq(self):
        return self.end_freq

    def set_end_freq(self, end_freq):
        self.end_freq = end_freq
        Qt.QMetaObject.invokeMethod(self._end_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.end_freq)))

    def get_carrying_frequency(self):
        return self.carrying_frequency

    def set_carrying_frequency(self, carrying_frequency):
        self.carrying_frequency = carrying_frequency
        Qt.QMetaObject.invokeMethod(self._carrying_frequency_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.carrying_frequency)))

    def get_btn_start(self):
        return self.btn_start

    def set_btn_start(self, btn_start):
        self.btn_start = btn_start

    def get_amplitude_(self):
        return self.amplitude_

    def set_amplitude_(self, amplitude_):
        self.amplitude_ = amplitude_
        Qt.QMetaObject.invokeMethod(self._amplitude__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.amplitude_)))

def snipfcn_snippet_0(self):
    print("Starting client and GUI")
    import threading
    threading.Thread(target=epy_module_client.client, daemon=True, args=(self,)).start()
    threading.Thread(target=epy_module_sweep.sweep, daemon=True, args=(self,)).start()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)




def main(top_block_cls=rxtx_PC, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
