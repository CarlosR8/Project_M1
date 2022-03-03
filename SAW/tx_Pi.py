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
        self.waveform_ = waveform_ = 103
        self.sample_rate_osmosdr = sample_rate_osmosdr = 1.152e6
        self.sample_rate_gr = sample_rate_gr = 200e3
        self.offset_ = offset_ = 0.5
        self.measured_frequency = measured_frequency = 434e6
        self.frequency_ = frequency_ = 86.8e6
        self.carrying_frequency = carrying_frequency = 86.8e6
        self.amplitude_ = amplitude_ = 0.4

        ##################################################
        # Blocks
        ##################################################
        self.rpitx_rpitx_sink_0 = rpitx.rpitx_sink(sample_rate_gr, carrying_frequency)
        self.blocks_magphase_to_complex_0 = blocks.magphase_to_complex(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(sample_rate_gr, waveform_, frequency_, amplitude_, offset_, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_magphase_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_magphase_to_complex_0, 0))
        self.connect((self.blocks_magphase_to_complex_0, 0), (self.rpitx_rpitx_sink_0, 0))


    def get_waveform_(self):
        return self.waveform_

    def set_waveform_(self, waveform_):
        self.waveform_ = waveform_
        self.analog_sig_source_x_0.set_waveform(self.waveform_)

    def get_sample_rate_osmosdr(self):
        return self.sample_rate_osmosdr

    def set_sample_rate_osmosdr(self, sample_rate_osmosdr):
        self.sample_rate_osmosdr = sample_rate_osmosdr

    def get_sample_rate_gr(self):
        return self.sample_rate_gr

    def set_sample_rate_gr(self, sample_rate_gr):
        self.sample_rate_gr = sample_rate_gr
        self.analog_sig_source_x_0.set_sampling_freq(self.sample_rate_gr)

    def get_offset_(self):
        return self.offset_

    def set_offset_(self, offset_):
        self.offset_ = offset_
        self.analog_sig_source_x_0.set_offset(self.offset_)

    def get_measured_frequency(self):
        return self.measured_frequency

    def set_measured_frequency(self, measured_frequency):
        self.measured_frequency = measured_frequency

    def get_frequency_(self):
        return self.frequency_

    def set_frequency_(self, frequency_):
        self.frequency_ = frequency_
        self.analog_sig_source_x_0.set_frequency(self.frequency_)

    def get_carrying_frequency(self):
        return self.carrying_frequency

    def set_carrying_frequency(self, carrying_frequency):
        self.carrying_frequency = carrying_frequency
        self.rpitx_rpitx_sink_0.set_freq(self.carrying_frequency)

    def get_amplitude_(self):
        return self.amplitude_

    def set_amplitude_(self, amplitude_):
        self.amplitude_ = amplitude_
        self.analog_sig_source_x_0.set_amplitude(self.amplitude_)

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
