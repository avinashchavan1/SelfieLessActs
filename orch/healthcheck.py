import time,csv,requests,threading,re,subprocess,os
def health():
	
		l=[]
		with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				l.append(row)
		print l		
		csv_file.close()
		for line in l:
			try:
				tempstr='http://localhost:'+str(line[1])+'/api/v1/_health'
				resp=requests.get(tempstr)
				if resp.status_code!=200:
					line[2]=False
				print resp.status_code
			except:	
				print "Container is Offline", str(line[1])
				#stop_relaunch(int(line[1]))
		print "\n"
		with open("log1.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(l)
		f.close()
		time.sleep(1)


def give_containerID(port):
	output = subprocess.check_output("sudo docker ps --format '{{.ID}}: {{.Ports}}'", shell=True)
	c=[]
	s=""
	for line in  output:
	
		if line=="\n":
			c.append(s)
			s=""
			continue
		s=s+line
	print c
	l=[]
	for line in c:
		l.append([line[0:12],int(line[22:26])])
	p=0
	for line in l:
		if line[1]==int(port):
			return line[0]


def stop_relaunch(port):
	temp=give_containerID(port)
	command='sudo '+'docker '+'stop '+str(temp)
	os.system(command)
	command='sudo '+'docker '+'rm '+str(temp)
	os.system(command)
	command='sudo '+'docker '+'run '+'-v '+'/home/ubuntu/data:/data '+'-d '+'-p '+str(port)+':'+str(80)+' acts:latest'
	os.system(command)
	return
"""
def stop_write(port):
	l=[]
	with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				if int(row[1])==int(port):
					pass
				else:
					l.append(row)
	csv_file.close()
	with open("log1.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(l)
	f.close()
"""

def stop_at_port(port):
	temp=give_containerID(port)
	command='sudo '+'docker '+'stop '+str(temp)
	os.system(command)
	command='sudo '+'docker '+'rm '+str(temp)
	os.system(command)
	l=[]
	with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				if int(row[1])==int(port):
					pass
				else:
					l.append(row)
	csv_file.close()
	with open("log1.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(l)
	f.close()
	return 1

def launch():
	l=[]
	with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				l.append(row)
	csv_file.close()
	print l
	a=l[-1][1]
	print int(a)+1
	b=int(l[-1][0][9])+1
	print b
	tp=["container"+str(b),str(int(a)+1),True,0]
	l.append(tp)
	a=int(int(a)+1)
	command='sudo '+'docker '+'run '+'-v '+'/home/ubuntu/data:/data '+' -d '+'-p '+str(a)+':'+str(80)+' acts:latest'
	com=os.system(command)
	print com
	if com!=0:
		return
	with open("log1.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(l)
	f.close()
	print "Succesfully launched container at ",a,"\n"
	return




def stop():
	l=[]
	with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				l.append(row)
	csv_file.close()
	print l
	a=l[-1][1]
	a=int(a)
	r=stop_at_port(a)
	if r==1:
		print "Sucessfully stopped container at ",a,"\n"
	else:
		print "Error"
	return

def consistency_check():
	l=[]
	with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				l.append(row)
	csv_file.close()
	flag=0
	#print l
	for line in l:
		if (line[2]==True or line[2]=='True') and int(line[3])==1:
			flag=1

	if flag==0:
		for line in l:
			if (line[2]==True or line[2]=='True') and int(line[3])==0:
				line[3]=1
				break

	with open("log1.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(l)
	f.close()



threading.Thread(target=consistency_check).start()
#launch()
#stop()


while(True):
	health()
	l=[]
	with open('log1.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				l.append(row)
	print l
	for line in l:
		if (line[2]==False or line[2]=="False"):
			stop_relaunch(int(line[1]))
			line[2]=True
	with open("log1.csv", "wb") as f:
			writer = csv.writer(f)
			writer.writerows(l)
	f.close()

