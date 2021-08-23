#!/bin/bash

python3 clean.py

g++ output_binary.cpp -o output_binary
./output_binary

g++ compute_xor.cpp -o compute_xor
./compute_xor

g++ sbox.cpp -o sbox
./sbox

python3 generate_keys.py

g++ DES_bruteforce.cpp -o brute
./brute

g++ DES_decryption.cpp -o decrypt 
./decrypt