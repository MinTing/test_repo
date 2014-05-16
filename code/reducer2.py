#This is the reducer
import sys

this=None
last=None
hit=0
maxx=0
maxf=''

for line in sys.stdin:
    data=line.strip().split('\t')
    if len(data)!=2:
        continue
    page=data[0]
    this=str(page)
    # print 'this ', this, 'last ', last
    if not last==None:
        if not this in last and not last in this:
            # print 'change'
            if hit>maxx:
                maxx=hit
                maxf=last
            print "{0}\t{1}".format(last, hit)
            hit=0
    hit+=1
    last=this
# Complete reading lines
if hit>maxx:
    maxx=hit
    maxf=last
print "{0}\t{1}".format(last, hit)

print "\n{0}\t{1}".format(maxf, maxx)


