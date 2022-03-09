# this module will be imported in the into your flowgraph

import numpy as np
import zmq
import array
from PyQt5 import Qt
import time
import scipy.interpolate as interp

def sweep(tt):
    Nt=10
    context=zmq.Context()
    
    mean_amplitude=[]
    # mean_amplitude_array=np.array([0])
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
                # tt.set_entry_var_frequency_(float(f)) 
                time.sleep(0.5) # Sleep for 3 seconds
                if tt.get_sweeping()=="False":
                    break
                # Record stream of data
                sock1=context.socket(zmq.SUB)
                sock1.connect("tcp://192.168.137.8:5555")
                sock1.setsockopt(zmq.SUBSCRIBE,b"")
                raw_recv=sock1.recv()
                sock1.close()
                recv=array.array('f',raw_recv) #float
                recv=recv[1::2]
                # mean_amplitude.append(np.mean(np.abs(recv))) # x[x >= 0]
                a = np.array( [ num for num in recv if num >= 0 ] )
                mean_amplitude.append(np.mean(a)) # 
                mean_amplitude_array=np.array(mean_amplitude)
                # print(mean_amplitude_array)
                # Plot results
                # tt.set_vector_length(len(mean_amplitude_array))
                # tt.set_vector_data(mean_amplitude_array)
                # Save vector in local file
                f = open("data/data_{}.txt".format(f), "w")
                f.write(str(recv))
                f.close()
            f = open("data/mean.txt", "w")
            f.write(str(mean_amplitude))
            f.close() 
            # Plot the results
            arr_ref = np.array(range(int(tt.get_vector_length()))) # Reference array for inporlation
            mean_interp = interp.interp1d(np.arange(mean_amplitude_array.size),mean_amplitude_array)
            new_mean_amplitude_array = mean_interp(np.linspace(0,mean_amplitude_array.size-1,arr_ref.size))
            tt.set_vector_data(new_mean_amplitude_array)
            tt.set_x_start(frequencies[0])
            tt.set_x_step((frequencies[len(frequencies)-1]-frequencies[0])/tt.get_vector_length())
            break
        # All frequencies tested, set button back to "Start"
        mean_amplitude=[]
        tt.tab_widget_0_grid_layout_1.itemAt(4).widget().setText("Start")
        tt.set_sweeping("False")

