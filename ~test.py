
#print(len("abcdefghijklmnopqrstuvwyxABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-=_+][}{|;:,./<>?~"))

def rnd(n, base=5):
    return int(base*round(float(n)/base))

def myrnd(x, num=5):
    print(x//num*num)

l = 9
print(myrnd(l), rnd(l))

for i in range(0,100,5):
    print(~3, -3, ..., Ellipsis)