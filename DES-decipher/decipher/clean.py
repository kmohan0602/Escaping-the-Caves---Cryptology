import time
import sys

f = open('output.log')
fout = open('cleanout.txt','w')

lines = f.readlines()
# print(len(lines))
count =0

for l in lines:
    if(count > 620):
        if(len(l)==19 and l[0]!='>'):
            # print(l[2:17])
            temp = l[2:18] + '\n'
            fout.write(temp)
            # sys.exit()
        # if(count==10):
        #     sys.exit()
    count+=1


fout.close()
# for l in lines:
#     print(len(l))
    # sys.exit()