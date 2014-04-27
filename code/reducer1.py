import sys

this=None
last=None
hit=0

for line in sys.stdin:
    data=line.split('\t')
    if len(data)!=2:
        continue
    page=data[0]
    this=page
    if not this==last and not last==None:
        print "{0}\t{1}".format(last, hit)
        hit=0
    hit+=1
    last=this
print "{0}\t{1}".format(last, hit)


