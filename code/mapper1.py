#This is the mapper
import sys

# Sample line
# 10.223.157.186 - - [15/Jul/2009:15:50:35 -0700] "GET /assets/js/lowpro.js HTTP/1.1" 200 10469

for line in sys.stdin:
    ip=line.split(' ')[0]
    if len(line.split('\"'))!=3:
        continue
    req=line.split('\"')[1].split('\"')[0]
    if len(req.split(' '))!=3:
        continue
    page=req.split(' ')[1]
    # print 'ip',ip
    # print 'req',req
    # print 'file', fi
    print "{0}\t{1}".format(page, 1)