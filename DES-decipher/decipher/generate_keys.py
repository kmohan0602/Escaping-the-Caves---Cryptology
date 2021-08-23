from math import *

maxy=int(pow(2,20))

dummy="XX1XX1XXX10X1X10XXX11XX10X0X0000111X00011011X11X0100X011"

file=open('possible_keys.txt','w')

for i in range(maxy):
	temp=list(dummy)
	s=str(bin(i))[2:].zfill(20)
	# print(s)
	curr=0
	for q in range(56):
		if temp[q]=='X' or temp[q]=='Z':
			temp[q]=s[curr]
			curr+=1
	s=('').join(temp)
	file.write(s+'\n')