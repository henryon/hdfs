#!/bin/bash
set -e
echo "this script is used for deleting the file which you want to delete on HDSF file system,please be sure attention for this,as if you deleted file ,you can't recove
ry it in a short time , or even you can recovery it ,it will take lots of time to do that"


if [ $# -ne 2 ]; then
    echo "Error ,you have to specify two parameter for this script"
    echo "Usage: `basename $0` IP filepath"
    exit 1
 fi
 IP=$1
 FILE=$2

 delete() {
     ssh hadoop@'$1' "hadoop dfs -rmr --skipTrash   '$2'" 
     echo "Good"
 }

 verify() {
  ssh hadoop@$1  "hadoop dfs -ls   $2" 
 }

case $IP in 
    '10.150.140.34')
        verify  $IP  $FILE
        if [ $? = 0 ]; then
                echo "the file $FILE doesn't exist on this HDFS, please verify "
        else
            delete $IP  $FILE
            if  [ $? = 0 ]; then
                echo "Successful to delete file $FILE"
            else
                echo "delete the file $FILE failed, please attention"
            fi
         fi ;;
    '10.180.1.133')
        verify  $IP  $FILE
        if [[ $?  != 0 ]]; then
                echo "the file $2 doesn't exist on this HDFS, please verify "
        else
            delete  $IP  $FILE
            if  [ $? != 0 ]; then
                echo "Successful to delete file $FILE"
            else
                echo "delete the file $FILE failed, please attention"
            fi
         fi ;;
    *)
        echo 'Your are input the wrong hdfs IP' ;;
esac