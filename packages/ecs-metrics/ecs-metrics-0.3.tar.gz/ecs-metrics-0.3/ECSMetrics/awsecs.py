import boto3
import json
import collections
import datetime
import os
from operations import *

class ECS:
	def createFolder(directory):
	    try:
	        if not os.path.exists(directory):
	            os.makedirs(directory)
	    except OSError:
	        print ('Error: Creating directory. ' +  directory)
        



	def awsECS(self, profile, cpuwarn, memwarn, d,h,m):

		session=boto3.session.Session(profile_name=profile)
		
		obj2.listCluster(session)
		my_json=None

		#mylist=[]
		final_list=[]
		pos=0
		

		for ele in obj3.Cluster:
			#p=ele.split('/')[1]
			#if(p=="hello-world-compute-env_Batch_929a21c9-89b5-3c12-baf0-9f7b418f7f21"):
			#	continue
			mylist=[]
			del obj3.Service[:]
			obj2.listService(session, ele)
			for ele2 in obj3.Service: 
				
				del obj3.TaskD[:]
				obj2.describeService(session, ele, ele2)

				for ele3 in obj3.TaskD: #CPU & MEMORY CHANGE
					del obj3.CPU[:]
					del obj3.MEMORY[:]
					obj2.describeTask(session, ele3)
					MaxCPU=max(obj3.CPU)
					MaxMEMORY=max(obj3.MEMORY)

				
				del obj3.Maxi[:]
				obj2.getMetricStatistics(session, 'CPUUtilization', ele, ele2, d,h,m) 
				obj2.getMetricStatistics(session, 'MemoryUtilization', ele, ele2, d,h,m) 

				cpuutil=0
				memutil=0
				cn=ele.split('/')[1]
				sn=ele2.split('/')[1]

				if len(obj3.Maxi)!=0:
					cpuutil=obj3.Maxi[0]
					memutil=obj3.Maxi[1]
					if obj3.Maxi[0]>cpuwarn:
						file1=open("service_for_cpu",'a+')
						file1.write("CLUSTER NAME -- %s"%cn)
						file1.write("     ")
						file1.write("SERVICE NAME -- %s"%sn)
						file1.write("\n\n")
						#print ("WARNING: CPU Usage Exceeded")

					if obj3.Maxi[1]>memwarn:
						file2=open("service_for_memory",'a+')
						file2.write("CLUSTER NAME -- %s"%cn)
						file2.write("     ")
						file2.write("SERVICE NAME -- %s"%sn)
						file2.write("\n\n")
					#print ("WARNING: Memory Usage Exceeded")

				
				p_dict={'CPU_Units':MaxCPU, 'MEMORY_Units':MaxMEMORY, 'CPU_Utilisation':cpuutil, 'MEMORY_Utilisation':memutil}

				k_dict=collections.OrderedDict()
				k_dict['Service_Name'] = ele2.split('/')[1]
				k_dict['Values'] = p_dict
				mylist.append(k_dict)
				#print("\n")
			
												
			look=collections.OrderedDict()
			look['Cluster_Name']=ele.split('/')[1]
			look['Services']=mylist

			
			
			
			
			final_list.append(look)
			
			
			
			print("----------------CLUSTER COMPLETED---------------------")
		
		add_dict={}
		add_dict['Cluster']=final_list
		my_json = json.dumps(add_dict, indent=2)

		# Example
		#createFolder('./data/')

		now = datetime.now()
		newDirName = now.strftime("%Y_%m_%d-%H%M")
		print "Making directory " + newDirName
		os.mkdir(newDirName)
		file=open("./"+newDirName+"/detail.json",'a+')


		
		file.write(my_json)
		file.write("\n")

			

obj=ECS()