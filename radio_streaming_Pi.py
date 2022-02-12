#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: radio_streaming_Pi
# GNU Radio version: 3.9.5.0

from gnuradio import analog
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import osmosdr
import time
import radio_streaming_Pi_epy_module_server as epy_module_server  # embedded python module
import threading


def snipfcn_snippet_0(self):
    print("Starting server")
    #import threading
    threading.Thread(target=epy_module_server.server,args=(self,)).start()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)


class radio_streaming_Pi(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "radio_streaming_Pi")

        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.station = station = 96.9e6
        self.samp_rate = samp_rate = 1.152e6

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_float, 1, 'tcp://192.168.137.8:5555', 100, False, -1)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(station, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            6,
            firdes.low_pass(
                1,
                samp_rate,
                96e3,
                48e3,
                window.WIN_HAMMING,
                6.76))
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=192e3,
        	audio_decimation=4,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.zeromq_pub_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))


    def get_station(self):
        return self.station

    def set_station(self, station):
        with self._lock:
            self.station = station
            self.osmosdr_source_0.set_center_freq(self.station, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        with self._lock:
            self.samp_rate = samp_rate
            self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 96e3, 48e3, window.WIN_HAMMING, 6.76))
            self.osmosdr_source_0.set_sample_rate(self.samp_rate)




def main(top_block_cls=radio_streaming_Pi, options=None):
    tb = top_block_cls()
    snippets_main_after_init(tb)
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
