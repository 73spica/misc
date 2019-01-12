# ref: http://kinokotimes.com/2016/11/07/easy_python_ping_pyping/

import pyping
from pyping.core import *

host = "ftp.tsukuba.wide.ad.jp"
RPing = pyping.ping(host)

#送り先
print("ADD:"+str(RPing.destination))
#送り先IP
print("AIP:"+str(RPing.destination_ip))
#最大往復秒
print("MAX:"+str(RPing.max_rtt)+"ms")
#最小往復秒
print("MIN:"+str(RPing.min_rtt)+"ms")
#平均往復秒
print("AVG:"+str(RPing.avg_rtt)+"ms")
