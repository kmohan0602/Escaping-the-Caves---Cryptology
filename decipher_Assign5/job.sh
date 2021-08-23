!#/bin/bash

python3 generate_inputs.py 
python3 change_ip_format.py 
chmod 777 run.exp
./run.exp 
python3 clean.py
pip3 install pyfinite
python3 brute_force.py 