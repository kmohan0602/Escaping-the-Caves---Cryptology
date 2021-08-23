import time
import sys

f = open('output.log')
fout = open('outputs.txt','w')

lines = f.readlines()
# print(len(lines))
count =0
val =1
words=0
for l in lines:
    if(count > 322):
        if(len(l)==19 and l[0]!='>'):
            # print(l[2:17])
            temp = l[2:18] + ' '
            if val%128==0:
            	temp+='\n'
            fout.write(temp)
            val+=1
            words+=1
            if words==1024:
                break 
            # sys.exit()
        # if(count==10):
        #     sys.exit()
    count+=1


fout.close()
# for l in lines:
#     print(len(l))
    # sys.exit()
