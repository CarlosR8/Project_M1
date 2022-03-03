# this module will be imported in the into your flowgraph
import socket
from gnuradio import eng_notation
from PyQt5 import Qt

def client(tt):
    # Storage variables initial values
    variables=["frequency_","waveform_","amplitude_","offset_","sample_rate_gr","sample_rate_osmosdr","carrying_frequency","measured_frequency"]
    old_values=[]
    for variable in variables:
        exec("old_values.append(tt.get_{}())".format(variable))
        # Convert default values of entry controls to eng notation 
        if(variable == "waveform_"):
            continue # Skip if not an entry control
        Qt.QMetaObject.invokeMethod(eval("tt._{}_line_edit".format(variable)), "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(eval("tt.{}".format(variable)))))
    while True:
        # Try to connect
        host = '192.168.137.8'
        port = 4242
        client_socket = socket.socket()
        client_socket.connect((host, port))
        if(client_socket.getsockname()[0] != "0.0.0.0"):
            # Connected
            print("Connected to server")
            while True:
                # Check if variables have changed to send the new values
                for i, variable in enumerate(variables):
                    if(eval("tt.get_{}()".format(variable))!=old_values[i]):
                        value=eval("tt.get_{}()".format(variable))
                        if(variable=="waveform_"):
                            value=value+100

                        message=variable + "=" + str(value) + ">" # Encoding message to send it
                        client_socket.send(message.encode())
                        # Register updated variable value
                        old_values[i]=eval("tt.get_{}()".format(variable))
                        # testing
                        # tt._frequency__tool_bar.setStyleSheet("QLabel { }")

                    # Pending changes indicator:  
                    # Check if "entry" controls text has been modified to change its color (indicating pending "enter" key)
                    try: # To ignore when incorrect value is typed
                        if(variable=="waveform_"): # If the current variable is not an "entry" ignore
                            pass

                        if(eval("eng_notation.str_to_num(str(tt._{var_name}_line_edit.text()))!=float(tt.get_{var_name}())".format(var_name=variable))):
                            if(eval("tt._{}_tool_bar.styleSheet()".format(variable))!="QLabel {background-color: yellow}"):
                                # To avoid conflict between GUI thread and Working thread (segmentation error) it must be used the invokeMethod function
                                # https://stackoverflow.com/questions/37598016/qapplication-method-setstylesheet-called-from-other-thread-causes-segmentation-f
                                Qt.QMetaObject.invokeMethod(eval("tt._{}_tool_bar".format(variable)), "setStyleSheet", Qt.Q_ARG("QString", "QLabel {background-color: yellow}"))
                        else:
                            if(eval("tt._{}_tool_bar.styleSheet()".format(variable))!=""):
                                Qt.QMetaObject.invokeMethod(eval("tt._{}_tool_bar".format(variable)), "setStyleSheet", Qt.Q_ARG("QString", ""))                        
                    except:
                        pass

                # client_socket.close()
