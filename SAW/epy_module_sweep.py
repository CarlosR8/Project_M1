# this module will be imported in the into your flowgraph

import numpy as np
import zmq
import array
from PyQt5 import Qt
import time

def sweep(tt):
    while True:
        # Retrieve start, span and end frequency
        start_freq=tt.get_entry_start_freq()
        span_freq=tt.get_entry_span_freq()
        end_freq=tt.get_entry_end_freq()
        # Calculate the frequency range
        frequencies=np.arange(start_freq,end_freq,span_freq).tolist()
        frequencies.append(end_freq)
        # Main procees
        while tt.get_sweeping()=="True":
            for f in frequencies:
                tt.set_entry_var_carrying_frequency(float(f))
                time.sleep(3) # Sleep for 3 seconds
                if tt.get_sweeping()=="False":
                    break
                # Setting the test frequency

            # If the next frequency is 


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