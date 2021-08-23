out_file=open("inputs.txt","w")
base_string="ff"*8

mapping={}
for i in range(16):
    key='{:0>4}'.format(format(i,"b"))
    value=chr(ord('f')+i)
    mapping[key]=value

for i in range(8):
    for j in range(128):
        binary_bits='{:0>8}'.format(format(j,"b"))
        left_part=binary_bits[:4]
        right_part=binary_bits[4:]
        dummy=list(base_string)
        dummy[i*2]=mapping[left_part]
        dummy[i*2+1]=mapping[right_part]
        to_write=''.join(dummy)
        out_file.write(to_write+' ')
    out_file.write('\n')

out_file.close()
