#!/usr/bin/bash
#author by henrywen
# Date:2014-8-20
#this script to auto-mount the hdfs mount point on UTS server

source /etc/profile
FILE=/root/test
TIMEOUT=10

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
fi