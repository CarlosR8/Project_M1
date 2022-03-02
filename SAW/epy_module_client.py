# this module will be imported in the into your flowgraph
import socket

def client(tt):
    while True:
        # Storage variables initial values
        variables=["frequency_","waveform_","amplitude_","offset_","sample_rate","carrying_frequency","measured_frequency"]
        old_values=[]
        new_values=[]
        for variable in variables:
            exec("old_values.append(tt.get_{}())".format(variable))
        
        new_values = old_values
        # Try to connect
        host = '192.168.137.8'
        port = 4242
        client_socket = socket.socket()
        client_socket.connect((host, port))
        if(client_socket.getsockname()[0] != "0.0.0.0"):
            # Connected
            print("Connected to server")
            while True:
                # Check if variables have changed
                for i, variable in enumerate(variables):
                    if(eval("tt.get_{}()".format(variable))!=old_values[i]):
                        value=eval("tt.get_{}()".format(variable))
                        if(variable=="waveform_"):
                            value=value+100

                        message=variable + "=" + str(value) + ">"
                        client_socket.send(message.encode())
                        # Register new variable value
                        old_values[i]=eval("tt.get_{}()".format(variable))

                # client_socket.close()
