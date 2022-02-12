# this module will be imported in the into your flowgraph
from ctypes import alignment
from email import message
import socket

def client(tt):
    while True:
        # Storage variables initial values
        test_variable = "False"
        # Try to connect
        host = '192.168.137.8'
        port = 4242
        client_socket = socket.socket()
        client_socket.connect((host, port))
        while True:
            if(client_socket.getsockname()[0] != "0.0.0.0"):
                # Connected
                print("Connected to server")
                # Check if variables have change
                print(tt.get_stream_variable())
                if(tt.get_stream_variable() != test_variable):
                    print("sending message")
                    test_variable = tt.get_stream_variable() # Store current value
                    message_ = "test!"
                    # client_socket.send(message_.encode())
                    # client_socket.close()



# def client(tt):
#     while True:
#         # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         #     print(testing)
#         #     s.connect(('192.168.137.8', 4242))
#         #     if(testing != ""):
#         #         print(testing)
                
#         #         # s.sendall(b'Hello, world')
#         #         # s.sendall(b'{}'.format(station + ">"))
#         #         s.send(testing.encode())
#         #         data = s.recv(1024)

#         #         print('Received', repr(data))
#         #         print(testing)
#         #         testing=""
#         host = '192.168.137.8'
#         port = 4242  # socket server port number

#         client_socket = socket.socket()  # instantiate
#         print(client_socket.getpeername())
#         client_socket.connect((host, port))  # connect to the server
#         # if(client_socket.raddr):
#             # print("conncted")
#         print(client_socket.getpeername())

#         message = "test..."  # take input
#         # print(tt.get_stream_variable())
#         # while tt.get_stream_variable() == 'True':
#             # print("sending message")
#         client_socket.send(message.encode())  # send message
        
#         data = client_socket.recv(1024).decode()  # receive response
        
#             # print('Received from server: ' + data)  # show in terminal

#             # message = input(" -> ")  # again take input

#         # client_socket.close()  # close the connection