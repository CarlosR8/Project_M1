# this module will be imported in the into your flowgraph

import numpy as np
import zmq
import array
from PyQt5 import Qt
import time
import scipy.interpolate as interp

# Function to divide the frequencies sub-lists
def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]
        yield every_chunk
#
def sweep(tt):
    Nt=10
    context=zmq.Context()
    
    mean_amplitude=[]
    mean_amplitude_array=[]
    # mean_amplitude_array=np.array([0])
    while True:
        while tt.get_sweeping()=="True":
            # Retrieve start, span and end frequency
            start_freq=tt.get_entry_start_freq()/5
            span_freq=tt.get_entry_span_freq()
            end_freq=tt.get_entry_end_freq()/5
            # Calculate the frequency range
            frequencies=np.arange(start_freq,end_freq,span_freq).tolist()
            frequencies.append(end_freq)
            n=int(len(frequencies)/((end_freq-start_freq)/100e3))
            frequency_chunks=list(list_split(frequencies, n))
            # Main procees
            for set in frequency_chunks:
                print("Changing carry frequency: {}".format(float(set[0])))
                # tt.set_entry_var_carrying_frequency(float(set[0]))
                for f in set:
                    # tt.set_entry_var_frequency_(float(f))
                    tt.set_entry_var_carrying_frequency(float(f)) 
                    time.sleep(0.75) # Sleep for 500 miliseconds
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
                    # mean_amplitude.append(np.mean(np.abs(recv)))      # Absolute values
                    a = np.array( [ num for num in recv if num >= 0 ] ) # Only positive values
                    mean_amplitude.append(np.mean(a)) # 
                    mean_amplitude_array=np.array(mean_amplitude)
                    try:
                        # Plot the results
                        arr_ref = np.array(range(int(tt.get_vector_length()))) # Reference array for inporlation
                        mean_interp = interp.interp1d(np.arange(mean_amplitude_array.size),mean_amplitude_array)
                        new_mean_amplitude_array = mean_interp(np.linspace(0,mean_amplitude_array.size-1,arr_ref.size))
                        tt.set_vector_data(new_mean_amplitude_array)
                    except:
                        pass
            tt.set_x_start((frequencies[0]*5)/1e6)
            tt.set_x_step(((frequencies[len(frequencies)-1]-frequencies[0])/tt.get_vector_length())/1e6)
            # All frequencies tested, set button back to "Start"
            btn_index=5
            tt.tab_widget_0_grid_layout_1.itemAt(btn_index).widget().setText("Start")
            tt.set_sweeping("False")
            # Reset arrays
            mean_amplitude=[]
            mean_amplitude_array=[]

