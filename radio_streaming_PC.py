#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: radio_streaming_PC
# GNU Radio version: 3.9.5.0

from gnuradio import audio
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq
import radio_streaming_PC_epy_module_GUI as epy_module_GUI  # embedded python module
import radio_streaming_PC_epy_module_client as epy_module_client  # embedded python module
import threading


def snipfcn_snippet_0(self):
    print("Starting client and GUI")
    #import threading
    threading.Thread(target=epy_module_client.client, daemon=True, args=(self,)).start()
    threading.Thread(target=epy_module_GUI.gui, daemon=True, args=(self,)).start().start()


def snippets_main_after_init(tb):
    snipfcn_snippet_0(tb)


class radio_streaming_PC(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "radio_streaming_PC", catch_exceptions=True)

        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.stream_variable = stream_variable = "False"
        self.station = station = 096.9e6
        self.samp_rate = samp_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_float, 1, 'tcp://192.168.137.8:5555', 100, False, -1, '')
        self.audio_sink_0 = audio.sink(samp_rate, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.zeromq_sub_source_0, 0), (self.audio_sink_0, 0))


    def get_stream_variable(self):
        return self.stream_variable

    def set_stream_variable(self, stream_variable):
        with self._lock:
            self.stream_variable = stream_variable

    def get_station(self):
        return self.station

    def set_station(self, station):
        with self._lock:
            self.station = station

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        with self._lock:
            self.samp_rate = samp_rate




def main(top_block_cls=radio_streaming_PC, options=None):
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
