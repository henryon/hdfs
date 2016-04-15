#!/bin/bash
#Version 0.0.1
#author HenryWen
#Notes: Please run this script as hdfs account

#define the logfile format
DATE=`date +%Y-%m-%d`
LOGFILE=HDFS-BACKUP.log.${DATE}

#get the hdfs directory from command line
DIR=$1

##get the s3 local directory(/s3mnt/PATH-ON-BUCKET), along with s3 bucket directory /PATH-ON-BUCKET
S3LOCALDIR=${DIR//\/data\//\/s3mnt\/}
S3SERVERDIR=${DIR//\/data\//}

##get s3 local file path prefix
PREFIX=${S3LOCALDIR%%}

##define the temp files for s3/hdfs temp file list, also with hdfs temp file list.
S3LIST=RC${S3DIR//\//-}
HDFSLIST=RC${DIR//\//-}

#define the start function
start() {
	echo "starting sync hdfs file"  >> ${LOGFILE}  2>&1
	setsid hadoop dfs -get ${DIR} ${S3LOCALDIR} &
}

##define this function make sure only one process is running for each directory
verify_process() {
	echo "checking the processing make sure it running"  >> ${LOGFILE}  2>&1
	LINE=`ps -ef|grep "${S3LOCALDIR}\b"|grep -v grep|wc -l`
	if [ ${LINE} -eq 1 ]; then
   		echo "the process running"  >> ${LOGFILE}  2>&1
        else
   		echo "the process not running, Please restart it"  >> ${LOGFILE}  2>&1
    		start
	fi
}

check_sync_stat() {
	#Get s3 bucket file and HDFS file. then Compare by file lines.if HDFS record line less or equal s3 lines. continue check synced files size .
	##if the records are full match,it is oK. 
	##and if some files doesn't match, delete them firstly. then retry. 
	##otherwise start get file.

	echo "Get s3 bucket result"	   >> ${LOGFILE}  2>&1
	aws s3 ls s3://es-hdfs-backup/${S3SERVERDIR}/ > ${S3LIST}
	perl -i.bak -nale   'print @F[2],"\t",@F[3] if scalar @F > 3 '  ${S3LIST}
	S3LISTLINE=`wc -l ${S3LIST}|cut -d" " -f1`  >>${LOGFILE}  2>&1
	echo "Get HDFS result"  >> ${LOGFILE}  2>&1
	hadoop dfs -ls ${DIR} |awk 'NF>3{print $5,"\t",$NF}' >  ${HDFSLIST}
	perl  -p -i.bak -e "s#${DIR}/##"  ${HDFSLIST}
 	HDFSLISTLINE=`wc -l ${HDFSLIST}|cut -d" " -f1`

	if [ ${HDFSLISTLINE} -le ${S3LISTLINE} ]; then
		echo "Backup seems ok. Let's coqmpare the result "  >> ${LOGFILE}  2>&1
		awk 'NR==FNR{a[$2]=$1}NR>FNR{ if ( $1 != a[$2] && a[$2] != " ") print $2 > "TEMP" }' ${HDFSLIST}  ${S3LIST}
		CMPLINE=`wc -l TEMP|cut -d" " -f1`

		if [ ${CMPLINE} -ne 0 ]; then
			echo "some files need rsync,first we delete them on s3 bucket. Then start()"  >> ${LOGFILE}  2>&1
			#add file path from hdfs file list
			sed -i.bak -e "s#^#${PREFIX}/#" TEMP
			echo "start delete s3 unmatched them"  >> ${LOGFILE}  2>&1
                        ##till now, here we disable auto delete them. will enable later
			#cat TEMP |xargs rm -rf
			## clear TEMP file
			> TEMP
			verify_process
		else
			echo "The directory backup is OK"  >> ${LOGFILE}  2>&1
		fi
	else
		verify_process	
	fi
}

##start script from here#######
check_sync_stat
