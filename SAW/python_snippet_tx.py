print("Starting server")
import threading
threading.Thread(target=epy_module_server.server,args=(self,)).start()
from subprocess import Popen
Popen(['python', 'rx_Pi.py'])