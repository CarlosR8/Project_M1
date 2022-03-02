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
import rpitx


class tx_Pi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Raspberry pi emitter (gr-rpitx)")

        ##################################################
        # Variables
        ##################################################
        self.waveform_ = waveform_ = 3
        self.sample_rate = sample_rate = 200e3
        self.frequency_ = frequency_ = 5e3

        ##################################################
        # Blocks
        ##################################################
        self.rpitx_rpitx_sink_0 = rpitx.rpitx_sink(sample_rate, 86.6e6)
        self.blocks_magphase_to_complex_0 = blocks.magphase_to_complex(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(sample_rate, waveform_, frequency_, 400e-3, 500e-3, 0)
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

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.sample_rate)

    def get_frequency_(self):
        return self.frequency_

    def set_frequency_(self, frequency_):
        self.frequency_ = frequency_
        self.analog_sig_source_x_0.set_frequency(self.frequency_)





def main(top_block_cls=tx_Pi, options=None):
    tb = top_block_cls()

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
