#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Raspberry Pi Receiver
# Author: cmrivera
# GNU Radio version: v3.8.5.0-5-g982205bd

from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import epy_module_shared_variable  # embedded python module
import osmosdr
import time


class rx_Pi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Raspberry Pi Receiver")

        ##################################################
        # Variables
        ##################################################
        self.sample_rate_osmosdr = sample_rate_osmosdr = 1.152e6
        self.measured_frequency = measured_frequency = 434e6

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, 'tcp://192.168.137.8:5555', 100, False, -1)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(sample_rate_osmosdr)
        self.osmosdr_source_0.set_center_freq(measured_frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(3, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.zeromq_pub_sink_0, 0))


    def get_sample_rate_osmosdr(self):
        return self.sample_rate_osmosdr

    def set_sample_rate_osmosdr(self, sample_rate_osmosdr):
        self.sample_rate_osmosdr = sample_rate_osmosdr
        self.osmosdr_source_0.set_sample_rate(self.sample_rate_osmosdr)

    def get_measured_frequency(self):
        return self.measured_frequency

    def set_measured_frequency(self, measured_frequency):
        self.measured_frequency = measured_frequency
        self.osmosdr_source_0.set_center_freq(self.measured_frequency, 0)

def snipfcn_snippet_0(self):
    print("Starting Receiver")
    import threading
    threading.Thread(target=epy_module_shared_variable.main,args=(self,)).start()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)




def main(top_block_cls=rx_Pi, options=None):
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
