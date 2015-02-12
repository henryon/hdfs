


#!/usr/bin/env python
#author by henry.wen
""" this script mainly to check the fuse process and make sure it work ,also can't exceed the memory threshhold"""


source /etc/profile
FILE=/root/test
TIMEOUT=10

echo "check memory"

MEM=`ps -e  -o pid,rss,comm|grep fus[e]|awk '{print $2}'`
PID=`ps -e  -o pid,rss,comm|grep fus[e]|awk '{print $1}'`

if [ ${MEM}  -gt 8000000 ]; then

    echo "the process ${PID} memory usage over 8G, we have to remount it "
    kill -9 ${PID}  && umount -l /hdfs/hp3

    if [ $? -eq 0 ]; then
        echo "we  have to remount /hdfs/hp3"
        /opt/letv/fuse-dfs/bin/fuse dfs://10.150.160.126:9000 ro /hdfs/hp3  &
    else
        echo "we  can't umount the /hdfs/hp3 correctly,pay attention for this"
        /opt/letv/fuse-dfs/bin/fuse dfs://10.150.160.126:9000 ro /hdfs/hp3  &
    fi
    exit 1
else

    echo "it looks like the ${PID} memory usage hasn't reach the threshhold (8G)"
fi


df -h > ${FILE} 2>&1 & { sleep ${TIMEOUT} ; eval 'kill -9 $!' > /dev/null;}
echo "check  mount point "
num=`grep "hdfs/hp3" ${FILE}|egrep -iv "Input|connected"|wc -l`


if [ $num -eq 0 ] ;then
   echo "we have to remount hdfs mount point"
   sync && sync && umount -l  /hdfs/hp3
   sleep 2
    /opt/letv/fuse-dfs/bin/fuse dfs://10.150.160.126:9000 ro /hdfs/hp3  &
else
   echo "the mount point is working well"
	