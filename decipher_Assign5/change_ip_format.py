f = open("inputs.txt", 'r')
ip = open("ipfile.txt", 'w')
for i in f.readlines():
	line = i.strip()
	line = i.split(' ')
	for word in line:
		if word != '\n':
			ip.write(word+'\n')
f.close()
ip.close()