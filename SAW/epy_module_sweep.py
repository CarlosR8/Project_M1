# this module will be imported in the into your flowgraph

import numpy as np
import zmq
import array
from PyQt5 import Qt

def sweep(tt):
    while True:
        # Check if "start" has been pressed
        if((tt.get_btn_start()==1) & (tt.tab_widget_0_grid_layout_1.itemAt(4).widget().text() == "Start")):
            tt.tab_widget_0_grid_layout_1.itemAt(4).widget().setText("Stop")
            tt.set_btn_start(0)
        elif((tt.get_btn_start()==1) & (tt.tab_widget_0_grid_layout_1.itemAt(4).widget().text() == "Stop")):
            tt.tab_widget_0_grid_layout_1.itemAt(4).widget().setText("Start")
            tt.set_btn_start(0)
        # Retrieve start, span and end frequency
        # start_freq=tt.get_start_freq()
        # span_freq=tt.get_span_freq()
        # stop_freq=tt.get_end_freq()
        # pass
        # Nt=10
        # context=zmq.Context()
        # sock1=context.socket(zmq.SUB)
        # sock1.connect("tcp://192.168.137.8:5555");
        # sock1.setsockopt(zmq.SUBSCRIBE,b"")
        # vector1=[]
        # print("start")
        # while(len(vector1)<Nt):
        #     raw_recv=sock1.recv()
        #     recv=array.array('f',raw_recv) #float
        #     # recv=array.array('l',raw_recv) #integer
        #     # print(recv)
        #     vector1.append(recv)

        # print("finish")
        # # print(recv)
        # f = open("data.txt", "w")
        # f.write(str(recv))
        # f.close()