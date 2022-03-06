#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Raspberry pi emitter (gr-rpitx)
# Author: cmrivera
# GNU Radio version: v3.8.5.0-5-g982205bd

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import epy_module_server  # embedded python module
import rpitx


class tx_Pi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Raspberry pi emitter (gr-rpitx)")

        ##################################################
        # Variables
        ##################################################
        self.var_waveform_ = var_waveform_ = 101
        self.entry_var_sample_rate_osmosdr = entry_var_sample_rate_osmosdr = 1.152e6
        self.entry_var_sample_rate_gr = entry_var_sample_rate_gr = 200e3
        self.entry_var_offset_ = entry_var_offset_ = 0.5
        self.entry_var_measured_frequency = entry_var_measured_frequency = 434e6
        self.entry_var_frequency_ = entry_var_frequency_ = 10000
        self.entry_var_carrying_frequency = entry_var_carrying_frequency = 86.8e6
        self.entry_var_amplitude_ = entry_var_amplitude_ = 0.3

        ##################################################
        # Blocks
        ##################################################
        self.rpitx_rpitx_sink_0 = rpitx.rpitx_sink(entry_var_sample_rate_gr, entry_var_carrying_frequency)
        self.blocks_magphase_to_complex_0 = blocks.magphase_to_complex(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(entry_var_sample_rate_gr, var_waveform_, entry_var_frequency_, entry_var_amplitude_, entry_var_offset_, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_magphase_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_magphase_to_complex_0, 0))
        self.connect((self.blocks_magphase_to_complex_0, 0), (self.rpitx_rpitx_sink_0, 0))


    def get_var_waveform_(self):
        return self.var_waveform_

    def set_var_waveform_(self, var_waveform_):
        self.var_waveform_ = var_waveform_
        self.analog_sig_source_x_0.set_waveform(self.var_waveform_)

    def get_entry_var_sample_rate_osmosdr(self):
        return self.entry_var_sample_rate_osmosdr

    def set_entry_var_sample_rate_osmosdr(self, entry_var_sample_rate_osmosdr):
        self.entry_var_sample_rate_osmosdr = entry_var_sample_rate_osmosdr

    def get_entry_var_sample_rate_gr(self):
        return self.entry_var_sample_rate_gr

    def set_entry_var_sample_rate_gr(self, entry_var_sample_rate_gr):
        self.entry_var_sample_rate_gr = entry_var_sample_rate_gr
        self.analog_sig_source_x_0.set_sampling_freq(self.entry_var_sample_rate_gr)

    def get_entry_var_offset_(self):
        return self.entry_var_offset_

    def set_entry_var_offset_(self, entry_var_offset_):
        self.entry_var_offset_ = entry_var_offset_
        self.analog_sig_source_x_0.set_offset(self.entry_var_offset_)

    def get_entry_var_measured_frequency(self):
        return self.entry_var_measured_frequency

    def set_entry_var_measured_frequency(self, entry_var_measured_frequency):
        self.entry_var_measured_frequency = entry_var_measured_frequency

    def get_entry_var_frequency_(self):
        return self.entry_var_frequency_

    def set_entry_var_frequency_(self, entry_var_frequency_):
        self.entry_var_frequency_ = entry_var_frequency_
        self.analog_sig_source_x_0.set_frequency(self.entry_var_frequency_)

    def get_entry_var_carrying_frequency(self):
        return self.entry_var_carrying_frequency

    def set_entry_var_carrying_frequency(self, entry_var_carrying_frequency):
        self.entry_var_carrying_frequency = entry_var_carrying_frequency
        self.rpitx_rpitx_sink_0.set_freq(self.entry_var_carrying_frequency)

    def get_entry_var_amplitude_(self):
        return self.entry_var_amplitude_

    def set_entry_var_amplitude_(self, entry_var_amplitude_):
        self.entry_var_amplitude_ = entry_var_amplitude_
        self.analog_sig_source_x_0.set_amplitude(self.entry_var_amplitude_)

def snipfcn_snippet_0(self):
    print("Starting server")
    import threading
    threading.Thread(target=epy_module_server.server,args=(self,)).start()
    from subprocess import Popen
    Popen(['python', 'rx_Pi.py'])


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)




def main(top_block_cls=tx_Pi, options=None):
    tb = top_block_cls()
    snippets_main_after_init(tb)
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
