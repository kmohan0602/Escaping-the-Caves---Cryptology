# !pip install pyfinite
import numpy as np
import random
import sympy as sp
from numpy.linalg import matrix_rank
np.set_printoptions(threshold=np.inf)
from pyfinite import ffield

inverse_mapping={}
for i in range(16):
    key='{:0>4}'.format(format(i,"b"))
    value=chr(ord('f')+i)
    inverse_mapping[key]=value

#we need a func to convert a byte to two chars
def string_from_byte(Byte):
    bit_string='{:0>8}'.format(format(Byte,"b"))
    return inverse_mapping[bit_string[:4]]+inverse_mapping[bit_string[4:]]

#A function to convert a full block (16 chars) to hex values
def block_to_hex(block):
    plain=""
    for i in range(0,len(block),2):
        st=block[i:i+2]
        plain+=chr(16*(ord(st[0]) - ord('f')) + ord(st[1]) - ord('f'))
    return plain

#We need functions to perform functions to perform Field calculations
dp_exp=[[-1]*128 for i in range(128)]

field=ffield.FField(7)

def Sum(a,b):
	return int(a)^int(b)

def Product(a,b):
	return field.Multiply(a,b)

def power(base,exp):
	if dp_exp[base][exp] != -1:
		return dp_exp[base][exp]

	ans=0
	if exp==0:
		return 1
	elif exp==1:
		return base
	elif exp%2==0:
		sqrt=power(base,exp>>1)
		ans=Product(sqrt,sqrt)
	else:
		sqrt=power(base,exp>>1)
		ans=Product(sqrt,sqrt)
		ans=Product(base,ans)

	dp_exp[base][exp]=ans
	return ans

def vector_addition(a,b):
	ans=[0]*8
	for i, (v1,v2) in enumerate(zip(a,b)):
		ans[i]=Sum(v1,v2)
	return ans

def scalar_multiply(v,element):
	ans=[0]*8
	for i in range(8):
		ans[i]=Product(v[i],element)
	return ans

def Linear_transform(matrix, exp_list):
    ans = [0]*8
    for row, elem in zip(matrix, exp_list):
        ans = vector_addition(scalar_multiply(row, elem), ans)
    return ans

possible_exp=[[] for i in range(8)]
possible_diag=[[[] for i in range(8)] for j in range(8)]

ip_file=open("inputs.txt","r")
op_file=open("outputs.txt","r")

for index, (ip_line,op_line) in enumerate(zip(ip_file.readlines(),op_file.readlines())):
	ip_string,op_string=[],[]

	for ib,ob in zip(ip_line.strip().split(" "),op_line.strip().split(" ")):
		ip_string.append(block_to_hex(ib)[index])
		op_string.append(block_to_hex(ob)[index])

	for i in range(1,127):
		for j in range(0,128):
			booly=True
			for ips,ops in zip(ip_string,op_string):
				if ord(ops)!=power(Product(power(Product(power(ord(ips),i),j),i),j),i):
					booly=False
					break
			if booly:
				possible_exp[index].append(i)
				possible_diag[index][index].append(j)

ip_file = open("inputs.txt", 'r')
op_file = open("outputs.txt", 'r')
for index, (ip_line, op_line) in enumerate(zip(ip_file.readlines(), op_file.readlines())):
    if index > 6 :
        break
    ip_string = []
    op_string = []
    for ib,ob in zip(ip_line.strip().split(" "),op_line.strip().split(" ")):
        ip_string.append(block_to_hex(ib)[index])
        op_string.append(block_to_hex(ob)[index+1])
    for i in range(1, 128):
        for p1, e1 in zip(possible_exp[index+1], possible_diag[index+1][index+1]):
            for p2, e2 in zip(possible_exp[index], possible_diag[index][index]):
                flag = True
                for ips, ops in zip(ip_string, op_string):
                    if ord(ops) != power(Sum(Product(power(Product(power(ord(ips), p2), e2), p2), i) ,Product(power(Product(power(ord(ips), p2), i), p1), e1)), p1):
                        flag = False
                        break
                if flag:
                    possible_exp[index+1] = [p1]
                    possible_diag[index+1][index+1] = [e1]
                    possible_exp[index] = [p2]
                    possible_diag[index][index] = [e2]
                    possible_diag[index][index+1] = [i]


def mimic_cipher(plaintext,linear_matrix, exponent_matrix):
	plaintext=[ord(char) for char in plaintext]
	ans=[0]*8
	for index,element in enumerate(plaintext):
		ans[index]=power(element,exponent_matrix[index])

	ans=Linear_transform(linear_matrix,ans)
	for index,element in enumerate(ans):
		ans[index]=power(element,exponent_matrix[index])
	ans=Linear_transform(linear_matrix,ans)
	for index,element in enumerate(ans):
		ans[index]=power(element,exponent_matrix[index])
	return ans

for index in range(6):
	offset=index+2

	list_expo=[li[0] for li in possible_exp]
	linear_transform_list=[[0 for i in range(8)] for j in range(8)]

	for i in range(8):
		for j in range(8):
			if len(possible_diag[i][j])==0:
				linear_transform_list[i][j]=0
			else:
				linear_transform_list[i][j]=possible_diag[i][j][0]
	ip_file=open("inputs.txt","r")
	op_file=open("outputs.txt","r")
	for index, (ip_line,op_line) in enumerate(zip(ip_file.readlines(),op_file.readlines())):
		if index > abs(offset-7):
			continue
		ip_string=[block_to_hex(block) for block in ip_line.strip().split(" ")]
		op_string=[block_to_hex(block) for block in op_line.strip().split(" ")]

		for i in range(1,128):
			linear_transform_list[index][index+offset]=i
			booly=True
			for ips,ops in zip(ip_string,op_string):
				if mimic_cipher(ips,linear_transform_list,list_expo)[index+offset] != ord(ops[index+offset]):
					booly=False
					break
			if booly==True:
				possible_diag[index][index+offset]=[i]
		ip_file.close()
		op_file.close()

linear_transform_list=[[0 for i in range(8)] for j in range(8)]
for i in range(8):
	for j in range(8):
		if len(possible_diag[i][j])==0:
			linear_transform_list[i][j]=0
		else:
			linear_transform_list[i][j]=possible_diag[i][j][0]

print("LINEAR TRANSFORM MATRIX : ")
for i in range(8):
	for j in range(8):
		print('{: >4}'.format(linear_transform_list[j][i]), end=' ')
	print(' ')

print("EXPONENT MATRIX :")
print(list_expo)

def password_breaker(password):
    left_pass=password[:16]
    right_pass=password[16:]
    left_pass = block_to_hex(left_pass)
    right_pass=block_to_hex(right_pass)
    ans_left = ""
    ans_right= ""
    for i in range(8):    #ind
        for j in range(128):  #ans
            inp = ans_left + string_from_byte(j)+(16-len(ans_left)-2)*'f'
            if ord(left_pass[i]) == mimic_cipher(block_to_hex(inp), linear_transform_list, list_expo)[i]:
                ans_left += string_from_byte(j)
                break
    
    for i in range(8):    #ind
        for j in range(128):  #ans
            inp = ans_right + string_from_byte(j)+(16-len(ans_right)-2)*'f'
            if ord(right_pass[i]) == mimic_cipher(block_to_hex(inp), linear_transform_list, list_expo)[i]:
                ans_right += string_from_byte(j)
                break

    return ans_left+ans_right

ciphered_password="ijligfklhhhifhkukkmmhrmtfgloglip"

print(f"Decrypted Password: {block_to_hex(password_breaker(ciphered_password))}")