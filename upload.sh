#! /bin/bash

sed -i 's+, 100, False, -1, \x27\x27)+, 100, False, -1)+g' radio_streaming_Pi.py
sed -i 's+, catch_exceptions=True)+)+g' radio_streaming_Pi.py
scp radio_streaming_Pi.py radio_streaming_Pi_epy_module_server.py root@192.168.137.8:/root