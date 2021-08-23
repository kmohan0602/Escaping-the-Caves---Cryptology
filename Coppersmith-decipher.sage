# function is taken from github: https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/coppersmith.sage
def coppersmith_howgrave_univariate(pol, modulus, beta, mm, tt, XX):
    
    dd = pol.degree()
    nn = dd * mm + tt

    polZ = pol.change_ring(ZZ)
    x = polZ.parent().gen()

    # compute polynomials
    gg = []
    for ii in range(mm):
        for jj in range(dd):
            gg.append((x * XX)**jj * modulus**(mm - ii) * polZ(x * XX)**ii)
    for ii in range(tt):
        gg.append((x * XX)**ii * polZ(x * XX)**mm)

    # construct lattice B
    BB = Matrix(ZZ, nn)

    for ii in range(nn):
        for jj in range(ii+1):
            BB[ii, jj] = gg[ii][jj]

    # LLL
    BB = BB.LLL()

    # transform shortest vector in polynomial
    new_pol = 0
    for ii in range(nn):
        new_pol += x**ii * BB[0, ii] / XX**ii

    # factor polynomial
    potential_roots = new_pol.roots()
    
    # test roots
    roots = []
    for root in potential_roots:
        if root[0].is_integer():
            result = polZ(ZZ(root[0]))
            if gcd(modulus, result) >= modulus^beta:
                roots.append(ZZ(root[0]))

    return roots

e = 5
N = 84364443735725034864402554533826279174703893439763343343863260342756678609216895093779263028809246505955647572176682669445270008816481771701417554768871285020442403001649254405058303439906229201909599348669565697534331652019516409514800265887388539283381053937433496994442146419682027649079704982600857517093
C = 23701787746829110396789094907319830305538180376427283226295906585301889543996533410539381779684366880970896279018807100530176651625086988655210858554133345906272561027798171440923147960165094891980452757852685707020289384698322665347609905744582248157246932007978339129630067022987966706955482598869800151693

codes=[['59' ,'6f','75','20','73','65','65','20'],
        ['61', '20', '47', '6f', '6c', '64', '2d', '42'],
        ['75', '67', '20', '69', '6e', '20', '6f', '6e'],
        ['65', '20', '63', '6f', '72', '6e', '65', '72'],
        ['2e', '20', '49', '74', '20', '69', '73', '20'],
        ['74', '68', '65', '20', '6b', '65', '79', '20'],
        ['74', '6f', '20', '61', '20', '74', '72', '65'],
        ['61', '73', '75', '72', '65', '20', '66', '6f'],
        ['75', '6e', '64', '20', '62', '79']]

pad_string=""
pad_string_binary=""

for line in codes:
    # line=line.split()
    for pair in line:
        # '2'->2->0010>-string
        x='{0:04b}'.format(int(pair[0],16))
        y='{0:04b}'.format(int(pair[1],16))
        joined=x+y
        joined=int(joined,2)
        # print(chr(joined),end='')
        pad_string+=chr(joined)
        pad_string_binary+= (x+y)

print("The padding applied is: {}".format(pad_string))

root=0
cur_length=0
set_mod_n=Zmod(N)

while not(root):
    P.<M> = PolynomialRing(set_mod_n)
    polynomial=((int(pad_string_binary,2)<<cur_length)+M)^e-C
    dd=polynomial.degree()

    beta=1
    epsilon=beta/7
    mm = ceil(beta**2 / (dd * epsilon))     
    tt = floor(dd * mm * ((1/beta) - 1))    
    XX = ceil(N**((beta**2/dd) - epsilon))

    root=coppersmith_howgrave_univariate(polynomial, N, beta, mm, tt, XX)
    cur_length+=4
    if root:
        root='{0:b}'.format(root[0])
        print(f"The Root is: {root}")
        break

padded_root="00"+root

print("The PassWord is: ",end='')
for i in range(0,len(padded_root),8):
    chunk=padded_root[i:i+8]
    chunk=int(chunk,2)
    print(chr(chunk),end='')
