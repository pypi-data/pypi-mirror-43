import boto3
import json
import collections
from operations import *

class ECS:

	def awsECS(self, profile, cpuwarn, memwarn, d,h,m):

		session=boto3.session.Session(profile_name=profile)
		
		obj2.listCluster(session)

		for ele in obj3.Cluster:
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


				if obj3.Maxi[0]>cpuwarn:
					file1=open("service_for_cpu",'a+')
					file1.write(ele2.split('/')[1])
					file1.write("\n")
					#print ("WARNING: CPU Usage Exceeded")

				if obj3.Maxi[1]>memwarn:
					file2=open("service_for_memory",'a+')
					file2.write(ele2.split('/')[1])
					file2.write("\n")
					#print ("WARNING: Memory Usage Exceeded")

				
				p_dict={'CPU_Units':MaxCPU, 'MEMORY_Units':MaxMEMORY, 'CPU_Utilisation':obj3.Maxi[0], 'MEMORY_Utilisation':obj3.Maxi[1]}

				k_dict=collections.OrderedDict()
				k_dict['Service_Name'] = ele2.split('/')[1]
				k_dict['Values'] = p_dict

				mylist.append(k_dict)
												
				look=collections.OrderedDict()
				look['Cluster_Name']=(ele.split('/'))[1]
				look['Services']=mylist

				add_dict={'Cluster':[look]}
								
				my_json = json.dumps(add_dict, indent=2)
			file=open('detail.json','a+')
			file.write(my_json)
			file.write("\n")

			print("----------------CLUSTER COMPLETED---------------------")

obj=ECS()