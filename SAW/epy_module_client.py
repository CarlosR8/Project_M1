# this module will be imported in the into your flowgraph
import socket
from gnuradio import eng_notation
from PyQt5 import Qt

def client(tt):
    # Storage variables initial values
    variables=["entry_var_frequency_","var_waveform_","entry_var_amplitude_","entry_var_offset_","entry_var_carrying_frequency","entry_var_measured_frequency","entry_start_freq","entry_span_freq","entry_end_freq"]
    old_values=[]
    for variable in variables:
        exec("old_values.append(tt.get_{}())".format(variable))
        # Convert default values of entry controls to eng notation 
        if("entry" in variable):
            Qt.QMetaObject.invokeMethod(eval("tt._{}_line_edit".format(variable)), "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(eval("tt.{}".format(variable)))))
    while True:
        # Try to connect
        host = '192.168.137.8'
        port = 4242
        client_socket = socket.socket()
        try:
            client_socket.connect((host, port))
        except:
            pass
        if(client_socket.getsockname()[0] != "0.0.0.0"):
            # Connected
            print("Connected to server")
            while True:
                # Check if variables have changed to send the new values
                for i, variable in enumerate(variables):
                    if((eval("tt.get_{}()".format(variable))!=old_values[i]) & ("var" in variable)):
                        value=eval("tt.get_{}()".format(variable))
                        if(variable=="var_waveform_"):
                            value=value+100

                        message=variable + "=" + str(value) + ">" # Encoding message to send it
                        client_socket.send(message.encode())
                        # Register updated variable value
                        old_values[i]=eval("tt.get_{}()".format(variable))                    
                    # Check if "entry" controls text has been modified to change its color (indicating pending "enter" key)
                    if "entry" in variable:
                        try: # To catch when incorrect value is typed
                            if(eval("eng_notation.str_to_num(str(tt._{var_name}_line_edit.text()))!=float(tt.get_{var_name}())".format(var_name=variable))):
                                if(eval("tt._{}_tool_bar.styleSheet()".format(variable))!="QLabel {background-color: yellow}"):
                                    Qt.QMetaObject.invokeMethod(eval("tt._{}_tool_bar".format(variable)), "setStyleSheet", Qt.Q_ARG("QString", "QLabel {background-color: yellow}"))
                            else:
                                if(eval("tt._{}_tool_bar.styleSheet()".format(variable))!=""):
                                    Qt.QMetaObject.invokeMethod(eval("tt._{}_tool_bar".format(variable)), "setStyleSheet", Qt.Q_ARG("QString", ""))                        
                        except:
                            if(eval("tt._{}_tool_bar.styleSheet()".format(variable))!="QLabel {background-color: red}"):
                                    Qt.QMetaObject.invokeMethod(eval("tt._{}_tool_bar".format(variable)), "setStyleSheet", Qt.Q_ARG("QString", "QLabel {background-color: red}"))
                            pass
                    # Check if "start" has been pressed
                    btn_index=6
                    if((tt.get_btn_start()==1) & (tt.tab_widget_0_grid_layout_1.itemAt(btn_index).widget().text() == "Start")):
                        tt.tab_widget_0_grid_layout_1.itemAt(btn_index).widget().setText("Stop")
                        tt.set_btn_start(0)
                        tt.set_sweeping("True")
                    elif((tt.get_btn_start()==1) & (tt.tab_widget_0_grid_layout_1.itemAt(btn_index).widget().text() == "Stop")):
                        tt.tab_widget_0_grid_layout_1.itemAt(btn_index).widget().setText("Start")
                        tt.set_btn_start(0)
                        tt.set_sweeping("False")
                # client_socket.close()
