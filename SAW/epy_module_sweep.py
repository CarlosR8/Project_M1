# this module will be imported in the into your flowgraph
import zmq
import numpy as np
import array
import scipy.interpolate as interp
import math
from PyQt5 import Qt
import time
import datetime
import os

# Function to print the measurement status on the GUI
def update_status(frequency_list, current_frequency, start_time):
    total=len(frequency_list)
    completed=frequency_list.index(current_frequency)+1
    percentage=(completed/total)*100
    elapsed_time=datetime.datetime.now()-start_time
    remaining_time=datetime.timedelta(seconds=elapsed_time.total_seconds()*((100-percentage)/percentage))
    return  "\t({0}/{1})\t\t-\t{2:1.2f}%\t-\tTime remaining: {3}\t-\tElapsed time: {4}".format(
        completed,total,percentage,str(remaining_time).split('.', 2)[0],str(elapsed_time).split('.', 2)[0])
#
# Function to divide the frequencies sub-lists
def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]
        yield every_chunk
#
# Function to retreive the index of the closest value of an array (not used)
def closest(lst, K):
     lst = np.asarray(lst)
     idx = (np.abs(lst - K)).argmin()
     return idx
#
def sweep(tt):
    context=zmq.Context()
    vector_length=int(tt.get_vector_length())
    mean_amplitude=[]
    mean_amplitude_array=[]
    
    real_values_array=np.full(vector_length,-1.0)
    mean_amplitude_array=np.array([0])
    # Set the vector sink properties
    tt.qtgui_vector_sink_f_0.set_line_marker(1,0)
    tt.qtgui_vector_sink_f_0.set_line_style(1,0)
    while True:
        while tt.get_sweeping()=="True":
            # Reset real points plot
            tt.set_vector_data_2(real_values_array)
            # Set delay variable
            delay=0.75
            start_time=datetime.datetime.now()
            # Clear the terminal
            os.system('cls||clear')
            # Deactivate/Activate Hold maximum in frequency sink
            tt.qtgui_freq_sink_x_0.enable_max_hold(False)
            tt.qtgui_freq_sink_x_0.enable_max_hold(True)
            # Retrieve start, span and end frequency
            start_freq=tt.get_entry_start_freq()/5
            span_freq=tt.get_entry_span_freq()
            end_freq=tt.get_entry_end_freq()/5
            # Calculate the frequency range
            frequencies=np.arange(start_freq,end_freq,span_freq).tolist()
            frequencies.append(end_freq)
            carrier_step=5e3
            n=int(len(frequencies)/((end_freq-start_freq)/carrier_step))
            frequency_chunks=list(list_split(frequencies, n))
            # Set the vector sink properties
            x_start=(start_freq*5)/1e6
            x_step=(5*(end_freq-start_freq)/1e6)/vector_length
            tt.qtgui_vector_sink_f_0.set_x_axis(x_start, x_step)
            # Main procees
            for set in frequency_chunks:
                if tt.get_var_method()==1: #Sweep generated frequency
                    print("Changing carrier frequency: {}".format(float(set[0])))
                    tt.set_entry_var_carrying_frequency(float(set[0]))
                    #Change measuring frequency
                    tt.set_entry_var_measured_frequency(float(set[0])*5)
                    time.sleep(delay) # Sleep for 750 miliseconds
                else:
                    tt.set_entry_var_measured_frequency(float(start_freq+(end_freq-start_freq)/2)*5)
                for f in set:
                    if tt.get_var_method()==0: #Sweep carrier frequency only
                        print("Changing carrier frequency: {}".format(float(f)))
                        tt.set_entry_var_carrying_frequency(float(f)) 
                    else: #Sweep generated frequency
                        print("Changing generated frequency: {}".format(float(f)))
                        tt.set_entry_var_frequency_(float(f)-float(set[0]))
                    time.sleep(delay) # Sleep for 750 miliseconds
                    # Update status label
                    try:
                        tt.set_var_status(update_status(frequencies, f, start_time))
                    except:
                        pass
                    #
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
                        arr_ref = np.array(range(vector_length)) # Reference array for inporlation
                        mean_interp = interp.interp1d(np.arange(mean_amplitude_array.size),mean_amplitude_array)
                        new_mean_amplitude_array = mean_interp(np.linspace(0,mean_amplitude_array.size-1,arr_ref.size))
                        tt.set_vector_data(new_mean_amplitude_array)
                    except:
                        pass
            # Plot the real values over interpolation
            idx=0
            try:
                for i,value in enumerate(new_mean_amplitude_array):
                    tolerance=abs(new_mean_amplitude_array[i]-new_mean_amplitude_array[i+1])
                    if math.isclose(value, mean_amplitude_array[idx],abs_tol = tolerance):
                        real_values_array[i]=value
                        idx=idx+1
            except:
                pass
            tt.set_vector_data_2(real_values_array)
            # All frequencies tested, set button back to "Start"
            btn_index=6
            tt.tab_widget_0_grid_layout_1.itemAt(btn_index).widget().setText("Start")
            tt.set_sweeping("False")
            # Reset arrays
            mean_amplitude=[]
            mean_amplitude_array=[]
            real_values_array=np.full(vector_length,-1.0)