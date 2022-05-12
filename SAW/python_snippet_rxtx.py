print("Starting client and GUI")
import threading
threading.Thread(target=epy_module_client.client, daemon=True, args=(self,)).start()
threading.Thread(target=epy_module_sweep.sweep, daemon=True, args=(self,)).start()