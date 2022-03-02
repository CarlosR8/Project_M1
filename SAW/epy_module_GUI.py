# this module will be imported in the into your flowgraph
import tkinter as tk
import tkinter.font as tkFont

def gui(tt):
    while True:
        window = tk.Tk()
        label = tk.Label(text="Current station: ")
        label.grid(column=0, row=0, columnspan=2)

        station_number = tk.StringVar()
        
        # Entry_Control = tk.Entry(window, textvariable=station_number, validate="key", validatecommand=callback, justify='center')
        Entry_Control = tk.Entry(window, textvariable=station_number, justify='center')
        Entry_Control.grid(column=0, row=1, columnspan=2)

        button = tk.Button(text="Change", command= lambda: changeStation(tt,Entry_Control.get()))
        button.grid(column=0, row=2)
        close = tk.Button(text="Close", command= lambda: closeButton(window))
        close.grid(column=1, row=2)

        window.mainloop()

def callback():
    # print(station_number.get()) #Triggered by typing
    return True

def changeStation(tt, station):
    try:
        tt.stream_variable = "True"
        # tt.set_stream_variable(tt.stream_variable)
        tt.set_stream_variable("True")
        tt.station = station
        tt.set_station(tt.station)
        print(tt.get_station())
        # host = '192.168.137.8'
        # port = 4242  # socket server port number

        # client_socket = socket.socket()  # instantiate
        # client_socket.connect((host, port))  # connect to the server

        # message = input(" -> ")  # take input

        # while message.lower().strip() != 'bye':
        #     client_socket.send(message.encode())  # send message
        #     data = client_socket.recv(1024).decode()  # receive response

        #     print('Received from server: ' + data)  # show in terminal

        #     message = input(" -> ")  # again take input

        # client_socket.close()  # close the connection
    except:
        print("Error!")

def closeButton(window):
    window.quit()