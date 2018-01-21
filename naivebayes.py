data = [line.split(',') for line in open("Referees-Training.csv").read().split('\n')]
heads = data[0]
data = data[1:-1]

data_points = len(data)
#P(bias)
pb=0
# num bias
nb=0
# num not bias
nnb=0
#P(ref[i]=1|bias)
skip = 3
prefb = [0]*(len(heads)-(4+skip))
#P(ref[i]=1|not bias)
prefnb = [0]*(len(prefb))

for i in range(len(data)):
    line = data[i]
    #print(i)
    if line[-1] == "0":
        nnb+=1
    elif line[-1] == "1":
        nb+=1
    for ref in range(len(prefb)):
        if line[ref+skip] == "1":
            if line[-1] == "0":
                prefnb[ref]+=1
            elif line[-1] == "1":
                prefb[ref]+=1
print(nb,nnb)
for i in range(len(prefb)):
    prefb[i]/=nb
    prefnb[i]/=nnb
pb = nb/(nb+nnb)
print("P(Bias) = {}".format(pb))
print("P(not Bias) = {}".format(1-pb))
for i in range(len(prefb)):
    print("P(Ref #{}|bias) = {}".format(i,prefb[i]))
    print("P(Ref #{}|not bias) = {}".format(i,prefnb[i]))

    
def prhomeltaway(x):
    #x is a vector corresponding to which ref is present for the game
    pxny=1
    for i,feature in enumerate(x):
        if feature == 1:
            pxny*=prefb[i]
        elif x == 0:
            pxny*=(1-prefb[i])
    pxnyc = 1
    for i,feature in enumerate(x):
        if feature == 1:
            pxnyc*=prefnb[i]
        elif feature == 0:
            pxnyc*=(1-prefnb[i])
    return pxny*pb/(pxny*pb+(1-pb)*pxnyc)

# num correct predictions    
ncp = 0
# num incorrect predictions
nip = 0
predbias =0
minp = 0.0000000001
maxp = 0.9999999999
while maxp-minp>.00000000001:
    ncp = 0
    nip = 0
    predbias =0
    tipping_pt = (maxp+minp)/2
    for line in data:
        if(prhomeltaway([int(ref) for ref in line[skip:len(prefb)+1]])>=tipping_pt):
            predbias+=1
            
        if ("1" if prhomeltaway([int(ref) for ref in line[skip:len(prefb)+1]])>=tipping_pt else "0") == (line[-1]):
            ncp+=1
        else:
            nip+=1
    if predbias < nb:
        maxp = tipping_pt
    else:
        minp = tipping_pt
tipping_pt = (maxp+minp)/2
print("\n")
print("tipping pt:",tipping_pt)
print("total games percent bias:",(nb/(nb+nnb)))
print("training results")
print("correct predictions",ncp)
print("incorrect predictions",nip)
print("accuracy",ncp/(ncp+nip))
print("predicted games percent bias:",predbias/(ncp+nip))
print("\n")

ncp = 0
nip = 0
nb = 0
nnb = 0
predbias = 0
vdata = [line.split(',') for line in open("Referees-Validation.csv").read().split('\n')]
vdata = vdata[1:-1]
for line in vdata:
    if(prhomeltaway([int(ref) for ref in line[skip:len(prefb)+1]])>=tipping_pt):
        predbias+=1
    
    if(line[-1]=="1"):
        nb+=1
    else:
        nnb+=1
    
    if ("1" if prhomeltaway([int(ref) for ref in line[skip:len(prefb)+1]])>=tipping_pt else "0") == (line[-1]):
        ncp+=1
    else:
        nip+=1
print("validation results")
print("total games percent bias:",(nb/(nb+nnb)))
print("correct predictions",ncp)
print("incorrect predictions",nip)
print("accuracy",ncp/(ncp+nip))
print("predicted games percent bias:",predbias/(ncp+nip))