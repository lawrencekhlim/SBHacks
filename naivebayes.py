data = [line.split(',') for line in open("Referees.csv").read().split('\n')]
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
prefb = [0]*78
#P(ref[i]=1|not bias)
prefnb = [0]*78

for i in range(len(data)):
    line = data[i]
    #print(i)
    if line[-1] == "FALSE":
        nnb+=1
    elif line[-1] == "TRUE":
        nb+=1
    for ref in range(len(prefb)):
        if line[ref+1] == "TRUE":
            if line[-1] == "FALSE":
                prefnb[ref]+=1
            elif line[-1] == "TRUE":
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

    
for line in data:
    if str(prhomeltaway([0 if ref == "FALSE" else 1 for ref in line[1:len(prefb)+1]])>=.5).upper() == line[-1]:
        ncp+=1
    else:
        nip+=1
print(ncp,nip)
    
