# ref: http://kinokotimes.com/2016/11/07/easy_python_ping_pyping/

import pyping
from pyping.core import *

host = "ftp.tsukuba.wide.ad.jp"
RPing = pyping.ping(host)

#$BAw$j@h(B
print("ADD:"+str(RPing.destination))
#$BAw$j@h(BIP
print("AIP:"+str(RPing.destination_ip))
#$B:GBg1}I|IC(B
print("MAX:"+str(RPing.max_rtt)+"ms")
#$B:G>.1}I|IC(B
print("MIN:"+str(RPing.min_rtt)+"ms")
#$BJ?6Q1}I|IC(B
print("AVG:"+str(RPing.avg_rtt)+"ms")
