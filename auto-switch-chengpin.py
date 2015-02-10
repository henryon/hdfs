#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib2
import paramiko
import re
from pymongo  import MongoClient
'''
   author by henry wen, just finished some funtion V 0.1
'''


dict={'10.150.110.22':12,'10.150.110.23':12,'10.150.110.24':12,'10.150.110.21':12}

OKIP=[];


def checktraffic(para1):
	'''
	   check the uploading server api/uploading status
	'''
	print  "check traffic here"
	response=urllib2.urlopen(para1)
	html=response.read()
	result=re.findall(r'uploadSize',html)
	print result
	l=len(result)
	return l	



def updatemongo(para2,para3):
	'''
	   connect to mongodb and update the upload server status
	'''
	print "starting update mongo record"
	connection=MongoClient('10.10.10.2',27017)
	print "Here Connected to MongoDB"
	db = connection.upload
	print "Switch to upload "
	#collection = db.test_collection
	#db.c_uploadserver.update( {'ip' : para2},{'$set':{'dispatchstatus' :0 }},upsert=False, multi=False)
	#print "update dispatchstatus successfully"
	
	db.c_uploadserver.update( {'ip' : para2},{'$set':{'nodenumber' : para3}},upsert=False, multi=False)
	''' 
	    check the updated record status
	'''
	#if  db.c_uploadserver.find({'ip' : para2,'dispatchstatus' :0,'nodenumber' : para3 }).count()  == 1:
	#	print "Greate update mongodb successfully"
	if  db.c_uploadserver.find({'ip' : para2,'nodenumber' : para3 }).count()  == 1:
		print "Greate update mongodb successfully"

def restoremongo(para):
	'''
	   connect to mongodb and update the upload server status
	'''
	print "starting update mongo record"
	connection=MongoClient('10.10.10.2',27017)
	print "Here Connected to MongoDB"
	db = connection.upload
	print "Switch to upload "
	#collection = db.test_collection
	#db.c_uploadserver.update( {'ip' : para},{'$set':{'dispatchstatus' :1 }},upsert=False, multi=False)
	#print "update dispatchstatus successfully"
	''' 
	    check the updated record status
	'''
	#if  db.c_uploadserver.find({'ip' : para,'dispatchstatus' :1}).count()  == 1:
	#	print "Greate restore mongodb successfully"
	if  db.c_uploadserver.find({'ip' : para}).count()  == 1:
		print "Greate restore mongodb successfully"




def switchstorage(para3,para4):
	'''
	   do operation on server
	'''
	print 'Here'
	ssh = paramiko.SSHClient()
    #sh=paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	print "Good Connected to ssh server"
	ssh.connect(para3,22,"root")
	#print "Here ok connected"
	stdin, stdout, stderr = ssh.exec_command("cd /hdfs && rm  -rf cur && ln -s /hdfs/%s  cur"  % para4)
	#t = paramiko.Transport((“主机”,”端口”))
	#t.connect(username = “用户名”, password = “cha018R!!”)
	#print stdout
	print"**************************************************"
	'''
	for i in stderr.readlines():
		print i

	for i in stdout.readlines():
		print i
	'''

	#for i in stderr.readlines():
	
	print "restarting resin"
		
	stdin,stdout,stderr = ssh.exec_command("/usr/local/resin/bin/resin.sh restart && echo fine")

	print "Finished restart resin"
	return 0
	#for i in stderr.readlines():
	#	Line+=1
	#	if Line > 0:
	#		print "Force to start resin"

	#for i in stdout.readlines():
	#	print i

	#ssh.close()
	#verify return code api/uploading
	#OKIP.append('para3')

def getStatusCode(para5):
	print "On staging  here"
	r=requests.get(url,allow_redirects=False)
	if r.status_code == 200:
		print 'Greate'
		return 0
	
		

	print "check status here "
	#result=re.findall(r'uploadSize',html)
	#if len(result) > 0:
	#	print "right"
	#	return 0

if __name__ == "__main__":
	#get the IP list"

	while len(OKIP) != len(dict.keys()):
	   	
		print "We are starting"
		for key in dict.keys():
			if key in OKIP:
				print "this %s has been switched"  %  key
 			if len(OKIP) == len(dict.keys()):
 				print "finished  switched "
 				for i in list:
 					print i
 				print "empty the list"
 				OKIP=[]
			else:
				print 'Here start switch uploading server'
				url='http://%s/api/uploading' % key
 				if checktraffic(url)  == 0:
 					print "OKKKKKK"
 					updatemongo(key,dict[key])
 					if checktraffic(url)  == 0:
 						print "Good"
 						if switchstorage(key,dict[key]) == 0:
 							print "After switch, we check return code"
 							getStatusCode(url)
 							restoremongo(key)
 							OKIP.append(key)
 							print "We've finished switch for %s" % key
 						else:
 							print "check web return code error"

 		

	#print "Goodbye,We've finished all the server in dictionary "





