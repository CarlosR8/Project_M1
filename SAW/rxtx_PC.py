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
        self.vector_length = vector_length = 1024
        self.var_status = var_status = "(0/0) - 0%"
        self.vector_data_2 = vector_data_2 = range(vector_length)
        self.vector_data = vector_data = range(vector_length)
        self.var_waveform_ = var_waveform_ = 2
        self.var_record = var_record = "False"
        self.var_method = var_method = 0
        self.sweeping = sweeping = "False"
        self.status = status = var_status
        self.sample_rate = sample_rate = 1.152e6
        self.entry_var_offset_ = entry_var_offset_ = 0.5
        self.entry_var_measured_frequency = entry_var_measured_frequency = 434e6
        self.entry_var_frequency_ = entry_var_frequency_ = 10e3
        self.entry_var_carrying_frequency = entry_var_carrying_frequency = 86.8e6
        self.entry_var_amplitude_ = entry_var_amplitude_ = 300e-3
        self.entry_start_freq = entry_start_freq = 433.42e6
        self.entry_span_freq = entry_span_freq = 2e3
        self.entry_end_freq = entry_end_freq = 434.58e6
        self.btn_start = btn_start = 0

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
        self._entry_var_measured_frequency_tool_bar = Qt.QToolBar(self)
        self._entry_var_measured_frequency_tool_bar.addWidget(Qt.QLabel('Measured Frequency  ' + ": "))
        self._entry_var_measured_frequency_line_edit = Qt.QLineEdit(str(self.entry_var_measured_frequency))
        self._entry_var_measured_frequency_tool_bar.addWidget(self._entry_var_measured_frequency_line_edit)
        self._entry_var_measured_frequency_line_edit.returnPressed.connect(
            lambda: self.set_entry_var_measured_frequency(eng_notation.str_to_num(str(self._entry_var_measured_frequency_line_edit.text()))))
        self.top_grid_layout.addWidget(self._entry_var_measured_frequency_tool_bar, 6, 2, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, 'tcp://192.168.137.8:5555', 100, False, -1)
        # Create the options list
        self._var_waveform__options = [0, 1, 2, 3, 4, 5]
        # Create the labels list
        self._var_waveform__labels = ['Constant', 'Sine', 'Cosine', 'Square', 'Triangle', 'Saw Tooth']
        # Create the combo box
        self._var_waveform__tool_bar = Qt.QToolBar(self)
        self._var_waveform__tool_bar.addWidget(Qt.QLabel('Waveform                  ' + ": "))
        self._var_waveform__combo_box = Qt.QComboBox()
        self._var_waveform__tool_bar.addWidget(self._var_waveform__combo_box)
        for _label in self._var_waveform__labels: self._var_waveform__combo_box.addItem(_label)
        self._var_waveform__callback = lambda i: Qt.QMetaObject.invokeMethod(self._var_waveform__combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._var_waveform__options.index(i)))
        self._var_waveform__callback(self.var_waveform_)
        self._var_waveform__combo_box.currentIndexChanged.connect(
            lambda i: self.set_var_waveform_(self._var_waveform__options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._var_waveform__tool_bar, 4, 2, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._var_method_options = [0, 1]
        # Create the labels list
        self._var_method_labels = ['Sweep carrier frequency', 'Sweep generated frequency']
        # Create the combo box
        # Create the radio buttons
        self._var_method_group_box = Qt.QGroupBox('Sweeping method' + ": ")
        self._var_method_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._var_method_button_group = variable_chooser_button_group()
        self._var_method_group_box.setLayout(self._var_method_box)
        for i, _label in enumerate(self._var_method_labels):
            radio_button = Qt.QRadioButton(_label)
            self._var_method_box.addWidget(radio_button)
            self._var_method_button_group.addButton(radio_button, i)
        self._var_method_callback = lambda i: Qt.QMetaObject.invokeMethod(self._var_method_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._var_method_options.index(i)))
        self._var_method_callback(self.var_method)
        self._var_method_button_group.buttonClicked[int].connect(
            lambda i: self.set_var_method(self._var_method_options[i]))
        self.tab_widget_0_grid_layout_1.addWidget(self._var_method_group_box, 2, 0, 1, 1)
        for r in range(2, 3):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self._status_tool_bar = Qt.QToolBar(self)

        if None:
            self._status_formatter = None
        else:
            self._status_formatter = lambda x: str(x)

        self._status_tool_bar.addWidget(Qt.QLabel('Progress' + ": "))
        self._status_label = Qt.QLabel(str(self._status_formatter(self.status)))
        self._status_tool_bar.addWidget(self._status_label)
        self.tab_widget_0_grid_layout_1.addWidget(self._status_tool_bar, 2, 1, 1, 2)
        for r in range(2, 3):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 3):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            vector_length,
            433.42,
            0.0002265625,
            "Frequency (MHz)",
            "Relative Mean voltage",
            "",
            2 # Number of inputs
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis(0, 0.4)
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("MHz")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [2, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
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
        self.qtgui_time_sink_x_0.set_y_axis(-1.1, 1.1)

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
            entry_var_measured_frequency, #fc
            sample_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-90, -5)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, -14, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
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
        self._entry_var_offset__tool_bar = Qt.QToolBar(self)
        self._entry_var_offset__tool_bar.addWidget(Qt.QLabel('Offset                        ' + ": "))
        self._entry_var_offset__line_edit = Qt.QLineEdit(str(self.entry_var_offset_))
        self._entry_var_offset__tool_bar.addWidget(self._entry_var_offset__line_edit)
        self._entry_var_offset__line_edit.returnPressed.connect(
            lambda: self.set_entry_var_offset_(eng_notation.str_to_num(str(self._entry_var_offset__line_edit.text()))))
        self.top_grid_layout.addWidget(self._entry_var_offset__tool_bar, 5, 2, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._entry_var_frequency__tool_bar = Qt.QToolBar(self)
        self._entry_var_frequency__tool_bar.addWidget(Qt.QLabel('Test frequency           ' + ": "))
        self._entry_var_frequency__line_edit = Qt.QLineEdit(str(self.entry_var_frequency_))
        self._entry_var_frequency__tool_bar.addWidget(self._entry_var_frequency__line_edit)
        self._entry_var_frequency__line_edit.returnPressed.connect(
            lambda: self.set_entry_var_frequency_(eng_notation.str_to_num(str(self._entry_var_frequency__line_edit.text()))))
        self.top_grid_layout.addWidget(self._entry_var_frequency__tool_bar, 4, 0, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._entry_var_carrying_frequency_tool_bar = Qt.QToolBar(self)
        self._entry_var_carrying_frequency_tool_bar.addWidget(Qt.QLabel('Carrier frequency       ' + ": "))
        self._entry_var_carrying_frequency_line_edit = Qt.QLineEdit(str(self.entry_var_carrying_frequency))
        self._entry_var_carrying_frequency_tool_bar.addWidget(self._entry_var_carrying_frequency_line_edit)
        self._entry_var_carrying_frequency_line_edit.returnPressed.connect(
            lambda: self.set_entry_var_carrying_frequency(eng_notation.str_to_num(str(self._entry_var_carrying_frequency_line_edit.text()))))
        self.top_grid_layout.addWidget(self._entry_var_carrying_frequency_tool_bar, 6, 0, 1, 2)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._entry_var_amplitude__tool_bar = Qt.QToolBar(self)
        self._entry_var_amplitude__tool_bar.addWidget(Qt.QLabel('Amplitude                   ' + ": "))
        self._entry_var_amplitude__line_edit = Qt.QLineEdit(str(self.entry_var_amplitude_))
        self._entry_var_amplitude__tool_bar.addWidget(self._entry_var_amplitude__line_edit)
        self._entry_var_amplitude__line_edit.returnPressed.connect(
            lambda: self.set_entry_var_amplitude_(eng_notation.str_to_num(str(self._entry_var_amplitude__line_edit.text()))))
        self.top_grid_layout.addWidget(self._entry_var_amplitude__tool_bar, 5, 0, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._entry_start_freq_tool_bar = Qt.QToolBar(self)
        self._entry_start_freq_tool_bar.addWidget(Qt.QLabel('Start frequency' + ": "))
        self._entry_start_freq_line_edit = Qt.QLineEdit(str(self.entry_start_freq))
        self._entry_start_freq_tool_bar.addWidget(self._entry_start_freq_line_edit)
        self._entry_start_freq_line_edit.returnPressed.connect(
            lambda: self.set_entry_start_freq(eng_notation.str_to_num(str(self._entry_start_freq_line_edit.text()))))
        self.tab_widget_0_grid_layout_1.addWidget(self._entry_start_freq_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self._entry_span_freq_tool_bar = Qt.QToolBar(self)
        self._entry_span_freq_tool_bar.addWidget(Qt.QLabel('Span' + ": "))
        self._entry_span_freq_line_edit = Qt.QLineEdit(str(self.entry_span_freq))
        self._entry_span_freq_tool_bar.addWidget(self._entry_span_freq_line_edit)
        self._entry_span_freq_line_edit.returnPressed.connect(
            lambda: self.set_entry_span_freq(eng_notation.str_to_num(str(self._entry_span_freq_line_edit.text()))))
        self.tab_widget_0_grid_layout_1.addWidget(self._entry_span_freq_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self._entry_end_freq_tool_bar = Qt.QToolBar(self)
        self._entry_end_freq_tool_bar.addWidget(Qt.QLabel('End frequency' + ": "))
        self._entry_end_freq_line_edit = Qt.QLineEdit(str(self.entry_end_freq))
        self._entry_end_freq_tool_bar.addWidget(self._entry_end_freq_line_edit)
        self._entry_end_freq_line_edit.returnPressed.connect(
            lambda: self.set_entry_end_freq(eng_notation.str_to_num(str(self._entry_end_freq_line_edit.text()))))
        self.tab_widget_0_grid_layout_1.addWidget(self._entry_end_freq_tool_bar, 1, 2, 1, 1)
        for r in range(1, 2):
            self.tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(2, 3):
            self.tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
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
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f(vector_data_2, True, vector_length, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_f(vector_data, True, vector_length, [])


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_time_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rxtx_PC")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_vector_length(self):
        return self.vector_length

    def set_vector_length(self, vector_length):
        self.vector_length = vector_length
        self.set_vector_data(range(self.vector_length))
        self.set_vector_data_2(range(self.vector_length))

    def get_var_status(self):
        return self.var_status

    def set_var_status(self, var_status):
        self.var_status = var_status
        self.set_status(self._status_formatter(self.var_status))

    def get_vector_data_2(self):
        return self.vector_data_2

    def set_vector_data_2(self, vector_data_2):
        self.vector_data_2 = vector_data_2
        self.blocks_vector_source_x_0_0.set_data(self.vector_data_2, [])

    def get_vector_data(self):
        return self.vector_data

    def set_vector_data(self, vector_data):
        self.vector_data = vector_data
        self.blocks_vector_source_x_0.set_data(self.vector_data, [])

    def get_var_waveform_(self):
        return self.var_waveform_

    def set_var_waveform_(self, var_waveform_):
        self.var_waveform_ = var_waveform_
        self._var_waveform__callback(self.var_waveform_)

    def get_var_record(self):
        return self.var_record

    def set_var_record(self, var_record):
        self.var_record = var_record

    def get_var_method(self):
        return self.var_method

    def set_var_method(self, var_method):
        self.var_method = var_method
        self._var_method_callback(self.var_method)

    def get_sweeping(self):
        return self.sweeping

    def set_sweeping(self, sweeping):
        self.sweeping = sweeping

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
        Qt.QMetaObject.invokeMethod(self._status_label, "setText", Qt.Q_ARG("QString", self.status))

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(self.entry_var_measured_frequency, self.sample_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.sample_rate)

    def get_entry_var_offset_(self):
        return self.entry_var_offset_

    def set_entry_var_offset_(self, entry_var_offset_):
        self.entry_var_offset_ = entry_var_offset_
        Qt.QMetaObject.invokeMethod(self._entry_var_offset__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_var_offset_)))

    def get_entry_var_measured_frequency(self):
        return self.entry_var_measured_frequency

    def set_entry_var_measured_frequency(self, entry_var_measured_frequency):
        self.entry_var_measured_frequency = entry_var_measured_frequency
        Qt.QMetaObject.invokeMethod(self._entry_var_measured_frequency_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_var_measured_frequency)))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.entry_var_measured_frequency, self.sample_rate)

    def get_entry_var_frequency_(self):
        return self.entry_var_frequency_

    def set_entry_var_frequency_(self, entry_var_frequency_):
        self.entry_var_frequency_ = entry_var_frequency_
        Qt.QMetaObject.invokeMethod(self._entry_var_frequency__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_var_frequency_)))

    def get_entry_var_carrying_frequency(self):
        return self.entry_var_carrying_frequency

    def set_entry_var_carrying_frequency(self, entry_var_carrying_frequency):
        self.entry_var_carrying_frequency = entry_var_carrying_frequency
        Qt.QMetaObject.invokeMethod(self._entry_var_carrying_frequency_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_var_carrying_frequency)))

    def get_entry_var_amplitude_(self):
        return self.entry_var_amplitude_

    def set_entry_var_amplitude_(self, entry_var_amplitude_):
        self.entry_var_amplitude_ = entry_var_amplitude_
        Qt.QMetaObject.invokeMethod(self._entry_var_amplitude__line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_var_amplitude_)))

    def get_entry_start_freq(self):
        return self.entry_start_freq

    def set_entry_start_freq(self, entry_start_freq):
        self.entry_start_freq = entry_start_freq
        Qt.QMetaObject.invokeMethod(self._entry_start_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_start_freq)))

    def get_entry_span_freq(self):
        return self.entry_span_freq

    def set_entry_span_freq(self, entry_span_freq):
        self.entry_span_freq = entry_span_freq
        Qt.QMetaObject.invokeMethod(self._entry_span_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_span_freq)))

    def get_entry_end_freq(self):
        return self.entry_end_freq

    def set_entry_end_freq(self, entry_end_freq):
        self.entry_end_freq = entry_end_freq
        Qt.QMetaObject.invokeMethod(self._entry_end_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.entry_end_freq)))

    def get_btn_start(self):
        return self.btn_start

    def set_btn_start(self, btn_start):
        self.btn_start = btn_start

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
