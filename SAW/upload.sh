#! /bin/bash
rm -f ./Symbolic\ links/epy_module_client.py
rm -f ./Symbolic\ links/epy_module_server.py
rm -f ./Symbolic\ links/epy_module_shared_variable.py

cp ./Symbolic\ links/epy_module_client*.py ./Symbolic\ links/epy_module_client.py
cp ./Symbolic\ links/epy_module_server*.py ./Symbolic\ links/epy_module_server.py
cp ./Symbolic\ links/epy_module_shared_variable*.py ./Symbolic\ links/epy_module_shared_variable.py
scp ./rx_Pi.py ./tx_Pi.py ./Symbolic\ links/epy_module_server.py ./Symbolic\ links/epy_module_shared_variable.py root@192.168.137.8:/root