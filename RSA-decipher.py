DIM_X = 5   # X dimension of state matrix
DIM_Y = 5   # Y dimesion of state matrix
DIM_Z = 64  # Z dimension of state matrix
import numpy as np 
CHI_inverse = {   # chin inverse mapping
        '00000':'00000',
        '00101':'00001',
        '01010':'00010',
        '01011':'00011',
        '10100':'00100',
        '10001':'00101',
        '10110':'00110',
        '10111':'00111',
        '01001':'01000',
        '01100':'01001',
        '00011':'01010',
        '00010':'01011',
        '01101':'01100',
        '01000':'01101',
        '01111':'01110',
        '01110':'01111',
        '10010':'10000',
        '10101':'10001',
        '11000':'10010',
        '11011':'10011',
        '00110':'10100',
        '00001':'10101',
        '00100':'10110',
        '00111':'10111',
        '11010':'11000',
        '11101':'11001',
        '10000':'11010',
        '10011':'11011',
        '11110':'11100',
        '11001':'11101',
        '11100':'11110',
        '11111':'11111',
        }

def chi_inverse(state):
	state = state.astype(np.int32)
	for z in range(DIM_Z):
		for x in range(DIM_X):
			ret = CHI_inverse[''.join([str(elem) for elem in state[x,:,z]])]
			state[x, :, z] = [int(elem) for elem in ret]
	return state

def pi_inverse(state):
	state = state.astype(np.int32)
	nblock=np.zeros((5,5,64),dtype=np.int32)
	for k in range(DIM_Z):
		for j in range(DIM_Y):
			for i in range(DIM_X):
				nblock[i,j,k] = state[j,(2*i+3*j)%5,k]
	return nblock

def theta(face):    # function that applies theta function on a XY plane
	col_parity=np.zeros((DIM_X), dtype=np.int32)
	for i in range(DIM_X): 
		for j in range(DIM_Y):
			col_parity[i]^=face[i,j]

	for i in range(DIM_X):
		for j in range(DIM_Y):
			face[i,j]^=(col_parity[(i+4)%DIM_X])^(col_parity[(i+1)%DIM_X])

	return face

def theta_inverse(state):
	state=state.astype(np.int32)
	ans_matrix=np.zeros((DIM_X,DIM_Y,DIM_Z), dtype=np.int32)
	for k in range(DIM_Z):
		current_phase=state[:,:,k]
		for i in range(32):
			to_invert=[int(n) for n in ("{0:0" + str(DIM_X) + "b}").format(i)]
			temp_copy=current_phase.copy()
			for col_num in range(5):
				if to_invert[col_num]:
					temp_copy[col_num,:]=abs(1-temp_copy[col_num,:])
			
			theta_applied=theta(temp_copy)
			if (theta_applied==current_phase).all():
				
				ans_matrix[:,:,k]=temp_copy
				break
	return ans_matrix


def digest_inverse(state,num_rounds=24):   # Function that inverts the state matrix in 24 rounds
	for round in range(num_rounds):
		state = chi_inverse(state) # calling chi_inverse
		state = pi_inverse(state)  # calling pi inverse
		state = theta_inverse(state) # calling theta inverse
	return state


bin_mapping={      # mapping for hexa decimal numbers to four bit binary strings
	'0':'0000',
	'1':'0001',
	'2':'0010',
	'3':'0011',
	'4':'0100',
	'5':'0101',
	'6':'0110',
	'7':'0111',
	'8':'1000',
	'9':'1001',
	'A':'1010',
	'B':'1011',
	'C':'1100',
	'D':'1101',
	'E':'1110',
	'F':'1111',
}

def final_test(sample):
	text=''
	if sample == 0:  # given hash value for password
		print('The invertion of hash value given in level:7')
		text="616860600000000006868A0365656EE667EFEB6F65656EE606878B0F65656EE60001010C0000000006878B0F65656EE66169616C000000006168606000000000"
	if sample == 1:  # hash value for dummy message "abcdefghijklmnop" which is 16 charecters long
		print('')
		print('The inversion of hash value for a dummy input string: "abcdefghijklmnop" ')
		text="68646C626A666E60000000000000000169656D636B676FE101010101010101810101010101010180010101010101018169656D636B676FE068646C626A666E60"

	text = list(text)
	bin_text = ''
	for letter in text:
		bin_text+=(bin_mapping[letter][::-1])

	bin_text+= "0"*64	
	bin_text = [int(i) for i  in bin_text]

	temp = np.zeros((5,5,64),dtype=np.int32)
	for k in range(576):
		temp[k//(64*5)][(k//64) % 5][k%64] = bin_text[k];   # creating state matrix using hash value
	return temp


for i in range(2):
	f_state = final_test(i)
	ans=digest_inverse(f_state,num_rounds=24)
	ans = ans.flatten()
	stri=""
	for i in ans:
		stri+=str(i)

	##*******************************************************************##
	password = stri

	reverse_text=''
	for i in range(0,len(password),8):
		chunk=password[i:i+8]
		chunk=int(chunk,2)

		if not ((chunk>=97 and chunk<=122) or (chunk>=65 and chunk<=90)): 
			chunk=35

		reverse_text+=chr(chunk)

	print(reverse_text)

























